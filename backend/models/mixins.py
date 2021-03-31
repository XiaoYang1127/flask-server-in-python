import datetime
import json

from sqlalchemy.event import listens_for

from backend.models.base import db, Column


class CTimestampMixin(object):
    created_at = Column(db.DateTime(True), default=db.func.now())
    updated_at = Column(db.DateTime(True), default=db.func.now())

    def serialize_time(self, column):
        if isinstance(column, datetime.datetime):
            return column.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(column, datetime.date):
            return column.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, column)


@listens_for(CTimestampMixin, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    if hasattr(target, "skip_updated_at"):
        return
    target.updated_at = db.func.now()


class CQueryMixin(object):

    @classmethod
    def get_by_id(cls, object_id):
        query = cls.query.filter(cls.id == object_id)
        return query.first()

    @classmethod
    def get_by_name(cls, object_name):
        query = cls.query.filter(cls.name == object_name)
        return query.first()

    @classmethod
    def get_by_uid(cls, user_id):
        query = cls.query.filter(cls.user_id == user_id)
        return query.first()
