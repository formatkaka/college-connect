from __init__ import *
import os
from flask_mail import Mail

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://siddhant:collegeconnect@localhost:5432/databasecc'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pvokrejooerxqb:OK2EVuhUXYxoVtIdO_rfCz7Ev6@ec2-107-22-170-249.compute-1.amazonaws.com:5432/d8bgfga3qa0vu7'
db = SQLAlchemy(app)
api = Api(app)
mail = Mail(app)
app.config['SECRET_KEY'] = 's4df65a4g6aksdh<>?:.[],-.906^&#hcsddsf]!@#%^^^&*d[bjhv]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'college.connect28@gmail.com'
app.config['MAIL_PASSWORD'] = 'collegeconnect1234'
# app.config['MAIL_USERNAME'] = 'college.connect28@gmail.com'
# app.config['MAIL_PASSWORD'] = 'collegeconnect1234'
mail = Mail(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
