from .base import *

import raven


DEBUG = bool(int(os.environ.setdefault("DEBUG", "0")))
GIT_SHA = raven.fetch_git_sha(os.path.dirname(os.pardir))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'rocket',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': os.environ.setdefault("MAIN_DB_USER", ""),
        'PASSWORD': os.environ.setdefault("MAIN_DB_PASS", ""),
        'HOST': os.environ.setdefault("MAIN_DB_HOST", ""),
        'PORT': os.environ.setdefault("MAIN_DB_PORT", ""),
        'CONN_MAX_AGE': 600,
    }
}

RAVEN_CONFIG = {
    'dsn': os.environ.setdefault("RAVEN_SENTRY_URL", ""),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': GIT_SHA,
}