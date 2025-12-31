import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition (minimal for dev)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Local apps
INSTALLED_APPS += [
    "crispy_forms",
    "widget_tweaks",
    "rest_framework",
    "accounts",
    "elections",
    "voting",
    "notifications",
    "results",
    # Scaffolding apps
    "audit",
    "reports",
    "integrity",
    "ledger",
    "monitoring",
    "disputes",
    "analytics",
    "integrations",
    "offline",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom middleware for revocation checks
    "accounts.middleware.RevokedAccessTokenMiddleware",
]

ROOT_URLCONF = "evoting_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "evoting_system.wsgi.application"
ASGI_APPLICATION = "evoting_system.asgi.application"

# Database - use SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Vote encryption key settings
VOTE_KEYS_DIR = str(BASE_DIR / "keys")
VOTE_PRIVATE_KEY_FILE = "private_key.pem"
VOTE_PUBLIC_KEY_FILE = "public_key.pem"
# Tally signing key settings (used to sign encrypted payloads and verify signatures at tally time)
TALLY_PRIVATE_KEY_FILE = "tally_sign_private.pem"
TALLY_PUBLIC_KEY_FILE = "tally_sign_public.pem"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Optional Sentry integration
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()], traces_sample_rate=0.1)
    except Exception:
        # don't block startup if sentry not installed
        pass
