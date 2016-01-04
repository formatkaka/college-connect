from __init__ import *
from config import *
from models import *
import os,flask,scrap
from flask.ext.mail import Message
from flask_mail import Message
import base64

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
		json_data = request.get_json()
		data, errors = info_schema.load(json_data)


		if username is None:                           # Check if any of auth headers are empty
			return jsonify({"Status":"Username field empty"})

		if password_hash is None:
			return jsonify({"Status":"Password field empty"})

		if errors :
			return jsonify(errors)



		stat,val = UserReg.if_unique(data['rollno'],data['email'],data['mobno'])
		email_id = data["email"]

		if not stat:
			return ({"Status":"{0} already reg.".format(val)})
		else :
				
			user_1 = UserReg(userName=username,passwordHash=password_hash,fullName=data['name']
							,rollNo=data['rollno'],emailId=data['email'],mobNo=data['mobno'])
			db.session.add(user_1)
			db.session.commit()

			recieve = "sid.siddhant.loya@gmail.com"
			token = user_1.gen_auth_token()								# TODO : Report if info commit fails
			op = UserReg_class(200,user_1.userName,token)
			result = userreg_schema.dump(op)

			link = 'http://0.0.0.0:8080/api/verify/' + base64.b64encode(email_id)

			msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
				sender = "siddhantloya2008@gmail.com",
				recipients = [recieve])

			msg.body = "please click on the link {0}".format(link)
			mail.send(msg)

			return "result.data"



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
		
		else:
			return jsonify({"Status":"Unauthorized"})


class UserInformation(Resource):
	""" API to GET user info """

	# def post(self,s):
	# 	return ({"Status":"Invalid Method."})	

	# arr = ["profile","myclubs","myevents","attending","followed"]

	# def get(self,s):
	# 	user = get_current_user()
	# 	arr = self.arr
	# 	if user:

	# 		if s == "profile":
	# 			json_data = request.get_json()
	# 			data, errors = info_schema.load(json_data)
	# 			if errors :
	# 				return jsonify(errors)
	# 			else :
					
	# 				stat,val = UserInfo.if_unique(data['rollno'],data['email'],data['mobno'])
	# 				if not stat:
	# 					return ({"Status":"{0} already reg.".format(val)})
	# 				else :
	# 					if UserInfo.save_info(data['name'],data['rollno'],data['email'],data['mobno'],user_id):
	# 						return ({"Status":"Information saved."})
	# 					else :
	# 						return ({"Status":"Some error occured."})

	# 		if s in arr:
	# 			if s == arr[0]:   

	# 				info = get_user_info(user)
	# 				op = UserInfo_P_class(200,info.fullName,info.rollNo,info.emailId,info.mobNo)
	# 				result = userinfo_p_schema.dump(op)
	# 				return result.data


	

	def get(self,s):
		user = get_current_user()
		arr = ["profile","myclubs","myevents","attending","followed"]
		if user:
			if s in arr:
				if s == arr[0]:   # Get current user profile
					
					# info = get_user_info(user)
					op = UserInfo_class(200,user.fullName,user.rollNo,user.emailId,user.mobNo)
					result = userinfo_schema.dump(op)
					return result.data

				elif s == arr[1]: # Get a list of clubs the user is admin of.
					
					myclubs = get_user_club(user)
					op = Nested_output(200,user.myclubs)
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


class UserUnique(Resource):
	"""API to check whether username or password unique"""

	field = ["username","email"]

	def post(self,attr):
		return ({"Status":"Invalid Method."})


	def get(self,attr):
		user = request.authorization
		if attr == self.field[0] :
			username = UserReg.query.filter_by(userName=user.username).first()
			if username is None :
				return jsonify({"Status" : "True"})
			else :
				return jsonify({"Status" : "False"})

		elif attr == self.field[1] :
			username = UserReg.query.filter_by(emailId=user.username).first()
			if username is None :
				return jsonify({"Status" : "True"})
			else :
				return jsonify({"Status" : "False"})

		else :
			return ({"Status":"Invalid Request."})

class EmailVerification(Resource):
	"""API to Verify Email"""

	def post(self):
		return ({"Status":"Invalid Method."})

	def get(self,code):
		email = base64.b64decode(code)
		user = UserReg.query.filter_by(emailId = email).first()
		user.isVerified = True		# TODO: Checking Email
		return "<center><h1>You're Now Verified User</h1></center>"

class EventRegistration(Resource):
	def post(self):
		user = get_current_user()
		if user:
			json_data = request.get_json()
			data, errors = eventreg_schema.load(json_data)
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
					return jsonify({"Status":"Error"})

		else :
			return jsonify({"Status":"Unauthorized access"})

	def get(self):
		user = get_current_user()
		if user:
			events_list = EventsReg.query.all()
			events = []
			for event in events_list:
				contacts = get_contact_info(event)
				e = Events_class(200,
								event.eventName,
								event.eventInfo,
								event.totalSeats,
								event.leftSeats,
								event.occupiedSeats,
								event.eventVenue,
								event.createdBy,
								event.verified,
								contacts
					)
				events.append(e)
				result = event_schema.dump(events)
				# if result.error == {}:
				return {"events":result.data}
				# else :
				# 	return {"error":result.error}
		else:
			return jsonify({"Status":"Unauthorized access"})
			# events = Events.query.all()


class Clubsget(Resource):
	def post(self,s1,s2):
		return {"Staus":"Not allowed"}


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
				result = club_schema.dump(clubs)
				# if result.error == {}:
				return {"clubs":result.data}
				# else :
				# 	return {"error":result.error}
			elif s2 == "info" and club :
				result = userinfo_c_schema.dump(club)
				return result.data
			elif s2 == "events" and club :
				pass
		
		else:
			return jsonify({"Status":"Unauthorized access."})




class User_Follow_Status(Resource):
	def post(self,s1,event_or_club_id,s2):
		user = get_current_user()
		if user:

			if s1 == "club" and s2 == "follow":
				club = ClubInfo.query.filter_by(id=event_or_club_id).first()
				club.add_follower(user)
				return jsonify({"Status":"Successfully followed."})

			elif s1 == "event" and s2 == "follow":
				event = EventsReg.query.filter_by(id=event_or_club_id).first()
				event.add_follower(user)
				return jsonify({"Status":"Successfully followed."})

			elif s1 == "club" and s2 == "unfollow":
				club = ClubInfo.query.filter_by(id=event_or_club_id).first()
				club.remove_follower(user)
				return jsonify({"Status":"Successfully unfollowed"})

			elif s1 == "event" and s2 == "unfollow":
				event = EventsReg.query.filter_by(id=event_or_club_id).first()
				event.remove_follower(user)
				return jsonify({"Status":"Successfully unfollowed"})

			else :
				return jsonify({"Status":"Invalid Request"})


		else :
			return jsonify({"Status":"Unauthorized access."})


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
		
# @api.errorhandler(500)
# def some_error():
# 	db.session.rollback()
# 	return "Retry"




api.add_resource(UserRegistration,'/api/user/reg')
api.add_resource(UserInformation,'/api/user/<string:s>')
api.add_resource(EventRegistration,'/api/events/')
api.add_resource(Clubsget,'/api/clubs/<string:s1>/<string:s2>')
api.add_resource(UserUnique,'/api/unique/<string:attr>')
api.add_resource(Testing,'/')
api.add_resource(WebScrap,'/api/scrap/<string:source>')
api.add_resource(User_Follow_Status,'/api/<string:s1>/<int:event_or_club_id>/<string:s2>/')
# api.add_resource(EEmail,'/api/mail')

if __name__ == "__main__":
	db.create_all()
	port = int(os.environ.get('PORT', 5432))
	app.run(host='0.0.0.0', port=port, debug=True)
	# app.run(port=6080,debug=True)

