from sys import exit
import yaml
import os

from click import BOOL, argument, option, prompt
from flask.cli import AppGroup
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from backend import models
from backend.settings import ROOT_DIR


manager = AppGroup(help="Users management commands.")


@manager.command()
def init():
    """init user from fake data"""
    base_path = "%s/data/" % ROOT_DIR
    file_path = os.path.join(base_path, 'fake/data_user.yml')
    fp = open(file_path, 'r', encoding='utf-8')
    data = yaml.safe_load(fp.read())
    for users in data.values():
        for user in users:
            create(user["email"], user["name"], user["password"])


@manager.command()
@argument("email")
@argument("name")
@option(
    "--password",
    "password",
    default="123456",
    help="user login password, default is 123456.",
)
def create_user(email, name, password="123456"):
    """create user from input parameters"""
    create(email, name, password)


def create(email, name, password):
    print("creating user (%s, %s)...\n\n" % (email, name,))

    user = models.CUser(
        name=name,
        email=email,
    )
    user.hash_password(password)

    try:
        models.db.session.add(user)
        models.db.session.commit()
    except Exception as e:
        print("Failed creating user: %s" % e)
        exit(1)


@manager.command(name="list")
def list_command(organization=None):
    """List all users"""

    users = models.User.query
    for i, user in enumerate(users.order_by(models.User.name)):
        if i > 0:
            print("-" * 20)
            print("\n")

        print("id: {}\nname: {}\nemail: {}\n".format(
            user.id,
            user.name,
            user.email,
        ))
