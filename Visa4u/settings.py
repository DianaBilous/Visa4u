"""
Django settings for Visa4u project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',

    # Django apps
    'django.contrib.sites',  # django-allauth

    # django-allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Социальные провайдеры
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.yandex',
    # 'allauth.socialaccount.providers.vk',

    'apps.visas',
    'apps.accounts',
    'apps.consultations',
    'apps.chat',

    'phonenumber_field',
]

PHONENUMBER_DEFAULT_REGION = 'RU'  # регион по умолчанию (Россия)
PHONENUMBER_DB_FORMAT = 'NATIONAL'  # Как хранить номер телефона в базе данных (NATIONAL/INTERNATIONAL)
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

SITE_ID = 3

ASGI_APPLICATION = 'Visa4u.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  # Адрес сервера Redis
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Управление визовыми заявками",
    "site_header": "Админка ClickCheck",
    "welcome_sign": "Добро пожаловать в административную панель",
    "site_brand": "ClickCheck",
    "site_logo": "images/logo.png",  # Добавьте сюда путь к логотипу
    "show_ui_builder": True,

    # Настройка меню с категориями
    "topmenu_links": [
        # Ссылка на главную страницу сайта
        {"name": "Выйти на сайт", "url": "/", "new_window": True},
        
        # Группа "Визы"
        {"name": "Визы", "icon": "fas fa-passport", "models": [
            {"name": "Страны", "model": "visas.country"},
            {"name": "Типы виз", "model": "visas.visatype"},
            {"name": "Требования к визам", "model": "visas.visarequirement"},
            {"name": "Документы для виз", "model": "visas.visadocument"},
            {"name": "Оценка шансов", "model": "visas.visaassessment"},
            {"name": "Заказы виз", "model": "visas.visaorder"},
            {"name": "Загрузки документов", "model": "visas.documentupload"},
            {"name": "Часто задаваемые вопросы", "model": "visas.faq"},
        ]},

        # Группа "Консультации"
        {"name": "Консультации", "icon": "fas fa-calendar-alt", "models": [
            {"name": "Доступные слоты", "model": "consultations.availableslot"},
            {"name": "Консультации", "model": "consultations.consultation"},
        ]},

        # Группа "Чат"
        {"name": "Чат", "icon": "fas fa-comments", "models": [
            {"name": "Сообщения", "model": "chat.message"},
        ]},
    ],

    # Настройки иконок для моделей
    "icons": {
        "visas.Country": "fas fa-flag",
        "visas.VisaType": "fas fa-passport",
        "visas.VisaRequirement": "fas fa-file-alt",
        "visas.VisaDocument": "fas fa-folder",
        "visas.VisaAssessment": "fas fa-check-circle",
        "visas.VisaOrder": "fas fa-file-signature",
        "visas.FAQ": "fas fa-question-circle",
        "visas.DocumentUpload": "fas fa-upload",
        "consultations.AvailableSlot": "fas fa-calendar-check",
        "consultations.Consultation": "fas fa-user-clock",
        "chat.Message": "fas fa-comments",
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'Visa4u.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Visa4u.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Стандартная аутентификация Django
    'allauth.account.auth_backends.AuthenticationBackend',  # Аутентификация через соцсети
]

# Настройки авторизации
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Вход через email
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Email подтверждение

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для перенаправлений после аутентификации
LOGIN_REDIRECT_URL = 'dashboard'  # Переадресация на личный кабинет после входа
LOGOUT_REDIRECT_URL = '/'         # Переадресация на главную страницу после выхода

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Почта, с которой будут отправляться письма
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Пароль или пароль приложения для Gmail
DEFAULT_FROM_EMAIL = 'noreply@clickcheck.com'  # Это будет указано как "От кого" в письме
