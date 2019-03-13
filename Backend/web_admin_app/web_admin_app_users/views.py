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

from core.organizations.utils import OrganizationUtils
from core.users.models import User, Uuid
from core.users.utils import save_profile_image
from core.users.uuid_management import UuidManagement
from .serializers import UserSerializer, ForgotPasswordSerializer, PasswordResetSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        has_role_attached = 'role' in request.data and request.data['role'] is not None and len(request.data['role']) > 0
        has_organization_attached = 'organization' in request.data and request.data['organization'] is not None and len(request.data['organization']) > 0

        def _has_role_permissions(role):
            if request.user.role == 'admin':
                return True
            elif request.user.role == 'owner':
                if role not in ['admin', 'owner']:
                    return True
                else:
                    return False
            elif request.user.role == 'coordinator':
                if role not in ['admin', 'owner', 'coordinator']:
                    return True
                else:
                    return False
            elif request.user.role == 'case_manager':
                return False
            elif request.user.role == 'network_manager':
                return False
            elif request.user.role == 'facility_manager':
                return False

        if 'email' in request.data:
            email = request.data['email'].lower()
            email_count = User.objects.filter(email=email).count()
            if email_count != 0:
                return Response(['Email already exists'], status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(['Email is required'], status=status.HTTP_403_FORBIDDEN)

        if has_role_attached:
            if not _has_role_permissions(request.data['role']):
                return Response('({}) user has not permission to create {}'.format(
                    request.user.role or 'Simple',
                    request.data['role'].title()
                ),
                    status=status.HTTP_403_FORBIDDEN)
        else:
            return Response('You should provide a valid role for user', status=status.HTTP_403_FORBIDDEN)

        if has_organization_attached:
            if request.data['role'] == 'admin':
                return Response('Admin does not belong to any organization', status=status.HTTP_403_FORBIDDEN)
        else:
            if request.data['role'] != 'admin':
                return Response('You should provide an organization for user', status=status.HTTP_403_FORBIDDEN)

        if not OrganizationUtils.exists(request.data['organization']):
            return Response('Organization does not exist', status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if 'profile_image' in request.data:
            instance.profile_image.delete(save=False)

            image = request.data['profile_image']
            image = save_profile_image(image, request.user)
            request.data['profile_image'] = image

        if 'password' in request.data:
            request.data.pop('password')

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLogin(APIView):

    def post(self, request, *args, **kwargs):
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET
        url = settings.BASE_URL + 'auth/token/'

        if 'email' not in request.data or 'password' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email'].lower()
        password = request.data['password']

        params = {
            'grant_type': 'password',
            'username': email,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        }

        login_request = requests.post(url, data=params)
        response = login_request.json()

        if 'error' in response:
            content = {
                'data': 'Wrong credentials'
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        if 'uuid' in request.data:
            uuid = Uuid.objects.filter(value=request.data['uuid']).first()

            if uuid is not None:
                oauth2_access_token = AccessToken.objects.get(token=response['access_token'])
                uuid.user = oauth2_access_token.user
                uuid.save()

            action = 'login'
            params = ''
            device = request.data.get('device', '')
            UuidManagement.log_action(request, request.data['uuid'], action, params, device)

        return Response(response, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET
        url = settings.BASE_URL + 'auth/revoke-token/'

        params = {
            'token': request.auth.token,
            'client_id': client_id,
            'client_secret': client_secret
        }

        try:
            uuid = Uuid.objects.filter(user=request.user).last()
            fcm_device = uuid.device
            fcm_device.active = False
            fcm_device.save()
        except Exception as ex:
            print(ex)

        requests.post(url, data=params)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPassword(APIView):

    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            user = get_object_or_404(User, email=email)
            params = {
                'email': user.email,
                'base_url': settings.BASE_URL,
                'site_name': 'www.child-rescue.com',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': default_token_generator.make_token(user)
            }
            email_template_name = 'users/password_reset_email.html'
            subject = 'Child Rescue Reset Password'
            email = loader.render_to_string(email_template_name, params)
            send_mail(subject, email, 'Child Rescue <%s>' % settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

            content = {'response': 'Reset password email sent successfully.'}
            return Response(content, status=status.HTTP_200_OK)

        content = {'response': 'Invalid data.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):

    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']

            uid = urlsafe_base64_decode(uid).decode()
            user = get_object_or_404(User, pk=uid)
            if user is not None and default_token_generator.check_token(user, token):
                password = serializer.validated_data['password']
                user.set_password(password)
                user.save()
                content = {'data': 'Password updated successfully'}
                return Response(content, status=status.HTTP_201_CREATED)

            content = {'data': 'User does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        content = {'data': 'Invalid data'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
