import os
from pathlib import Path
import datetime
# Sentry optional import
try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
except Exception:  # pragma: no cover
    sentry_sdk = None
    DjangoIntegration = None

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - controlled by environment for deployment
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", os.environ.get("SECRET_KEY", "dev-secret-key"))
# DEBUG should be False in production. Control via env var 'DJANGO_DEBUG'.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']

# Security-related settings (toggleable via DJANGO_SECURE or explicit env vars)
DJANGO_SECURE = os.environ.get('DJANGO_SECURE', 'False').lower() in ('1', 'true', 'yes')
# HSTS: set via SECURE_HSTS_SECONDS or enable with DJANGO_SECURE
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000' if DJANGO_SECURE else '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True' if DJANGO_SECURE else 'False').lower() in ('1', 'true', 'yes')
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True' if DJANGO_SECURE else 'False').lower() in ('1', 'true', 'yes')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True' if DJANGO_SECURE else 'False').lower() in ('1', 'true', 'yes')
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True' if DJANGO_SECURE else 'False').lower() in ('1', 'true', 'yes')
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True' if DJANGO_SECURE else 'False').lower() in ('1', 'true', 'yes')
SECURE_REFERRER_POLICY = os.environ.get('SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin')
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Redis / Celery defaults
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/1")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/2")

K_CACHE_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "300"))

# Application definition (minimal for dev)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",

]

# Local apps
INSTALLED_APPS += [
    "abac",
    "crispy_forms",
    "widget_tweaks",
    "rest_framework",
    "ai_ops",
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
    "posters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom middleware for revocation checks
    "accounts.middleware.RevokedAccessTokenMiddleware",
]

# Session idle timeout (seconds). Default 30 minutes for MVP.
SESSION_IDLE_TIMEOUT = int(os.environ.get('SESSION_IDLE_TIMEOUT', 1800))

# Add session timeout middleware after AuthenticationMiddleware
MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1, 'accounts.middleware.SessionIdleTimeoutMiddleware')
# Add suspension enforcement middleware to prevent access during suspension
MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 2, 'accounts.suspension_middleware.SuspensionEnforcementMiddleware')
# Ensure RolePortalGuardMiddleware runs after authentication so request.user is set
MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 3, 'accounts.middleware.RolePortalGuardMiddleware')
# Redirect staff users who open /admin/ to the custom admin dashboard
MIDDLEWARE.insert(MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 4, 'accounts.middleware.AdminRedirectMiddleware')
# Add CSP middleware after Security/WhiteNoise
MIDDLEWARE.insert(2, "accounts.middleware.ContentSecurityPolicyMiddleware")
# Add IP geolocation blocking middleware (runs early to catch blocked IPs)
MIDDLEWARE.insert(1, "accounts.middleware.GeoBlockingMiddleware")

ROOT_URLCONF = "evoting_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "accounts" / "templates",  # ensure legacy accounts/* templates resolve
        ],
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

# Database — always PostgreSQL (no SQLite fallback)
# Defaults target the local Docker compose setup; override via env vars for other environments.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "evoting"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# Caching (Redis)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": K_CACHE_TIMEOUT,
    }
}
# Use database sessions for better reliability (cache sessions can have timing issues)
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Password validation
AUTH_PASSWORD_VALIDATORS = []
# Use strong password hashing (Argon2 preferred)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (local or S3)
USE_S3 = os.environ.get('USE_S3', 'False').lower() in ('1', 'true', 'yes')

if USE_S3:
    # S3 Storage (requires django-storages[s3])
    try:
        INSTALLED_APPS.append('storages')
    except Exception:
        pass
    # AWS S3 configuration
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'default-bucket')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',  # 1 day
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = os.environ.get('AWS_S3_FILE_OVERWRITE', 'False').lower() in ('1', 'true')
    AWS_QUERYSTRING_AUTH = os.environ.get('AWS_QUERYSTRING_AUTH', 'False').lower() in ('1', 'true')
    
    # Static files on S3
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATIC_ROOT = 's3://static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # Media files on S3
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    MEDIA_ROOT = 's3://media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    # Local file storage (Render disk or local filesystem)
    STATIC_URL = os.environ.get('STATIC_URL', '/static/')
    STATIC_ROOT = os.environ.get('STATIC_ROOT', BASE_DIR / 'staticfiles')
    MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
    MEDIA_ROOT = os.environ.get('MEDIA_ROOT', BASE_DIR / 'media')
    
    # Include the project's top-level `static/` directory for staticfiles discovery during development
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
    
    # Use manifest storage in production; simpler storage in debug to avoid missing-manifest errors during dev
    if DEBUG:
        STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    else:
        STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Vote encryption key settings
VOTE_KEYS_DIR = str(BASE_DIR / "keys")
VOTE_PRIVATE_KEY_FILE = "private_key.pem"
VOTE_PUBLIC_KEY_FILE = "public_key.pem"
# Tally signing key settings (used to sign encrypted payloads and verify signatures at tally time)
TALLY_PRIVATE_KEY_FILE = "tally_sign_private.pem"
TALLY_PUBLIC_KEY_FILE = "tally_sign_public.pem"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

# Default post-login redirect for Django auth — send students to voting home
LOGIN_REDIRECT_URL = '/'
# Explicit login URL so auth mixins don't rely on a namespaced URL name
LOGIN_URL = '/accounts/login/'

# Access token signing secret (use a secure value in prod, e.g., from KMS)
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "dev-access-secret")

# REST framework: add our JTI authentication backend
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "accounts.authentication.JTIAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": os.environ.get("THROTTLE_USER_RATE", "200/min"),
        "anon": os.environ.get("THROTTLE_ANON_RATE", "50/min"),
    },
}

# Celery configuration
CELERY_BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_ROUTES = {
    "evoting_system.tasks.send_otp_email": {"queue": "otp"},
    "evoting_system.tasks.send_otp_sms": {"queue": "otp"},
    "evoting_system.tasks.send_login_notice": {"queue": "notify"},
    "evoting_system.tasks.clear_expired_otps": {"queue": "maintenance"},
    "evoting_system.tasks.unlock_account": {"queue": "maintenance"},
    "evoting_system.tasks.process_suspension_expirations": {"queue": "maintenance"},
    "evoting_system.tasks.log_vote_event": {"queue": "default"},
    "evoting_system.tasks.update_turnout_counter": {"queue": "default"},
    "evoting_system.tasks.notify_voting_spike": {"queue": "notify"},
    "evoting_system.tasks.generate_candidate_qr_bulk": {"queue": "low"},
    "evoting_system.tasks.resize_candidate_photo": {"queue": "low"},
    "evoting_system.tasks.compute_results_tally": {"queue": "reports"},
    "evoting_system.tasks.generate_results_pdf": {"queue": "reports"},
    "evoting_system.tasks.run_security_monitor_task": {"queue": "security"},
}
CELERY_BEAT_SCHEDULE = {
    "clear-expired-otps": {
        "task": "evoting_system.tasks.clear_expired_otps",
        "schedule": 300.0,
    },
    "process-suspension-expirations": {
        "task": "evoting_system.tasks.process_suspension_expirations",
        "schedule": 3600.0,  # Run every hour
    },
    "security-monitor": {
        "task": "evoting_system.tasks.run_security_monitor_task",
        "schedule": 600.0,
    },
}

# Sentry (optional)
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN and sentry_sdk and DjangoIntegration:
    try:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration()],
            traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.05")),
            send_default_pii=False,
        )
    except Exception:
        # don't block startup if sentry not installed
        pass

# Media / storage configuration: enable S3-backed media when env vars present
if os.environ.get('AWS_STORAGE_BUCKET_NAME'):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', None)
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', None)
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    # optional: use unsigned URLs OR set MEDIA_URL explicitly
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Site URL for QR generation and absolute links
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')

# Optional Sentry integration (legacy block kept for safety)
if SENTRY_DSN and sentry_sdk and DjangoIntegration:
    try:
        sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()], traces_sample_rate=0.1)
    except Exception:
        pass
# Email configuration
# By default, use console backend during development. In production (DEBUG=False)
# prefer SMTP backend unless `EMAIL_BACKEND` is explicitly set via env var.
if os.environ.get('EMAIL_BACKEND'):
    EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' if not DEBUG else 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'voting@university.edu')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'voting@university.edu')

# Email template directory for render_to_string
EMAIL_TEMPLATE_DIR = BASE_DIR / 'templates' / 'accounts' / 'email'

# Development helpers
# When True (and DEBUG=True) the password API may return the generated code
# in responses for local testing. This flag is forcibly disabled when DEBUG=False
# to prevent accidental leakage in production.
DEV_ALLOW_DEBUG_CODES = False
if DEBUG:
    DEV_ALLOW_DEBUG_CODES = os.environ.get('DEV_ALLOW_DEBUG_CODES', 'False').lower() in ('1','true','yes')

# Session security
SESSION_IDLE_TIMEOUT = int(os.environ.get('SESSION_IDLE_TIMEOUT', '1800'))  # 30 minutes default
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True' if DJANGO_SECURE else 'False').lower() in ('1','true','yes')
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True' if DJANGO_SECURE else 'False').lower() in ('1','true','yes')
CSRF_USE_SESSIONS = True

# Minimum seconds between password reset code sends for the same identifier
PASSWORD_RESET_MIN_INTERVAL = int(os.environ.get('PASSWORD_RESET_MIN_INTERVAL', '60'))

# Logging: add a rotating file handler for password code logs to avoid unbounded growth.
LOG_DIR = BASE_DIR / 'logs'
PASSWORD_CODE_LOG = str(LOG_DIR / 'password_codes.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'password_codes_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PASSWORD_CODE_LOG,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        # Existing Django loggers keep defaults; add a dedicated logger for password codes
        'password_codes': {
            'handlers': ['password_codes_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
# ============================================================================
# IP GEOLOCATION & BLOCKING CONFIGURATION
# ============================================================================

# Enable/disable IP-based geolocation blocking
IP_BLOCKING_ENABLED = os.environ.get('IP_BLOCKING_ENABLED', 'True').lower() in ('true', '1', 'yes')

# IP addresses to whitelist (bypass geolocation checks)
IP_BLOCKING_WHITELIST = [
    '127.0.0.1',  # localhost
    '::1',  # IPv6 localhost
]

# URL paths to exclude from IP blocking
IP_BLOCKING_EXCLUDED_PATHS = [
    '/accounts/ip-blocked/',  # The blocked page itself
    '/api/health/',  # Health checks
    '/static/',  # Static files
    '/media/',  # Media files
    '/accounts/login/',  # Login page (for user redirect)
    '/accounts/register/',  # Registration
    '/api/password/reset/',  # Password reset APIs
    '/accounts/password-reset/',  # Password reset pages
    '/__debug__/',  # Django debug toolbar
]