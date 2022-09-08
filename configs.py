# 数据库的配置变量
from datetime import timedelta

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'secret'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = 'XXXXXXXXXX@qq.com'
MAIL_PASSWORD = 'XXXXXXXXXX'
MAIL_DEFAULT_SENDER = 'XXXXXXXXXX@qq.com'

# 会话
SECRET_KEY = 'dAiwfUfXdqrapsGmNm,uZBj*=^!Z)m72'
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
