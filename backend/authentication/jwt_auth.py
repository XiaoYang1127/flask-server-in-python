import datetime

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    decode_token
)


def init_app(app):
    app.config['JWT_SECRET_KEY'] = 'jwt_token_for'
    JWTManager(app)


def jwt_token_for(user):
    identity = {
        'email': user.email
    }

    access_token = create_access_token(
        identity=identity,
        expires_delta=datetime.timedelta(days=1)
    )
    refresh_token = create_refresh_token(identity=identity)

    return {
        'email': identity,
        'access_token': access_token,
        'refresh_token': refresh_token,
    }


def jwt_decode_token(encoded_token, csrf_value=None, allow_expired=False):
    return decode_token(encoded_token, csrf_value, allow_expired)
