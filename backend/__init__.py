from __future__ import absolute_import
import os

import redis
from flask_mail import Mail
from flask_migrate import Migrate

from backend import settings
from backend.app import create_app  # noqa

__version__ = "1.0.0"


redis_connection = redis.from_url(settings.REDIS_URL)
rq_redis_connection = redis.from_url(settings.RQ_REDIS_URL)
mail = Mail()
migrate = Migrate()
