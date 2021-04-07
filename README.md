# flask-server-in-python

## 简单介绍

### flask

- https://dormousehole.readthedocs.io/en/stable/

### flask-sqlalchemy

- http://www.pythondoc.com/flask-sqlalchemy/quickstart.html

### flask-migrate

- 使用 Alembic 处理 Flask 应用程序的 SQLAlchemy 数据库迁移的扩展
- https://flask-migrate.readthedocs.io/en/latest/

### flask-login

- 提供 Flask 的用户会话管理。它处理登录，注销和记住用户会话的常见任务
- https://flask-login.readthedocs.io/en/stable/

### flask-jwt-extended

- https://flask-jwt-extended.readthedocs.io/en/stable/

### flask-mail

- 可以在 Flask 应用中设置 SMTP 使得可以发送邮件信息
- http://www.pythondoc.com/flask-mail/

### flask-talisman

- 处理设置 HTTP 标头的过程，这些标头可以帮助防止一些常见的 Web 应用程序安全性问题
- https://pypi.org/project/flask-talisman/

### flask-limiter

- 提供速率限制功能。它支持使用内存，redis 和 memcache 的当前实现进行存储的可配置后端
- 可基于 ip 限制单个时间内访问次数，用于拦截恶意的浏览器请求
- https://flask-limiter.readthedocs.io/en/stable/

### flask-cors

- 用于处理跨源资源共享（CORS），使得跨源 AJAX 成为可能
- https://flask-cors.readthedocs.io/en/latest/

## 快速上手

- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- 启动项目
  - flask run

## 部署方式

### gunicorn + gevent

- gunicorn -c gunicorn.py backend.wsgi:app

### python + gevent

- python main.py pro

### 开发模式

- python main.py dev
