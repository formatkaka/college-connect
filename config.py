from __init__ import *
import os


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://siddhant:collegeconnect@localhost:5432/mydb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pvokrejooerxqb:OK2EVuhUXYxoVtIdO_rfCz7Ev6@ec2-107-22-170-249.compute-1.amazonaws.com:5432/d8bgfga3qa0vu7'
db = SQLAlchemy(app)
api = Api(app)
app.config['SECRET_KEY'] = 's4df65a4g6aksdh<>?:.[],-.906^&#hcsddsf]!@#%^^^&*d[bjhv]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
auth = HTTPBasicAuth()