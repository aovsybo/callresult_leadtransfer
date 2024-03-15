import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = 'django-insecure-o^vy^sje-9(7*rbcga-@c0vvxp*j_%kwo@s9+l57tgfqyfp&gu'
DEBUG = True if os.environ.get("DEBUG") == "True" else False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(',')


WR_INTEGRATION_SUBDOMAIN = os.environ.get("WR_INTEGRATION_SUBDOMAIN")
WR_INTEGRATION_CLIENT_SECRET = os.environ.get("WR_INTEGRATION_CLIENT_SECRET")
WR_INTEGRATION_CLIENT_ID = os.environ.get("WR_INTEGRATION_CLIENT_ID")
WR_INTEGRATION_CODE = os.environ.get("WR_INTEGRATION_CODE")
WR_INTEGRATION_REDIRECT_URI = os.environ.get("WR_INTEGRATION_REDIRECT_URI")
WR_REFRESH_TOKEN = os.environ.get("WR_REFRESH_TOKEN")

AMO_CONTACT_FIELD_IDS = {
    1124905: "phone",
    1124907: "email",
    # 794014: "date",
    # 784770: "site",
    # 612396: "city",
    # 794016: "page",
}
AMO_LEAD_FIELD_IDS = {
    # 166045: "utm_source",
    # 166043: "utm_medium",
    # 166047: "utm_campaign",
    # 166051: "utm_content",
    # 166049: "utm_term",
    # 754509: "roistat_visit",
}
AMO_LEAD_STATUS_ID = 64999962  # Стадия внутри воронки
AMO_LEAD_PIPELINE_ID = 7908070  # Воронка

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'leadtransfer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  os.environ.get("POSTGRES_DB"),
        'USER':  os.environ.get("POSTGRES_USER"),
        'PASSWORD':  os.environ.get("POSTGRES_PASSWORD"),
        'HOST':  os.environ.get("POSTGRES_HOST"),
        'PORT':  os.environ.get("POSTGRES_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
