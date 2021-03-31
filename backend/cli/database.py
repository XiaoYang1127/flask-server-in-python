import time

from click import argument, option
from flask.cli import AppGroup
from flask_migrate import stamp

import sqlalchemy
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import select
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine


manager = AppGroup(help="Manage the database (create/drop tables.).")


def _wait_for_db_connection(db):
    retried = False
    while not retried:
        try:
            db.engine.execute("SELECT 1;")
            return
        except DatabaseError:
            time.sleep(3)

        retried = True


@manager.command()
def rebuild_tables():
    drop_tables()
    create_tables()


@manager.command()
def create_tables():
    """Create the database tables."""
    from backend.models import db

    _wait_for_db_connection(db)
    # To create triggers for searchable models, we need to call configure_mappers().
    sqlalchemy.orm.configure_mappers()
    db.create_all()

    # Need to mark current DB as up to date
    stamp()


@manager.command()
def drop_tables():
    """Drop the database tables."""
    from backend.models import db

    _wait_for_db_connection(db)

    db.drop_all()
