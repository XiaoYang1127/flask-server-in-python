from flask import make_response
from flask_restful import Api
from werkzeug.wrappers import Response

from backend.utils import json_dumps
from backend.handlers import auth
from backend.handlers.users import CUserResource


class CApiExt(Api):

    def add_resource(self, resource, *urls, **kwargs):
        # TODO: check repeated url
        return super(CApiExt, self).add_resource(resource, *urls, **kwargs)


api = CApiExt()


def init_app(app):
    api.init_app(app)


@api.representation("application/json")
def json_representation(data, code, headers=None):
    # Flask-Restful checks only for flask.Response but flask-login uses werkzeug.wrappers.Response
    if isinstance(data, Response):
        return data

    resp = make_response(json_dumps(data), code)
    resp.headers.extend(headers or {})
    return resp


# user api
api.add_resource(CUserResource, "/api/v1/user", endpoint="users")
