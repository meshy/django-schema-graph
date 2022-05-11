import environ
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ROOT_URLCONF = "tests.urls"
SECRET_KEY = "not-for-production"
INSTALLED_APPS = [
    "tests.app_a",
    "tests.app_b",
    "tests.app_c",
    "tests.app_d",
    "tests.basic",
    "tests.generic",
    "tests.inheritance",
    "tests.installed",
    "tests.proxy",
    "schema_graph",
    'django.contrib.admindocs',
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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
TEMPLATES = (
    {"BACKEND": "django.template.backends.django.DjangoTemplates",
     "APP_DIRS": True,
     'OPTIONS': {
         'context_processors': [
             'django.template.context_processors.debug',
             'django.template.context_processors.request',
             'django.contrib.auth.context_processors.auth',
             'django.contrib.messages.context_processors.messages',
         ],
     },
     },
)
STATIC_URL = "/static/"
