from pathlib import Path
import os
from decouple import config

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',cast=bool, default=True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #3rd party
    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    'dj_rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
     #'rest_auth',
    'debug_toolbar',
    'taggit',
    'taggit_serializer',
    #my apps
    'pages.apps.PagesConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
]

# DJANGO RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ], 
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',# debug toolbar
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

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

WSGI_APPLICATION = 'base.wsgi.application'


# Datamav
# https://docs.djangoproject.com/en/3.1/ref/settings/#datamavs

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'PORT':config('PORT', cast=int),
        'HOST':config('HOST'),
        #'SSL':
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
        


# DJANGO DEBUG TOOLBAR CONFIGS
INTERNAL_IPS = [
    '127.0.0.1',
]

# DJANGO-CRISPY-FORMS CONFIGS
# ------------------------------------------------------------------------------
# https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# CUSTOM USER MODEL CONFIGS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'users.User'

# DJANGO-ALLAUTH CONFIGS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
#email backends
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#authentication backends REQURED!!!
AUTHENTICATION_BACKENDS = (
   "django.contrib.auth.backends.ModelBackend",
   "allauth.account.auth_backends.AuthenticationBackend"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'pages:index'
# https://django-allauth.readthedocs.io/en/latest/views.html#logout-account-logout
LOGOUT_REDIRECT_URL = 'pages:index'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGGING ={
    'version':1,
    'loggers':{
        'django':{
            'handlers':['file','file2'],
            'level':'DEBUG'
        }
    },
    'handlers':{
        'file':{
            'level':'INFO',
            'class': 'logging.FileHandler',
            'filename':'./logs/debug5.log',
            'formatter':'simpleRe',
        },
        'file2':{
            'level':'DEBUG',
            'class': 'logging.FileHandler',
            'filename':'./logs/debug6.log',
            'formatter':'simpleRe',
        }
    },
    'formatters':{
        'simpleRe': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }

    }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['app_name.herokuapp.com'] # include your host name here!!
    DEBUG = False
