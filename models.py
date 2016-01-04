from config import *
from impf import *
from opschemas import *



####### Reference table for many-many relationships #######

#1 ---> CLUBS FOLLOWED BY USERS
user_clubs = db.Table('user_clubs',
    db.Column('club_id', db.Integer, db.ForeignKey('clubs.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

#2 ---> EVENTS ATTENDING BY USERS
user_events = db.Table('user_events',
	db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
	db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

#3 ---> ADMINS LIST OF A CLUB
club_admins = db.Table('club_admins',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'))
)



#################
#### MODELS #####
#################


class UserReg(db.Model):
	__tablename__ = "users"
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)
	userName = db.Column(db.String,unique=True, nullable=False)
	passwordHash = db.Column(db.String, nullable=False)	
	isadmin = db.Column(db.Boolean, default=False)
	currentAdmin = db.Column(db.Boolean, default=True)
	activeStatus = db.Column(db.Boolean, default=True)
	isVerified = db.Column(db.Boolean, default=False)
	fullName = db.Column(db.String, nullable=False)
	rollNo = db.Column(db.String, nullable=False, unique=True)
	emailId = db.Column(db.String, unique=True)
	mobNo = db.Column(db.Integer, unique=True)	


	#For users presently in the college!
	# clubs_following = db.relationship('ClubInfo', secondary=user_clubs,
	#   backref='users')
# >>>>>>> baee92788eb13faa096053f020139f90309c3bc3
	# events_attending = db.relationship('EventsReg', secondary=user_events,
	# 	backref='users')	

	@staticmethod
	def if_username_unique(username):
		if UserReg.query.filter_by(userName=username).first():
			return False
		else :
			return True

	
	def check_password_hash(self,password_hash):
		if password_hash == self.passwordHash:
			return True
		else :
			return False

	@staticmethod
	def register_user(username,password_hash):
		user = UserReg(userName=username,passwordHash=password_hash)
		db.session.add(user)
		db.session.commit()
		return user

	def gen_auth_token(self,expiration=1200):
		 
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		# email_id = UserInfo.query.filter_by(user_id=self.id).first().emailId
		return s.dumps({ 'email': self.id })

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = UserReg.query.get(data['email'])
		return user

	def add_club(clubname): 
		""" Add a user to list of club followers """

		club = ClubInfo.query.filter_by(clubName=clubname).first()
		club.followers.append(self)
		db.session.add(club)
		db.session.commit()

	def add_event(eventname):
		""" Add a user to list of event followers """

		event = EventsReg.query.filter_by(eventName=eventname).first()
		event.followers.append(self)
		db.session.add(event)
		db,session.commit()

# class UserInfo(db.Model):
# 	__tablename__ = "userinfo"
# 	__table_args__ = {'extend_existing': True}

# 	id = db.Column(db.Integer, primary_key=True)
# 	fullName = db.Column(db.String, nullable=False)
# 	rollNo = db.Column(db.String, nullable=False, unique=True)
# 	emailId = db.Column(db.String, unique=True)
# 	mobNo = db.Column(db.Integer, unique=True)
# 	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)



# 	@staticmethod
# 	def save_info(name,rollno,email,mobno,user_id):
# 		info = UserInfo(fullName=name,rollNo=rollno,emailId=email,mobNo=mobno,user_id=user_id)
# 		db.session.add(info)
# 		db.session.commit()
# 		return True

	@staticmethod
	def if_unique(rollno,email,mobno):
		a,b,c=0,0,0
		if UserReg.query.filter_by(rollNo=rollno).first():
			a=1
		if UserReg.query.filter_by(emailId=email).first(): 
			b=1
		if UserReg.query.filter_by(mobNo=mobno).first():
			c=1
		return err_stat(a,b,c)

	# @staticmethod
	# def update_info():
	# 	pass

	# def __repr__(self):
	# 	return "<id> {0} <rollNo> {1} <fullName> {2} <emailId> {3} <mobNo> {4} ".format(self.id,self.rollNo,self.fullName,self.emailId
																									# ,self.mobNo)


class Admins(db.Model):
	""" Table containing all the verified Admins """
	__table_args__ = {'extend_existing': True}
	__tablename__ = "admins"

	id = db.Column(db.Integer, primary_key=True)
	club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
	student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	current_admin = db.Column(db.Boolean,default=True)

	@staticmethod
	def register_admin(s_id,c_id):
		admin = Admins(club_id=c_id,student_id=s_id)
		db.session.add(admin)


class ClubInfo(db.Model):
	""" A list of all the clubs ,their admins and its EventsReg """
	__table_args__ = {'extend_existing': True}
	__tablename__ = "clubs"

	id = db.Column(db.Integer, primary_key=True)
	clubName = db.Column(db.String, nullable=False)
	aboutClub = db.Column(db.Text)
	adminsList = db.relationship('UserReg', secondary=club_admins,
		backref='a_clubs')
	followers = db.relationship('UserReg', secondary=user_clubs,
		backref='f_clubs')


	@staticmethod
	def reg_club(name,about):
		club = ClubInfo(clubName=name,aboutClub=about)
		db.session.add(club)
		db.session.commit()
		return True

	@staticmethod
	def reg_admin(club_name,rollno):
		club = ClubInfo.query.filter_by(clubName=club_name).first()
		admin_id = UserReg.query.filter_by(rollNo=rollno).first()
		admin = UserReg.query.filter_by(id=admin_id).first()
		club.adminsList.append(admin)
		db.session.add(club)
		db.session.commit()

# <<<<<<< HEAD
	def add_follower(self,user):
		self.followers.append(user)
		db.session.add(self)
		db.session.commit()
# =======
# 	# def add_follower(clubname):
# 	# 	club = ClubInfo.query.filter_by(clubName=clubname).first()
# >>>>>>> baee92788eb13faa096053f020139f90309c3bc3

	def remove_follower(self,user):
		self.followers.remove(user)
		db.session.commit()

class EventsReg(db.Model):
	""" List of events """
	
	__table_args__ = {'extend_existing': True}
	__tablename__ = "events"

	id = db.Column(db.Integer, primary_key=True)
	eventName = db.Column(db.String)
	eventInfo = db.Column(db.String, nullable=True)
	startDateTime = db.Column(db.DateTime,nullable=True)
	endDateTime = db.Column(db.DateTime,nullable=True)
	totalSeats = db.Column(db.Integer)
	occupiedSeats = db.Column(db.Integer)
	leftSeats = db.Column(db.Integer)
	eventVenue = db.Column(db.String)
	verified = db.Column(db.Boolean, default=False)	#If the event is verified
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id')) # The id of the admin it was created by.
	# orgBy = db.relationship('OrgBy', backref='event', lazy='dynamic',nullable=True)
	contacts = db.relationship('ContactsForEvent',backref='event',lazy='dynamic')	# List of contacts for the event
	followers = db.relationship('UserReg', secondary=user_events,
		backref='events')
	activeStatus = db.Column(db.Boolean, default=False)




	@staticmethod
	def register_one(name,about,seats,venue,sdt,edt,user_id):
		eve = EventsReg(eventName=name,
						eventInfo=about,
						totalSeats = seats,
						eventVenue =venue,
						startDateTime=sdt,
						endDateTime=edt,
						createdBy = user_id)
		db.session.add(eve)
		db.session.commit()
		return eve

	def add_contacts(self,contacts):
		for item in contacts:
			ContactsForEvent.register_con(item['contactname'],item['contactnumber'],self.id)
		return True

	def set_active(self):
		self.activeStatus=True
		db.session.add(self)
		db.session.commit()

	def add_follower(self,user):
		self.followers.append(user)
		db.session.add(self)
		db.session.commit()

	def remove_follower(self,user):
		self.followers.remove(user)
		db.session.commit()

	def __repr__(self):
		return "<Name> {0} <Info> {1} <Seats> {2} <Venue> {3} <Verified> {4} <createdBy> {5} ".format(self.eventName,self.eventInfo,self.seats,self.eventVenue,self.verified,self.createdBy)



class OrgBy(db.Model):
	""" Table containing Club ids which have organised an event (One club or more than one club combined) """
	__tablename__="orgby"
	
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)
	orgBy = db.Column(db.Integer, db.ForeignKey('clubs.id'))
	event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

# class OrgFor(db.Model):
# 	""" Table containing Club ids for which a given event is organised """
# 	__tablename__="orgfor"
# 	__table_args__ = {'extend_existing': True}

# 	id = db.Column(db.Integer, primary_key=True)
# 	orgFor = db.Column(db.Integer,db.ForeignKey('clubs.id'))
# 	event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class ContactsForEvent(db.Model):
	""" List of contacts """
	__table_args__ = {'extend_existing': True}
	__tablename__ = "contacts_events"

	id = db.Column(db.Integer, primary_key=True)
	contactName = db.Column(db.String)
	contactNumber = db.Column(db.Integer)
	event_id = db.Column(db.Integer,db.ForeignKey('events.id'))

	@staticmethod
	def register_con(name,number,eve_id):
		contact = ContactsForEvent()
		contact.contactName = name
		contact.contactNumber = number
		contact.event_id = eve_id
		db.session.add(contact)
		db.session.commit()

####################################
######## HELPER FUNCTIONS ##########
####################################

def get_user_club(user):
	""" Returns a list of clubs of which the user is admin """

	admin = Admins.query.filter_by(student_id=user.id).all()
	clubs = []
	for i in range(0,len(admin)):
		club = ClubInfo.query.filter_by(id = admin[i].club_id).first()
		clubs.append(club)	

	return clubs


def get_current_user():
	""" Find user object if it has valid token or username-password. """

# Incorrect credentials

	user = request.authorization

	if not user:
		return jsonify({"Status":"Empty headers."})

	username_or_token = user.username
	password = user.password
	
	verified = UserReg.verify_auth_token(username_or_token)

	if verified:
		return verified

	user_get = UserReg.query.filter_by(userName=username_or_token).first()
	if user_get:
		if user_get.check_password_hash(password):
			return UserReg.query.filter_by(userName=username_or_token).first()
		else :
			return None
	else :
		return None 


# def get_user_info(user):
# 	info = UserReg.query.filter_by(user_id=user.id).first()
# 	if info:
# 		return info
# 	else :
# 		return None


def err_stat(a,b,c):
	if a==0 and b==0 and c == 0:
		return True,None
	if a==0 and b==0 and c == 1:
			return False,1
	if a==0 and b==1 and c == 0:
		return False,2
	if a==0 and b==1 and c == 1:	
		return False,3
	if a==1 and b==0 and c == 0:
		return False,4
	if a==1 and b==0 and c == 1:
		return False,5
	if a==1 and b==1 and c == 0:
		return False,6
	if a==1 and b==1 and c == 1:
		return False,7


def user_is_admin(user):
	if user.isadmin and user.currentAdmin:
		return True
	else :
		return False


def conv_time(t):
	dt = datetime.fromtimestamp(t)
	return dt



def get_admin_info(club):
	admins = []

	for admin in club.adminsList:
		info = get_user_info(admin)
		a = Admins(admin.userName,info.mobNo)
		admins.append(a)
	return admins

def get_contact_info(event):
	contacts = []
	for contact in event.contacts:
		a = Admins(contact.contactName,contact.contactNumber)
		contacts.append(a)
	return contacts

