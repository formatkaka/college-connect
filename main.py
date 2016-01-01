from __init__ import *
from config import *
from models import *
import os,flask,scrap

from schemas import *
from opschemas import *

class Testing(Resource):
	"""Test Class for API"""

	def get(self):
		hello = '<h1>It Works!</h1>'
		response = flask.make_response(hello)
		response.headers['content-type'] = 'text/html'
		return response

class UserRegistration(Resource):
	""" API to register a new user or obtain token for a user"""

	def post(self):
		""" Register a user """

		user = request.authorization
		if not user:
			return jsonify({"Status":"Empty payload"})

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

		if user is False:
			return jsonify({"Status":"Dont shit here."})

		if user:
			token = user.gen_auth_token()
			
			op = UserReg_class(200,user.userName,token)
			result = userreg_schema.dump(op)
			return result.data
		
		else:# if user.check_password_hash(user.password_hash):
			return jsonify({"Status":"Unauthorized"})





class UserInformation(Resource):
	""" API to POST and GET user info """

	def post(self,s):

		user = get_current_user()
		user_id = user.id
		if user:
			if s == "profile":
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
		arr = ["profile","myclubs","myevents","attending","followed"]
		if user:
			if s in arr:
				if s == arr[0]:   # Get current user profile

					info = get_user_info(user)
					op = UserInfo_class(200,info.fullName,info.rollNo,info.emailId,info.mobNo)
					result = userinfo_schema.dump(op)
					return result.data

				elif s == arr[1]: # Get a list of clubs the user is admin of.
					
					myclubs = get_user_club(user)
					op = Nested_output(200,myclubs)
					result = userinfo_schema.dump(myclubs)
					return result.data
					


				elif s == arr[2]: # Get a list of event submitted by a user.
					pass

				elif s == arr[3]: # Get a list of events the user wants to attend.
					pass

				elif s == arr[4]: # Get a list of clubs followed by user.
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
				event = EventsReg.register_one(data['name'],
											   data['about'],
											   data['seats'],
											   data['venue'],
											   conv_time(data['sdt']),
											   conv_time(data['edt']),
											   user.id)
				if user_is_admin(user):
					event.verified = True
				elif not user_is_admin(user):
					event.verified = False
				else :
					return jsonify({"Status":"Some error occured"})

				if event.add_contacts(data['contacts']):
					event.set_active()
					return jsonify({"Status":"Event Saved"})

		else :
			return jsonify({"Status":"Unauthorized access"})

	def get(self):
		user = get_current_user()
		if user:
			pass


class Clubsget(Resource):
	
	def get(self,s1,s2):
		user = get_current_user()
		if user:
			if s1 == "list":

				clubs_list = ClubInfo.query.all()

				clubs = []
				for club in clubs_list:
					admins = get_admin_info(club)
					c = Club_class(club.clubName,club.aboutClub,admins)
					clubs.append(c)

				return {"clubs":club_schema.dump(clubs)}
				
			elif s2 == "info" and club :
				result = userinfo_c_schema.dump(club)
				return result.data
			# elif s2 == "events" and club :
			# 	result = 
		# else:
		# 	return Error04









sources = ["notice", "seminar", "quick"]

class WebScrap(Resource):
	def get(self, source):
		scrapper = scrap.Scrap()
		if source == sources[0]:
			return jsonify(scrapper.get_notice())
		elif source == sources[1]:
			return jsonify(scrapper.get_seminar())
		elif source == sources[2]:
			return jsonify(scrapper.get_quicks())
		else:
			return jsonify({"Status":'Invalid request'})



api.add_resource(UserRegistration,'/api/user/reg')
api.add_resource(UserInformation,'/api/user/<string:s>')
api.add_resource(EventRegistration,'/api/events')
api.add_resource(Clubsget,'/api/clubs/<string:s1>/<string:s2>')
api.add_resource(Testing,'/')
api.add_resource(WebScrap,'/api/scrap/<string:source>')

if __name__ == "__main__":
	db.create_all()
	# port = int(os.environ.get('PORT', 5432))
	# app.run(host='0.0.0.0', port=port, debug=True)
	app.run(port=7080,debug=True)
