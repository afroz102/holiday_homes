import os
from django.contrib import messages

# after adding lines in answer above all css files should be associated correctly
import mimetypes
mimetypes.add_type("text/css", ".css", True)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9s^+-bt9x&dr&(_*yflscjfqoj!^skeeuh-^i%c&93%=dua#h9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS",
                          "127.0.0.1,localhost").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bookings',
    'home',
    'landlords',
    'tasks',
    'units',
    'users',

    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug toolbar
]

ROOT_URLCONF = 'holiday_homes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'holiday_homes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{
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

# For debugging toolbar
INTERNAL_IPS = ['127.0.0.1']


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar, }


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'

# Uploaded Image will be stored here
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


'''
He X-Frame-Options is used to prevent the site from clickjacking attacks.
It defines whether or not a browser should be allowed to render a page in a
< frame > , < iframe > , < embed > or < object > . The frame-ancestors
directive present in Content-Security-Policy(CSP) obsoletes X-Frame-Options.
'''
X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

# Email config
AUTHENTICATION_BACKENDS = (
    'users.authentication.EmailBackend',
)

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sahiljmi102@gmail.com'
EMAIL_HOST_PASSWORD = 'Sahilraza@1029534'


# To display flash messages type as bootstrap class
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
