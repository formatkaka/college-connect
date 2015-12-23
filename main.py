from __init__ import *
from config import *
from models import *

from schemas import *

class UserRegistration(Resource):
	""" API to register a new user or obtain token for a user"""

	def post(self):
		""" Register a user """

		user = request.authorization
		username = user.username
		password_hash = user.password

		if username is None:                           # Check if any of auth headers are empty
			return jsonify({"Status":"Username field empty"})

		if password_hash is None:
			return jsonify({"Status":"Password field empty"})

		if UserReg.if_username_unique(username):							# Check if the username is unique.If unique , register the user
			user = UserReg.register_user(username,password_hash)			# and return the auth token generated fot the user with its id
			token = user.gen_auth_token()
			return jsonify({"token":token})

		elif not UserReg.if_username_unique(username) :					# Return error if username not unique
			return jsonify({"Status":"Username not unique"})


	def get(self):
		""" Obtain/Generate token for user """

		user = get_current_user()

		if user.check_password_hash(user.password_hash):
			return jsonify({"Token":user.gen_auth_token()})

class UserInformation(Resource):
	""" API to POST and GET user info """

	def post(self): 
		user = get_current_user()
		user_id = user.id
		if user:
			json_data = request.get_json()
			data, errors = info_schema.load(json_data)
			if errors :
				return jsonify(errors)
			else :
				
				stat,val = UserInfo.if_unique(data['rollno'],data['mobno'],data['email'])
				if not stat:
					return ({"Status":"{0} already reg.".format(val)})
				else :
					if UserInfo.save_info(data['name'],data['rollno'],data['mobno'],data['email'],user_id):
						return ({"Status":"Information saved."})
					else :
						return ({"Status":"Some error occured."})

		else :
			return ({"Status":"Invalid User."})	
	
	def get(self):
		user = get_current_user()
		if user:
			info = get_user_info(user)
			return jsonify({"name":info.fullName,"rollno":info.rollNo,"mobno":info.mobNo,"email":info.emailId})
		else :
			return jsonify({"Status":"Invalid"})





class EventRegistration(Resource):
	def post(self):
		user = get_current_user()
		if user:
			json_data = request.get_json()
			data, errors = event_schema.load(json_data)
			if errors :
				return jsonify(errors)
			else :



		else :
			return jsonify({"Status":"Unauthorized access"})
	

api.add_resource(UserRegistration,'/')
api.add_resource(UserInformation,'/info')

if __name__ == "__main__":
	db.create_all()
	app.run(port=6080,debug=True)
