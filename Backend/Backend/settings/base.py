"""
Django settings for Backend project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = []


# Application definition

BASE_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
]

PRODUCT_APPS = [
    'core.users.apps.UsersConfig',
    'core.organizations.apps.OrganizationsConfig',
    'core.cases.apps.CasesConfig',
    'core.alerts.apps.AlertsConfig',
    'core.evidences.apps.EvidencesConfig',
    'core.choices.apps.ChoicesConfig',
    'core.firebase.apps.FirebaseConfig',

    'web_admin_app.web_admin_app_users.apps.WebAdminAppUsersConfig',
    'web_admin_app.web_admin_app_organizations.apps.WebAdminAppOrganizationsConfig',
    'web_admin_app.web_admin_app_cases.apps.WebAdminAppCasesConfig',
    'web_admin_app.web_admin_app_alerts.apps.WebAdminAppAlertsConfig',
    'web_admin_app.web_admin_app_evidences.apps.WebAdminAppEvidencesConfig',
    'web_admin_app.web_admin_app_choices.apps.WebAdminAppChoicesConfig',

    'mobile_app.mobile_app_users.apps.MobileAppUsersConfig',
    'mobile_app.mobile_app_cases.apps.MobileAppCasesConfig',
    'mobile_app.mobile_app_alerts.apps.MobileAppAlertsConfig',
    'mobile_app.mobile_app_evidences.apps.MobileAppEvidencesConfig',
    'mobile_app.mobile_app_firebase.apps.MobileAppFirebaseConfig',
]

INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + PRODUCT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Backend.urls'
AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Backend.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Django REST Framework Configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}


# Django REST Framework Social Auth 2 configuration

AUTHENTICATION_BACKENDS = (

    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

    # Google
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)


# Django OAuth Toolkit Configuration

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
    'REFRESH_TOKEN_EXPIRE_SECONDS': 63072000,
    'ACCESS_TOKEN_EXPIRE_SECONDS': 31536000
}


# Facebook configuration

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET')

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}

# Google configuration

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


# Social Auth Pipeline

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'users.social_pipeline.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'users.social_pipeline.user_details',
    'users.social_pipeline.save_avatar',
)


# CORS Configuration

CORS_ORIGIN_ALLOW_ALL = True
CSRF_COOKIE_NAME = 'csrftoken'


# Important Variables

BASE_URL = os.getenv('BASE_URL')
OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        # 'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.getenv('POSTGRES_DATABASE_NAME'),
        "USER": os.getenv('POSTGRES_DATABASE_USER'),
        "PASSWORD": os.getenv('POSTGRES_DATABASE_PASSWORD'),
        "HOST": os.getenv('POSTGRES_DATABASE_HOST'),
        "PORT": os.getenv('POSTGRES_DATABASE_PORT'),
    }
}


# SMTP Mail Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('gr', gettext('Greek')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
