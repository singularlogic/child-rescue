from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('me/', UserDetail.as_view(), name='me'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/', PasswordReset.as_view(), name='password_reset'),
    path('', UserList.as_view(), name='get_users')
]

urlpatterns = format_suffix_patterns(urlpatterns)
