import datetime

from flask import request, make_response, redirect
from flask_restful import abort
from flask_login import login_user, logout_user

from backend import models
from backend.utils import locales, app_log
from backend.authentication import jwt_auth, get_login_url
from backend.handlers.base import (
    routes,
    require_fields,
)


@routes.route("/ping", methods=["GET"])
def ping():
    return f"pong {datetime.datetime.now()}"


@routes.route("/api/v1/register", methods=["POST"])
def register_user():
    req_dict = request.get_json(True)
    name = req_dict.get("name", "")
    email = req_dict.get("email", "")
    password = req_dict.get("password", "")

    # check params
    if not name:
        errno = locales.USER_NAME_INVALID
        app_log.error("register_user %s %s" % (errno, req_dict))
        abort(400, message=errno)

    if not email:
        errno = locales.USER_EMAIL_INVALID
        app_log.error("register_user %s %s" % (errno, req_dict))
        abort(400, message=errno)

    if not password:
        errno = locales.USER_PASSWORD_INVALID
        app_log.error("register_user %s %s" % (errno, req_dict))
        abort(400, message=errno)

    # add new model
    try:
        user_model = models.CUser(
            name=name,
            email=email,
        )
        user_model.hash_password(password)
        models.db.session.add(user_model)
        models.db.session.commit()
        app_log.log(f"{name}:{email} register success")
    except Exception as e:
        app_log.exception("register_user failed %s" % (str(e)))
        abort(400, message=locales.MODEL_ADD_FAILED)

    return make_response("", 204)


@routes.route("/api/v1/login", methods=["POST"])
def login():
    req_dict = request.get_json(True)
    require_fields(req_dict, [
        "email", "password"
    ])

    email = req_dict.get("email", "")
    password = req_dict.get("password", "")

    user_model = models.CUser.get_by_email(email)
    if user_model and user_model.verify_password(password):
        login_user(user_model)
        app_log.info(f"uid:{user_model.id} email:{user_model.email} login success")
        return jwt_auth.jwt_token_for(user_model)
    else:
        abort(401, message=locales.USER_PASSWORD_WRONG)


@routes.route("/api/v1/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(get_login_url())


@routes.route("/api/v1/reset_password", methods=["POST"])
def reset_password():
    abort(404, message=locales.REQUEST_METHOD_NOTIMPLEMENTED)


@routes.route("/api/v1/forget_password", methods=["POST"])
def forget_password():
    abort(404, message=locales.REQUEST_METHOD_NOTIMPLEMENTED)
