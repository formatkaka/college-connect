#####################
#### O/P Schemas ####
#####################

from marshmallow import fields, Schema






##### User Registration #####
class UserReg_class():
	def __init__(self,status_code,username,token):
		self.status_code = status_code
		self.username = username
		self.token = token

class UserReg_Response(Schema):
	status_code = fields.Int()
	username = fields.Str()
	token = fields.Str()


##### User Information #####

# 1 - Personal Info

class UserInfo_class(Schema):

	def __init__(self,admin,events,clubsfollowed,eventsattending,name,rollno,email,mobno):
		self.admin = admin
		self.events = events
		self.clubsfollowed = clubsfollowed 
		self.eventsattending = eventsattending
		self.name = name
		self.rollno = rollno
		self.email = email
		self.mobno = mobno


class UserInfo_Response(Schema):
	status_code = fields.Int()
	name = fields.Str()
	rollno = fields.Str()
	email = fields.Email()
	mobno = fields.Int()
	# eventsattending = fields.Nested
	# clubs_following = fields.Str(many=True)
	# events_attending = fields.Str(many=True)
	# club_if_admin = fields.Str(many=True)
	# events_created = fields.Str(many=True)
	
# 2 - Clubs/Events

class Admins():
	def __init__(self,name,mobno):
		self.name= name
		self.mobno = mobno

class Admin_Response(Schema):
	name = fields.Str()
	mobno = fields.Int()

class Club_class():
	def __init__(self,name,about,admins):
		self.name = name
		self.about = about
		self.admins = admins



class Club_response(Schema):
	name = fields.Str()
	about = fields.Str()
	admins = fields.Nested(Admin_Response,many=True)

class Error_Response(Schema):
	status_code = fields.Int()
	err_message = fields.Str()
	extra_1 = fields.Str()
	extra_2 = fields.Str()


class Events_class():
	def __init__(self,status_code,name,about,total_seats,available_seats,occupied_seats,venue,createdby,verified,contacts):
		self.status_code = status_code
		self.name = name
		self.about = about
		self.total_seats = total_seats
		self.available_seats = available_seats
		self.occupied_seats = occupied_seats
		self.venue = venue
		self.createdby = createdby
		self.verified = verified
		self.contacts = contacts

class Events_Response(Schema):
	status_code = fields.Int()
	name = fields.Str()
	about = fields.Str()
	total_seats = fields.Int()
	available_seats = fields.Int()
	occupied_seats = fields.Int()
	venue = fields.Str()
# <<<<<<< HEAD
	createdby = fields.Int()
	verified = fields.Str()
	contacts = fields.Nested(Admin_Response,many=True)
# =======
	createdby = fields.Str()
	# contacts = 
# >>>>>>> baee92788eb13faa096053f020139f90309c3bc3


userreg_schema = UserReg_Response()
err_schema = Error_Response()
userinfo_schema = UserInfo_Response()
club_schema = Club_response(many=True)
event_schema = Events_Response(many=True)
