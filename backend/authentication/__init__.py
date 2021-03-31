import hashlib
import hmac
import logging
import time
from urllib.parse import urlsplit, urlunsplit

from flask import jsonify, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, user_logged_in
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized

from backend import models, settings
from backend.utils import app_log

from .jwt_auth import jwt_decode_token, init_app as jwt_init_app


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id_with_identity):
    try:
        user_id, _ = user_id_with_identity.split("-")
        user = models.User.get_by_id(user_id)
        if user.get_id() != user_id_with_identity:
            return None
        return user
    except (NoResultFound, ValueError, AttributeError):
        return None


def get_login_url(external=False, next="/"):
    return url_for("backend.login", next=next, _external=external)


@login_manager.unauthorized_handler
def redirect_to_login():
    if request.is_xhr or "/api/" in request.path:
        response = jsonify({"message": "Couldn't find resource. Please login and try again."})
        response.status_code = 404
        return response

    login_url = get_login_url(next=request.url, external=False)
    return redirect(login_url)


def load_user_from_jwt_token(token, csrf_value):
    try:
        data = jwt_decode_token(token, csrf_value=csrf_value)
        identity = data.get('identity', {})
        email = identity.get('email', None)
        user = models.User.get_by_email(email)
        if user:
            return user
        else:
            return None
    except Exception:
        return None


def request_loader(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None

    token_type = auth_headers[0].lower()
    token = auth_headers[1]
    if not token or token == 'null':
        return None

    if token_type == 'bearer':
        csrf_value = request.headers.get('csrf_token')
        return load_user_from_jwt_token(token, csrf_value)
    else:
        return None


def log_user_logged_in(app, user):
    event = {
        "action": "login",
        "timestamp": int(time.time()),
        "ip": request.remote_addr,
        "user_id": user.id,
        "user_agent": request.user_agent.string,
    }
    app_log.info(f"log_user_logged_in {event}")


def init_app(app):
    jwt_init_app(app)
    login_manager.init_app(app)
    login_manager.anonymous_user = models.CAnonymousUser

    user_logged_in.connect(log_user_logged_in)
    login_manager.request_loader(request_loader)
