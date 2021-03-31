import datetime
import sys
import time
import json

from inspect import isclass
from funcy import project

from flask import Blueprint, current_app, request
from flask_login import current_user
from flask_restful import Resource, abort

import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import sort_query

from flask_jwt_extended import jwt_required

from backend import settings
from backend.utils import locales, json_dumps, app_log


routes = Blueprint("backend", __name__, template_folder=settings.fix_assets_path(
    "backend/templates"))


class CBaseResource(Resource):
    decorators = [jwt_required]

    def __init__(self, *args, **kwargs):
        super(CBaseResource, self).__init__(*args, **kwargs)
        self._user = None

    @property
    def log_cls(self):
        return f"{self.__class__.__name__} uid:{self.user_id}"

    @property
    def user_id(self):
        try:
            user_id_with_identity = self.login_user.get_id()
            if user_id_with_identity:
                user_id, _ = user_id_with_identity.split("-")
            else:
                app_log.error(f"user not found user:{user_id_with_identity}")
                user_id = 0
        except Exception:
            app_log.exception("user found failed")
            user_id = 0
        return user_id

    @property
    def login_user(self):
        return current_user._get_current_object()

    def serialize_time(self, column):
        if isinstance(column, datetime.datetime):
            return column.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(column, datetime.date):
            return column.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, column)

    def update_model(self, model, updates):
        b_set = False
        for k, v in updates.items():
            if v is None:
                continue
            if getattr(model, k, None) == v:
                continue
            b_set = True
            setattr(model, k, v)
        return b_set

    def clone_model(self, model):
        mapper = sqlalchemy.inspect(type(model))
        new_model = type(model)()
        for col in mapper.columns:
            if col.primary_key:
                continue
            setattr(new_model, col.key, getattr(model, col.key))
        new_model.user_id = self.user_id
        return new_model

    def order_by_field(self, query_set, model, sort_info):
        # data type transform
        if sort_info:
            try:
                sort_info = json.loads(sort_info)
            except Exception:
                sort_info = {}
        else:
            sort_info = {}

        # sort by field
        for field, order in sort_info.items():
            if not getattr(model, field, None):
                continue
            if order == "descend":
                query_set = query_set.order_by(getattr(model, field, None).desc())
            else:
                query_set = query_set.order_by(getattr(model, field, None).asc())
        return query_set


def require_fields(req, fields):
    if type(fields) not in (list, tuple, set):
        raise Exception("require_fields field type must be list or tuple or set")

    for f in fields:
        if f not in req:
            app_log.error("requir_fields field:%s not in %s" % (f, req))
            abort(400, message=locales.REQUEST_FIELD_MISS)


def permit_params(req, fields):
    return project(req, fields)


def get_object_or_404(fn, *args, **kwargs):
    try:
        rv = fn(*args, **kwargs)
        if rv is None:
            abort(404, message=locales.RESULT_FOUND_NONE)
    except NoResultFound:
        abort(404, message=locales.RESULT_NOT_FOUND)
    return rv


def paginate(query_set, page, page_size, serializer, **kwargs):
    count = query_set.count()

    if page < 1:
        abort(400, message=locales.RESULT_PAGE_INVALID)

    if (page - 1) * page_size + 1 > count > 0:
        abort(400, message=locales.RESULT_PAGE_LIMIT)

    if page_size > 250 or page_size < 1:
        abort(400, message=locales.RESULT_PAGE_SIZE_LIMIT)

    results = query_set.paginate(page, page_size)

    # support for old function based serializers
    if isclass(serializer):
        items = serializer(results.items, **kwargs).serialize()
    else:
        items = [serializer(result) for result in results.items]

    return {
        "count": count,
        "page": page,
        "pageSize": page_size,
        "data": items,
    }


def json_response(response):
    return current_app.response_class(json_dumps(response), mimetype="application/json")


def order_results(results, default_order, allowed_orders, fallback=True):
    """
    Orders the given results with the sort order as requested in the
    "order" request query parameter or the given default order.
    """
    # See if a particular order has been requested
    requested_order = request.args.get("order", "").strip()

    # and if not (and no fallback is wanted) return results as is
    if not requested_order and not fallback:
        return results

    # and if it matches a long-form for related fields, falling
    # back to the default order
    selected_order = allowed_orders.get(requested_order, None)
    if selected_order is None and fallback:
        selected_order = default_order

    # The query may already have an ORDER BY statement attached
    # so we clear it here and apply the selected order
    return sort_query(results.order_by(None), selected_order)
