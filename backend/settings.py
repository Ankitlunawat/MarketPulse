import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = os.environ.get("SECRET_KEY", "local-demo-only-change-before-deployment")
DEBUG = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth", "rest_framework", "tracker"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware"]
ROOT_URLCONF = "urls"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
if os.environ.get("PGDATABASE"):
    DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": os.environ["PGDATABASE"], "USER": os.environ["PGUSER"], "PASSWORD": os.environ["PGPASSWORD"], "HOST": os.environ.get("PGHOST","localhost"), "PORT": os.environ.get("PGPORT","5432")}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"]}
