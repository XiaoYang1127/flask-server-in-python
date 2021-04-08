import sys


APP_HOST = "0.0.0.0"
APP_PORT = 8080

RUN_DEVELOPMENT = "dev"
RUN_PRODUCTION = "pro"
RUN_ALL = {RUN_DEVELOPMENT, RUN_PRODUCTION}


def run_in_development():
    from backend import settings, create_app

    app = create_app()

    # update config
    options = {
        "host": APP_HOST,
        "port": APP_PORT,
        "debug": True,
    }

    # multi-process or multi-thread
    if settings.DEPLOY_PROCESSES:
        options["processes"] = settings.DEPLOY_PROCESSES
    elif settings.DEPLOY_THREADED:
        options["threaded"] = True

    app.run(**options)


def run_in_production():
    from gevent.pywsgi import WSGIServer
    from gevent import monkey

    monkey.patch_all()

    from backend import create_app

    app = create_app()
    server = WSGIServer((APP_HOST, APP_PORT), app)
    server.serve_forever()


def run_in_production2():
    from wsgiref.simple_server import make_server
    from backend import create_app

    app = create_app()
    server = make_server(APP_HOST, APP_PORT, app)
    server.serve_forever()


if __name__ == "__main__":
    args = sys.argv
    if len(args) <= 1:
        print("need a param in %s" % RUN_ALL)
        exit(0)

    if args[1] == RUN_DEVELOPMENT:
        run_in_development()

    elif args[1] == RUN_PRODUCTION:
        run_in_production()

    else:
        print("param not in %s" % RUN_ALL)
