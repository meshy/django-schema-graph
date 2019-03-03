import environ


env = environ.Env()


DATABASES = {'default': env.db(default='sqlite://:memory:')}
SECRET_KEY = 'not-for-production'
