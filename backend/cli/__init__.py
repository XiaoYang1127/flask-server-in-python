import click
import simplejson
from flask import current_app
from flask.cli import FlaskGroup, run_command

from backend import __version__, settings
from backend.app import create_app
from backend.cli import (
    database,
    users,
)


def create(group):
    app = current_app or create_app(from_shell=True)
    group.app = app

    @app.shell_context_processor
    def shell_context():
        from backend import models, settings

        return {"models": models, "settings": settings}

    return app


@click.group(cls=FlaskGroup, create_app=create)
def manager():
    """Management script"""


manager.add_command(database.manager, "database")
manager.add_command(users.manager, "users")
manager.add_command(run_command, "runserver")


@manager.command()
def version():
    print(__version__)


@manager.command()
def check_settings():
    for name, item in current_app.config.items():
        print("{} = {}".format(name, item))


@manager.command()
@click.argument("email", default=settings.MAIL_DEFAULT_SENDER, required=False)
def send_test_mail(email=None):
    from backend import mail
    from flask_mail import Message

    if email is None:
        email = settings.MAIL_DEFAULT_SENDER

    mail.send(
        Message(
            subject="Test Message",
            recipients=[email],
            body="Test message."
        )
    )


@manager.command()
def ipython():
    """Starts IPython shell instead of the default Python shell."""
    import sys
    import IPython
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    banner = "Python %s on %s\nIPython: %s\n version: %s\n" % (
        sys.version,
        sys.platform,
        IPython.__version__,
        __version__,
    )

    ctx = {}
    ctx.update(app.make_shell_context())
    IPython.embed(banner1=banner, user_ns=ctx)
