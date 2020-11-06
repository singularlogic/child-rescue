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
from users.models import User, Uuid
from users.uuid_management import UuidManagement
from users.web_admin_api.permissions import UserObjectPermissions, UserPermissions
from .serializers import (
    UserSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

    def list(self, request, *args, **kwargs):
        organization = request.user.organization
        role = request.query_params.get("role", None)
        queryset = User.objects.get_users(organization=organization, role=role)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # self.check_object_permissions(self.request, request.data.get("organization", None))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserObjectPermissions,)

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        self.check_object_permissions(self.request, get_object_or_404(User, id=pk))
        return User.objects.get(id=pk)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if "password" in request.data:
            request.data.pop("password")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        r = UserRanking(instance)
        fr = r.get_new_user_rank()
        instance.ranking = fr
        instance.save()

        return Response(serializer.data)


class UserMe(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
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

            if uuid is not None:
                oauth2_access_token = AccessToken.objects.get(token=response["access_token"])
                uuid.user = oauth2_access_token.user
                uuid.save()

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


class ForgotPassword(APIView):
    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"].lower()
            user = get_object_or_404(User, email=email)
            params = {
                "email": user.email,
                "base_url": settings.BASE_FE_URL,
                "site_name": "platform.childrescue.eu",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
            }
            email_template_name = "users/reset_password.html"
            prefix = settings.SERVER.upper() + " " if settings.SERVER != 'production' else ""
            subject = "{}Child Rescue Reset Password".format(prefix)
            # email = loader.render_to_string(email_template_name, params)
            html_content = loader.get_template(email_template_name).render(params)
            send_mail(
                subject,
                "",
                "Child Rescue <%s>" % settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=html_content,
            )
            return Response("success", status=status.HTTP_200_OK)
        return Response("not_found", status=status.HTTP_404_NOT_FOUND)


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


class ChangePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        old_password = request.data["oldPassword"]
        user = self.request.user
        if user is not None:
            if user.check_password(old_password):
                user.set_password(request.data["password"])
                user.save()
                return Response("success", status=status.HTTP_201_CREATED)
            else:
                return Response("invalid_old_password", status=status.HTTP_201_CREATED)
        else:
            content = {"data": "Invalid data"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
