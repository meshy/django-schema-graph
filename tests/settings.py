import environ


env = environ.Env()


DATABASES = {"default": env.db(default="sqlite://:memory:")}
SECRET_KEY = "not-for-production"
INSTALLED_APPS = [
    "tests",
    "schema_graph",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
TEMPLATES = (
    {"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True},
)
STATIC_URL = "/static/"
