from __init__ import *
from config import *
from models import *

from schemas import *
from opschemas import *


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
			
			op = UserReg_class(200,user.userName,token)
			result = userreg_schema.dump(op)


			return result.data

		elif not UserReg.if_username_unique(username) :					# Return error if username not unique
			return jsonify({"Status":"Username not unique"})


	def get(self):
		""" Obtain/Generate token for user """

		user = get_current_user()

		if user.check_password_hash(user.password_hash):
			return jsonify({"Token":user.gen_auth_token()})


arr = ["info","clubs","events"]

class UserInformation(Resource):
	""" API to POST and GET user info """

	def post(self,s):

		user = get_current_user()
		user_id = user.id
		if user:
			json_data = request.get_json()
			data, errors = info_schema.load(json_data)
			if errors :
				return jsonify(errors)
			else :
				
				stat,val = UserInfo.if_unique(data['rollno'],data['email'],data['mobno'])
				if not stat:
					return ({"Status":"{0} already reg.".format(val)})
				else :
					if UserInfo.save_info(data['name'],data['rollno'],data['email'],data['mobno'],user_id):
						return ({"Status":"Information saved."})
					else :
						return ({"Status":"Some error occured."})

		else :
			return ({"Status":"Invalid User."})	


	def get(self,s):
		user = get_current_user()
		if user:
			if s in arr:
				if s == arr[0]:

					info = get_user_info(user)
					op = UserInfo_P_class(200,info.fullName,info.rollNo,info.emailId,info.mobNo)
					result = userinfo_p_schema.dump(op)
					return result.data

				elif s == arr[1]:
					
					myclubs = get_user_club(user)
					op = Nested_output(200,myclubs)
					result = userinfo_c_schema.dump(myclubs)
					return result.data
					


				elif s == arr[2]:
					pass

			else :
				return jsonify({"Status":'Invalid request'})
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
				event = EventsReg.register_one(data['name'],data['about'],

											   data['seats'],
											   data['venue'],
											   user.id)
				if user_is_admin(user):
					event.verified = True
				elif not user_is_admin(user):
					event.verified = False
				else :
					return jsonify({"Status":"Some error occured"})

				event.add_contacts(data['contacts'])
				return jsonify({"Status":"Event Saved"})

		else :
			return jsonify({"Status":"Unauthorized access"})


class Clubsget(Resource):
	def get(self):
		user = get_current_user()
		if user:
			clubs = ClubInfo.query.all()

api.add_resource(UserRegistration,'/api/user/reg')
api.add_resource(UserInformation,'/api/user/<string:s>')
api.add_resource(EventRegistration,'/api/events')
api.add_resource(Clubsget,'/clubs/')

if __name__ == "__main__":
	db.create_all()
	app.run(port=5080,debug=True)

