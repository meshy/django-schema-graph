import environ


env = environ.Env()


DATABASES = {"default": env.db(default="sqlite://:memory:")}
SECRET_KEY = "not-for-production"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "schema_graph.tests",
]
