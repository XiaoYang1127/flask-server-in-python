from flask import request, make_response
from flask_restful import abort

from backend import models
from backend.utils import locales, app_log
from backend.authentication.jwt_auth import jwt_token_for
from backend.handlers.base import (
    CBaseResource,
    require_fields,
    permit_params,
    paginate,
)


class CUserResource(CBaseResource):

    # ============================================================================================== #
    #                                           get                                                  #
    # ============================================================================================== #

    def get(self):
        method = request.args.get("method", "")
        func = getattr(CUserResource, method, None)
        if not func:
            app_log.error("%s get method:%s undefined" % (self.log_cls, method))
            abort(404, message=locales.HTTP_GET_UNDEFINED)

        return func(self)

    def user_detail(self, user_id):
        user_model = models.CUser.get_by_id(user_id)
        if not user_model:
            app_log.error("%s user_details %s not found" % (self.log_cls, user_id))
            abort(400, message=locales.USER_NOT_FOUND)

        return user_model.serialize_detail()

    def user_list(self):
        query_set = models.CUser.query.filter()

        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", 20, type=int)
        sort_info = request.args.get("sorter", {})
        query_set = self.order_by_field(query_set, models.CUser, sort_info)

        return paginate(query_set, page, page_size, lambda f: f.serialize_list())

    # ============================================================================================== #
    #                                           post                                                 #
    # ============================================================================================== #

    def post(self):
        req_dict = request.get_json(True)
        method = req_dict.get("method", "")
        func = getattr(CUserResource, method, None)
        if not func:
            app_log.error("%s post method:%s not found" % (self.log_cls, method))
            abort(404, message=locales.HTTP_POST_UNDEFINED)

        return func(self, req_dict)

    def update_user(self, req_dict):
        req_dict = permit_params(req_dict, [
            "user_id", "name",
        ])

        user_id = req_dict.pop("user_id", None)
        name = req_dict.get("name", "")

        # check params
        if not name:
            errno = locales.USER_NAME_INVALID
            app_log.error("%s update_user %s %s" %
                          (self.log_cls, errno, req_dict))
            abort(400, message=errno)

        user_model = models.CUser.get_by_id(user_id)
        if not user_model:
            errno = locales.USER_NOT_FOUND
            app_log.error("%s update_user %s %s" %
                          (self.log_cls, errno, req_dict))
            abort(400, message=errno)

        # update model
        try:
            b_set = self.update_model(user_model, req_dict)
            if b_set:
                models.db.session.commit()
        except Exception as e:
            app_log.exception("%s update_user failed %s" % (self.log_cls, str(e)))
            abort(400, message=locales.MODEL_UPDATE_FAILED)

        return user_model.serialize_simple()

    def delete_user(self, req_dict):
        user_id = req_dict.get("user_id", None)

        user_model = models.CUser.get_by_id(user_id)
        if not user_model:
            app_log.error("%s delete_user %s not found" % (self.log_cls, user_id))
            abort(400, message=locales.USER_NOT_FOUND)

        try:
            models.db.session.delete(user_model)
            models.db.session.commit()
        except Exception as e:
            app_log.exception("%s delete_user failed %s" % (self.log_cls, str(e)))
            abort(400, message=locales.MODEL_DELETE_FAILED)

        return make_response("", 204)
