from __init__ import *
import os
from flask_mail import Mail
# from thread_app import MyThread
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/databse'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://siddhant:collegeconnect@localhost:5432/db7'


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://icogkawnroahpr:c22UCPudryC5xAmpqE9jjNWz37@ec2-204-236-226-63.compute-1.amazonaws.com:5432/dat3mrlsck6nk7'
db = SQLAlchemy(app)
api = Api(app)
mail = Mail(app)
app.config['SECRET_KEY'] = 's4df65a4g6aksdh<>?:.[],-.906^&#hcsddsf]!@#%^^^&*d[bjhv]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 2
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'college.connect01@gmail.com'
app.config['MAIL_PASSWORD'] = 'collegeconnect1234'
# app.config['MAIL_USERNAME'] = 'college.connect28@gmail.com'
# app.config['MAIL_PASSWORD'] = 'collegeconnect1234'
mail = Mail(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# from main import cron
# from threading import Thread

# class MyThread(object):
#     def __init__(self, app,tar):
#
#         self.app = app
#         self.__thread = Thread(target=tar, args=())
#
#
#     def start_thread(self):
#         self.__thread.start()

bootstrap = Bootstrap(app)



