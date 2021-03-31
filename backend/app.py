import os
import redis

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

from backend import settings
from backend.utils import log, app_log


class CMyApp(Flask):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "template_folder": settings.STATIC_ASSETS_PATH,
                "static_folder": settings.STATIC_ASSETS_PATH,
                "static_url_path": "/static",
            }
        )
        super(CMyApp, self).__init__(__name__, *args, **kwargs)
        # Make sure we get the right referral address even behind proxies like nginx.
        self.wsgi_app = ProxyFix(self.wsgi_app, x_for=settings.PROXIES_COUNT, x_host=1)
        # Configure Redash using our settings
        self.config.from_object("backend.settings")


def create_app(from_shell=False):
    from backend import (
        authentication,
        handlers,
        migrate,
        mail,
    )
    from backend.models.base import db

    # base init
    log.setup_logging(logName="app.log")

    # application init
    app = CMyApp()
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    app.before_first_request(before_first_request)

    authentication.init_app(app)
    handlers.init_app(app)

    return app


def before_first_request():
    app_log.info("recv first request")
