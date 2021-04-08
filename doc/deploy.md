# 如何支持高并发部署

## 从 flask 本身来讲

- 多线程方式

  - app.run(`threaded`=True)
  - param `threaded`: should the process handle each request in a separate thread?

- 多进程方式
  - app.run(`processes`=True)
  - param `processes`: if greater than 1 then handle each request in a new process up to this maximum number of concurrent processes.

## 从部署，gunicorn + gevent 方式

- reference: https://blog.igevin.info/posts/how-to-deploy-flask-apps/
- gunicorn -c gunicorn.py backend.wsgi:app

### 从代码，gevent 方式

- python main.py pro
- python main.py dev
