

def init_app(app):
    from backend.handlers.api import api
    from backend.handlers.base import routes

    app.register_blueprint(routes)
    api.init_app(app)
