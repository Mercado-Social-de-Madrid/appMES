"""
Django settings for appmes project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import environ
import sentry_sdk
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from firebase_admin import initialize_app

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

# Take environment variables from .env file
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
VERSION = "2.3.2"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
ADMINS = env.list("ADMINS")

SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS'),
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSRF_COOKIE_SAMESITE = None

# Application definition

INSTALLED_APPS = [
    # Custom apps
    'authentication',
    'benefits',
    'offers',
    'public',
    'news',
    'market',
    'core',
    'reports',

    # Third-party apps
    'qr_code',
    'ckeditor',
    'imagekit',
    'sass_processor',
    'log_viewer',
    'admin_interface',
    'colorfield',
    'rest_framework',
    'rest_framework.authtoken',
    'fcm_django',
    'django_unused_media',
    'modeltranslation',
    'localflavor',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',

    'django_cleanup.apps.CleanupConfig',  # Needs to be at the end
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

CSP_EXCLUDE_URL_PREFIXES = ("/admin/", "/auth/")
CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'", 'data:', 'maps.googleapis.com', 'chart.apis.google.com', 'maps.gstatic.com')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", 'data:', 'fonts.googleapis.com', 'www.gstatic.com', 'use.fontawesome.com', 'cdnjs.cloudflare.com')
CSP_FONT_SRC = ("'self'", "'unsafe-inline'", 'fonts.gstatic.com', 'use.fontawesome.com')
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", 'code.jquery.com', 'www.google.com', 'www.gstatic.com', 'cdnjs.cloudflare.com', 'maxcdn.bootstrapcdn.com', 'maps.googleapis.com')


ROOT_URLCONF = 'appmes.urls'
AUTH_USER_MODEL = 'authentication.User'

default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'market.context_processors.user_market',
                'core.context_processors.version_number',
            ],
            "loaders": default_loaders if DEBUG else cached_loaders,
        },
    },
]

WSGI_APPLICATION = 'appmes.wsgi.application'

# ======= Database Configuration ========
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PWRD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT')
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter', 
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATE_INPUT_FORMATS = ['%d/%m/%Y']

LANGUAGES = (
    ('es', _('Castellano')),
    ('eu', _('Euskara')),
    # ('ca', _('Catalá')),
    # ('gl', _('Galego')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'es'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('es', 'eu', )

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'documentation', 'admin', 'site', 'assets'),
    os.path.join(BASE_DIR, 'documentation', 'user', 'site', 'assets')
]
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

BASESITE_URL = env('BASESITE_URL')
LOGIN_URL = reverse_lazy('auth:login')
LOGIN_REDIRECT_URL = reverse_lazy('market:index')
LOGOUT_REDIRECT_URL = reverse_lazy('public:index')
SITE_ID = 1

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# ======= Logging Configuration ========
LOGGING_DIR = env('LOGGING_DIR')
os.makedirs(LOGGING_DIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'multi_thread_file_handler': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'mes.log'),
            'formatter': 'verbose',
        },
        'single_thread_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'mes.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 31,
            'formatter': 'verbose',
            'utc': True,
        },
    },
    'loggers': {
        '': {
            'handlers': env.list('LOGGING_HANDLERS'),
            'level': os.environ.get('LOGLEVEL', 'INFO').upper(),
            'propagate': False,
        },
    },
}

LOG_VIEWER_FILES = []
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = LOGGING_DIR
LOG_VIEWER_PAGE_LENGTH = 25  # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25  # Max log files loaded in Datatable per page
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None  # String regex expression to exclude the log from line

GMAPS_APIKEY = env('GOOGLE_MAPS_APIKEY')

INITIAL_LATITUDE = 40.43399206106631
INITIAL_LONGITUDE = -3.7048717038201344


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width':'100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Format', 'FontSize','TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-',  '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'Link', 'Unlink'],
        ]
    },
}

# ======= Mailing configuration =======

EMAIL_BACKEND = env('EMAIL_BACKEND')

# Email SMTP server configuration (can be local or an online service like SendGrid)
EMAIL_HOST = env('EMAIL_HOST_URL')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_SEND_FROM = env('EMAIL_SEND_FROM')

ENABLE_EMAIL_SENDING = env('ENABLE_EMAIL_SENDING') == 'True'

# ======= Sentry Configuration ========
sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=0.5,
    environment=env('SENTRY_ENV')
)

# ======= Firebase Configuration ========
FIREBASE_APP = initialize_app()
FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}

# ======= APP Links Configuration ======
ASSETLINKS_FILE = os.path.join(ROOT_DIR, env('ASSETLINKS_FILE'))

# ======= Semantic search Config =======
SEMANTIC_SIMILARITY_THRESHOLD = env('SEMANTIC_SIMILARITY_THRESHOLD', float, 0.7)
ENABLE_VECTOR_EMBEDDING = env('ENABLE_VECTOR_EMBEDDING', bool, False)
