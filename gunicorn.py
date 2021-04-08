import os
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

name = "backend"
debug = True
loglevel = "debug"
bind = "0.0.0.0:8080"
pidfile = "logs/gunicorn.pid"
# accesslog = "logs/access.log"
# errorlog = "logs/error.log"

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gunicorn.workers.ggevent.GeventWorker"
# worker_class = "gevent"

worker_connections = 1000
max_requests = 1000
max_requests_jitter = 10
threads = 5
preload_app = True
reload = True

x_forwarded_for_header = "X-FORWARDED-FOR"
