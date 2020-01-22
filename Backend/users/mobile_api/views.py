import datetime
import requests

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken

from analytics.analytics_basic import UserRanking
from users.mobile_api.serializers import (
    UserSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    UuidActivitySerializer,
)
from users.models import User, Uuid, UuidActivity
from users.utils import save_profile_image
from users.uuid_management import UuidManagement


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        def verify_email():
            if "email" in request.data:
                email = request.data["email"].lower()
                email_count = User.objects.filter(email=email).count()
                if email_count != 0:
                    return Response(["Email already exists"], status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(["Email is required"], status=status.HTTP_403_FORBIDDEN)

        verify_email()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET
        url = settings.BASE_AUTH_URL + "auth/token/"

        if "email" not in request.data or "password" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        email = request.data["email"].lower()
        password = request.data["password"]

        params = {
            "grant_type": "password",
            "username": email,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        login_request = requests.post(url, data=params)
        response = login_request.json()

        if "error" in response:
            content = {"data": "Wrong credentials"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        if "uuid" in request.data:
            uuid = Uuid.objects.filter(value=request.data["uuid"]).first()

            oauth2_access_token = AccessToken.objects.get(token=response["access_token"])
            user = oauth2_access_token.user
            if uuid is not None:
                uuid.user = user
                uuid.save()
            user.last_login = datetime.datetime.now()
            user.save()

            action = "login"
            params = ""
            device = request.data.get("device", "")
            UuidManagement.log_action(request, request.data["uuid"], action, params, device)

        return Response(response, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET
        url = settings.BASE_AUTH_URL + "auth/revoke-token/"

        params = {
            "token": request.auth.token,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        try:
            uuid = Uuid.objects.filter(user=request.user).last()
            fcm_device = uuid.device
            # fcm_device.active = False
            fcm_device.save()
        except Exception as ex:
            print(ex)

        requests.post(url, data=params)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            uuid = Uuid.objects.filter(user=self.request.user).last()
            fcm_device = uuid.device
            fcm_device.active = True
            fcm_device.save()
        except Exception as ex:
            print(ex)

        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if "profile_image" in request.data:
            instance.profile_image.delete(save=False)

            image = request.data["profile_image"]
            image = save_profile_image(image, request.user)
            request.data["profile_image"] = image

        if "password" in request.data:
            request.data.pop("password")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        user = self.request.user
        r = UserRanking(user)
        fr = r.get_new_user_rank()
        user.ranking = fr
        user.save()
        return Response(serializer.data)


class ForgotPassword(APIView):
    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"].lower()
            user = get_object_or_404(User, email=email)
            params = {
                "email": user.email,
                "base_url": settings.BASE_AUTH_URL,
                "site_name": "www.child-rescue.com",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                "user": user,
                "token": default_token_generator.make_token(user),
            }
            email_template_name = "users/password_reset_email.html"
            subject = "Child Rescue Reset Password"
            email = loader.render_to_string(email_template_name, params)
            send_mail(
                subject, email, "Child Rescue <%s>" % settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False,
            )

            content = {"response": "Reset password email sent successfully."}
            return Response(content, status=status.HTTP_200_OK)

        content = {"response": "Invalid data."}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data["uid"]
            token = serializer.validated_data["token"]

            uid = urlsafe_base64_decode(uid).decode()
            user = get_object_or_404(User, pk=uid)
            if user is not None and default_token_generator.check_token(user, token):
                password = serializer.validated_data["password"]
                user.set_password(password)
                user.save()
                content = {"data": "Password updated successfully"}
                return Response(content, status=status.HTTP_201_CREATED)

            content = {"data": "User does not exist"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        content = {"data": "Invalid data"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class UuidActivityCreate(generics.CreateAPIView):
    queryset = UuidActivity.objects.all()
    serializer_class = UuidActivitySerializer

    def create(self, request, *args, **kwargs):

        if "uuid" not in request.data or request.data["uuid"] == "":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        uuid = Uuid.objects.filter(value=request.data["uuid"]).first()

        if uuid is None:
            uuid = Uuid.objects.create(value=request.data["uuid"])

            if request.user.is_authenticated:
                uuid.user = request.user
                uuid.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uuid=uuid)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
