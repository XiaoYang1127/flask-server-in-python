from __future__ import absolute_import
import os

import redis
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from backend import settings
from backend.app import create_app  # noqa

__version__ = "1.0.0"


redis_connection = redis.from_url(settings.REDIS_URL)
rq_redis_connection = redis.from_url(settings.RQ_REDIS_URL)


mail = Mail()
migrate = Migrate()
cors = CORS()
talisman = Talisman(force_https=False)
limiter = Limiter(key_func=get_remote_address)  # limit request count by remote ip address
