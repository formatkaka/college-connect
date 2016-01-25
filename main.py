from __init__ import *
from config import *
from models import *
import os, flask, scrap
from flask_mail import Message
import base64
from schemas import *
from opschemas import *
from flask.ext.restful import abort
from push_notifs import push_notif
from sqlalchemy.exc import  SQLAlchemyError
from gmail_logs import *
from drive_api import DriveApi
from functools import wraps


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		user= get_current_user()

			# return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

class Testing(Resource):
	"""Test Class for API"""
	def get(self):
		hello = '<h1>It Works!</h1>'
		response = flask.make_response(hello)
		response.headers['content-type'] = 'text/html'
		return response


class UserRegistration(Resource):
	""" API to register a new user or obtain token for a user"""

	def post(self, s1):
		""" Register a user """
		if s1 != "reg":
			abort(400)
		user = request.authorization
		if not user:
			abort(401, message="ERR01")

		email = user.username
		password_hash = user.password
		json_data = request.get_json()
		data, errors = info_schema.load(json_data)

		if email == "":  # Check if any of auth headers are empty
			abort(401, message="ERR02")

		if password_hash == "":
			abort(401, message="ERR03")

		if errors:
			return jsonify(errors)

		stat = UserReg.if_unique(data.rollno, data.mobno)

		if stat:
			# try :
			user_1 = UserReg( passwordHash=password_hash, fullName=data.name
							 , rollNo=data.rollno, emailId=email, mobNo=data.mobno)
			db.session.add(user_1)
			db.session.commit()
			recieve = ["sid.siddhant.loya@gmail.com", "murali.prajapati555@gmail.com"]
			token = user_1.gen_auth_token(expiration=1200)
			op = UserReg_class(token)
			result = userreg_schema.dump(op)

			link = 'https://sheltered-fjord-8731.herokuapp.com/api/verify/' + base64.b64encode(email)

			msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
					  sender="college.connect28@gmail.com",
					  recipients=recieve)

			msg.body = "please click on the link {0}".format(link)
			mail.send(msg)

			return result.data
			# except SQLAlchemyError:
			#     db.session.rollback()
			#     abort(500)

			# except Exception as e :

				# try:
				#     db.session.delete(user_1)
				#     db.session.commit()
				# except:
				#     db.session.rollback()
				# logging.error(e)
				# abort(500)



	def get(self, s1):
		""" Obtain/Generate token for user """
		if s1 != "token":
			abort(400)
		user = get_current_user()

		token = user.gen_auth_token(expiration=1200)

		op = UserReg_class(token)
		result = userreg_schema.dump(op)
		return result.data

	def put(self, s1):
		if s1 != "edit":
			abort(400)
		user = get_current_user()
		json_data = request.get_json()
		data, errors = info_schema.load(json_data)
		if errors:
			return jsonify(errors)
		try:
			UserReg.if_unique(data.rollno, data.mobno, user)
			user.mobNo = data.mobno
			user.rollNo = data.rollno
			user.fullName = data.name
			db.session.add(user)
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()
			logging.error(e)
			abort(500)
		except Exception as e :
			logging.error(e)
			abort(500)

		return jsonify({"message": "edited"})


class ForgotPassword(Resource):
	""" API to Reset Password """

	def post(self):
		json_data = request.get_json()
		data, errors = forgot_pass.load(json_data)
		if errors:
			return jsonify(errors)

		user = UserReg.query.filter_by(emailId=data['email']).first_or_404()

		s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 30)
		token = s.dumps({'id': user.id})

		link = 'https://sheltered-fjord-8731.herokuapp.com/api/reset/' + token

		msg = Message(subject="Reset password",
					  sender="college.connect01@gmail.com",
					  recipients=["siddhantloya2008@gmail.com"])

		msg.body = "please click on the link {0}".format(link)
		mail.send(msg)
		return jsonify({"message": "email sent"})

	def get(self):
		pass


class UserInformation(Resource):
	""" API to GET user info """

	def get(self):
		user = get_current_user()
		events_attending = [user.events[i].id for i in range(0, len(user.events))]
		clubs_following = [user.f_clubs[i].id for i in range(0, len(user.f_clubs))]
		events_created = EventsReg.query.filter_by(createdBy=user.id).all()
		my_events = [events_created[i].id for i in range(0, len(events_created))]
		club_admin = [user.a_clubs[i].id for i in range(0, len(user.a_clubs))]

		info = UserInfo_class( user.fullName, user.rollNo, user.emailId,
							  user.mobNo, club_admin, my_events, clubs_following, events_attending)

		data, errors = userinfo_schema.dump(info)
		if errors:
			return jsonify({"Errors": errors})
		else:
			return jsonify({"Information": data})
			# else:
			#     return jsonify({"message": "Invalid"})


class UserUnique(Resource):
	"""API to check whether username or password unique"""

	field = ["email"]

	def get(self, attr):
		user = request.authorization
		if attr == self.field[0]:
			email = UserReg.query.filter_by(emailId=user.username).first()
			if email is None:
				return jsonify({"message": "True"})
			else:
				abort(409, message="ERR14")

		else:
			abort(400, message="Invalid URL")


class EmailVerification(Resource):
	"""API to Verify Email"""

	# def post(self):
	#     return ({"message": "Invalid Method."})

	def get(self, code):
		email = base64.b64decode(code)
		user = UserReg.query.filter_by(emailId=email).first_or_404()
		user.isVerified = True
		db.session.add(user)
		db.session.commit()

		hello = '<h1>You are now a verified user.</h1>'
		response = flask.make_response(hello)
		response.headers['content-type'] = 'text/html'
		return response


class EventRegistration(Resource):
	def post(self):
		user = get_current_user()
		if user.isVerified is False:
			abort(401,message="ERR08")
		json_data = request.get_json()
		data, errors = eventreg_schema.load(json_data)
		if errors:
			return jsonify(errors)
		else:
			# try:
			event = EventsReg.register_one(data.name,
										   data.about,
										   data.venue,
										   conv_time(data.sdt),
										   user,
										   data.contacts,
										   data.seats,
										   conv_time(data.edt),
										   conv_time(data.lastregtime)
										   )
			# drive = DriveApi()
			# flag = drive.upload(data.image, 'qwerty')
			# event.imageLink = str(flag)
			# db.session.add(event)
			# db.session.commit()
			push_notif("A new event has been created.{0}".format(data.name))
			return jsonify({"message": event.id})

	def get(self):
		events_list = EventsReg.query.all()
		events = []
		for event in events_list:
			contacts = get_contact_info(event)
			e = Events_class(
					event.eventName,
					event.eventInfo,
					event.eventVenue,
					event.createdBy,
					event.verified,
					contacts,
					event.clubName,
					event.id,
					event.totalSeats,
					event.leftSeats,
					event.occupiedSeats


			)
			events.append(e)

		result, errors = event_schema.dump(events)
		return {"events": result}

			# events = Events.query.all()


class Clubsget(Resource):

	def get(self):
		clubs_list = ClubInfo.query.all()

		clubs = []
		for club in clubs_list:
			admins = get_admin_info(club)
			events = [club.eventsList[i].id for i in range(0, len(club.eventsList))]
			c = Club_class(club.clubName, club.aboutClub, admins, events)
			clubs.append(c)
		result = club_schema.dump(clubs)
		# if result.error == {}:
		return {"clubs": result.data}


class User_Follow_message(Resource):
	def post(self, s1, event_or_club_id, s2):
		user = get_current_user()
		if user:

			if s1 == "club" and s2 == "follow":
				club = ClubInfo.query.filter_by(id=event_or_club_id).first_or_404()
				club.add_follower(user)
				return jsonify({"message": "Successfully followed."})

			elif s1 == "event" and s2 == "follow":
				event = EventsReg.query.filter_by(id=event_or_club_id).first_or_404()
				event.add_follower(user)
				return jsonify({"message": "Successfully followed."})

			elif s1 == "club" and s2 == "unfollow":
				club = ClubInfo.query.filter_by(id=event_or_club_id).first_or_404()
				club.remove_follower(user)
				return jsonify({"message": "Successfully unfollowed"})

			elif s1 == "event" and s2 == "unfollow":
				event = EventsReg.query.filter_by(id=event_or_club_id).first_or_404()
				event.remove_follower(user)
				return jsonify({"message": "Successfully unfollowed"})

			else:
				return jsonify({"message": "Invalid Request"})


sources = ["notice", "seminar", "quick"]


class GCMessaging(Resource):
	def post(self):
		json_data = request.get_json()
		data, errors = gcm_schema.load(json_data)

		gcm_id_arr = GCMRegIds.query.filter_by(id=1).first()
		gcm_id_arr.data.append(data['gcmid'])
		db.session.add(gcm_id_arr)
		db.session.commit()
		return jsonify({"message": "saved"})
		# except:
		#     abort(500, message="ERR")


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
			return jsonify({"message": 'Invalid request'})


class AddRemoveAdmin(Resource):
	def post(self):
		json_data = request.get_json()
		data, errors = admin_schema.load(json_data)
		if errors:
			return jsonify(errors)
		else:
			club = ClubInfo.query.filter_by(id=data['club_id']).first_or_404()
			user = UserReg.query.filter_by(rollNo=data['rollno']).first_or_404()
			if not user.isVerified:
				abort(401, message="ERR08")
			if user.isAdmin:
				abort(409, message="ERR26")
			else:
				club.adminsList.append(user)
				user.isAdmin = True
				db.session.add_all([club, user])
				db.session.commit()
				return jsonify({"message": "admin added"})


class Testing1(Resource):
	def post(self):
		pass
		# user = get_current_user()
		# if user:
		json_data = request.get_json()
		base = json_data['file']
		drive = DriveApi()
		flag = drive.upload(base, 'qwerty')
		if flag:
			return jsonify({"Status": "Success"})
		else:
			return jsonify({"Status": "Upload Failed."})


class Reauthenticate(Form):
	new_password = PasswordField('Enter new password', validators=[DataRequired()])
	re_password = PasswordField('Re-enter new password', validators=[DataRequired(), EqualTo('new_password',
																							 message=' New Passwords do not match')])
	submit = SubmitField('Change Password')


@app.route('/api/reset/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
	s = Serializer(app.config['SECRET_KEY'])
	data = s.loads(token)
	user = UserReg.query.filter_by(id=data['id']).first()
	form = Reauthenticate()
	if form.validate_on_submit():
		user.passwordHash = form.new_password.data
		db.session.add(user)
		db.session.commit()
		flash('Password Changed')
		return render_template('reset.html', form=None)

	return render_template('reset.html', form=form)

# if not app.debug:
#     import logging
#     from logging.handlers import SMTPHandler
#
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)

api.add_resource(UserRegistration, '/api/user/<string:s1>')
api.add_resource(UserInformation, '/api/user/info')
api.add_resource(EventRegistration, '/api/events')
api.add_resource(Clubsget, '/api/clubs/list')
api.add_resource(UserUnique, '/api/unique/<string:attr>')
api.add_resource(Testing, '/')
api.add_resource(WebScrap, '/api/scrap/<string:source>')
api.add_resource(User_Follow_message, '/api/<string:s1>/<int:event_or_club_id>/<string:s2>')
api.add_resource(EmailVerification, '/api/verify/<string:code>')
api.add_resource(Testing1, '/api/test')
api.add_resource(GCMessaging, '/api/gcm')
api.add_resource(ForgotPassword, '/api/password')
api.add_resource(AddRemoveAdmin, '/api/admin')

if __name__ == "__main__":
	# manager.run()
	# db.create_all()
	port = int(os.environ.get('PORT', 5432))
	app.run(host='0.0.0.0', port=port, debug=True)
	# app.run(port=8080,debug=True)

	# TODO - 1. server_id for event and clubs
	# TODO - 2. clubs event list, user.isAdmin implementation !
	# TODO - 3. clubname in events api.
	# TODO - 4. not,None
	# TODO - 5. mobile number,json string input!
	# TODO - 6. gcm(events created)
	# TODO - 7. imports