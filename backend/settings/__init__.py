import os
import os.path

from .helpers import (
    fix_assets_path,
    parse_boolean,
    int_or_none,
    add_decode_responses_to_redis_url,
)


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

LOG_PATH = os.environ.get("LOG_PATH", f"{ROOT_DIR}/logs")
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

STATIC_ASSETS_PATH = fix_assets_path(
    os.environ.get("STATIC_ASSETS_PATH", "client/dist/")
)

HOST = os.environ.get("HOST", "localhost")


# database
POSTGRES_URL = "postgresql:///postgres"
MYSQL_URL = "mysql+pymysql://root:mxworld2006999@localhost:3306/flask_test"
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URL", MYSQL_URL)
SQLALCHEMY_MAX_OVERFLOW = int_or_none(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", 100))
SQLALCHEMY_POOL_SIZE = int_or_none(os.environ.get("SQLALCHEMY_POOL_SIZE", 100))
SQLALCHEMY_POOL_RECYCLE = int_or_none(os.environ.get("SQLALCHEMY_POOL_RECYCLE", 30 * 60))
SQLALCHEMY_POOL_TIMEOUT = int_or_none(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", 5))
SQLALCHEMY_DISABLE_POOL = parse_boolean(os.environ.get("SQLALCHEMY_DISABLE_POOL", "false"))
SQLALCHEMY_ENABLE_POOL_PRE_PING = parse_boolean(
    os.environ.get("SQLALCHEMY_ENABLE_POOL_PRE_PING", "false"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False


# redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_USER = os.environ.get("REDIS_USER", "root")
REDIS_PASS = os.environ.get("REDIS_PASS", "mxworld2006999")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)
REDIS_URL_DEFAULT = f"redis://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
REDIS_URL = os.environ.get("REDIS_URL", REDIS_URL_DEFAULT)
REDIS_URL = add_decode_responses_to_redis_url(REDIS_URL)
RQ_REDIS_URL = os.environ.get("RQ_REDIS_URL", REDIS_URL)
PROXIES_COUNT = int(os.environ.get("REDASH_PROXIES_COUNT", "1"))


# mail
MAIL_SERVER = os.environ.get("MAIL_SERVER", os.environ.get("MAIL_HOST", "smtp.qq.com"))
MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
MAIL_USE_TLS = parse_boolean(os.environ.get("MAIL_USE_TLS", "true"))  # 587
MAIL_USE_SSL = parse_boolean(os.environ.get("MAIL_USE_SSL", "false"))  # 465
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")  # the authorization code of email
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "")  # your email address
MAIL_MAX_EMAILS = os.environ.get("MAIL_MAX_EMAILS", 5000)
MAIL_ASCII_ATTACHMENTS = parse_boolean(os.environ.get("MAIL_ASCII_ATTACHMENTS", "false"))


# deploy
DEPLOY_THREADED = parse_boolean(os.environ.get("DEPLOY_THREADED", "true"))
DEPLOY_PROCESSES = int(os.environ.get("DEPLOY_PROCESSES", 1))
