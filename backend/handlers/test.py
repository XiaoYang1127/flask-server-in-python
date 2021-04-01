import datetime

from flask import request, make_response, redirect
from flask_login import current_user
from flask_restful import abort

from backend import limiter
from backend.handlers.base import routes


@routes.route("/test_ping1", methods=["GET"])
@limiter.limit("100/day")
@limiter.limit("10/hour")
@limiter.limit("1/minute")
def test_ping1():
    return f"test_pong1 {datetime.datetime.now()}"


@routes.route("/test_ping2")
@limiter.limit("100/day", exempt_when=lambda: current_user.is_admin)
def test_ping2():
    """满足给定条件时，可以免除每个限制"""
    return f"test_pong2 {datetime.datetime.now()}"
