from config import *
from impf import *

class UserReg(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	userName = db.Column(db.String,unique=True, nullable=False)
	password_hash = db.Column(db.String, nullable=False)
	isadmin = db.Column(db.Boolean, default=False)

	@staticmethod
	def if_username_unique(username):
		if UserReg.query.filter_by(userName=username).first():
			return False
		else :
			return True

	
	def check_password_hash(self,password_hash):
		if password_hash == self.password_hash:
			return True
		else :
			return False

	@staticmethod
	def register_user(username,password_hash):
		user = UserReg(userName=username,password_hash=password_hash)
		db.session.add(user)
		db.session.commit()
		return user

	def gen_auth_token(self,expiration=1200):
		 
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({ 'id': self.id })

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = UserReg.query.get(data['id'])
		return user


class UserInfo(db.Model):
	__tablename__ = "userinfo"

	id = db.Column(db.Integer, primary_key=True)
	fullName = db.Column(db.String, nullable=False)
	rollNo = db.Column(db.Integer, nullable=False, unique=True)
	emailId = db.Column(db.String, unique=True)
	# dob = db.Column(db.DateTime)
	mobNo = db.Column(db.Integer, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

	@staticmethod
	def save_info(name,rollno,email,mobno,user_id):
		info = UserInfo(fullName=name,rollNo=rollno,emailId=email,mobNo=mobno,user_id=user_id)
		db.session.add(info)
		db.session.commit()
		return True

	@staticmethod
	def if_unique(rollno,email,mobno):
		a,b,c=0,0,0
		if UserInfo.query.filter_by(rollNo=rollno).first():
			a=1
		if UserInfo.query.filter_by(emailId=email).first(): 
			b=1
		if UserInfo.query.filter_by(mobNo=mobno).first():
			c=1
		return err_stat(a,b,c)

	@staticmethod
	def update_info()

	def __repr__(self):
		return "<id> {0} <rollNo> {1} <fullName> {2} <emailId> {3} <mobNo> {4} ".format(self.id,self.rollNo,self.fullName,self.emailId
																									,self.mobNo)


class Admins(db.Model):
	""" Table containing all the verified Admins"""

	__tablename__ = "admins"
	id = db.Column(db.Integer, primary_key=True)
	club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
	student_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	@staticmethod
	def register_admin(s_id,c_id):
		admin = Admins(club_id=c_id,student_id=s_id)
		db.session.add(admin)


class ClubInfo(db.Model):
	""" A list of all the clubs ,their admins and its Events"""

	__tablename__ = "clubs"

	id = db.Column(db.Integer, primary_key=True)
	clubName = db.Column(db.String, nullable=False)
	aboutClub = db.Column(db.Text)
	adminsList = db.relationship('Admins', backref='clubs', lazy='dynamic')
	eventsList = db.relationship('Events', backref='clubs', lazy='dynamic')

	@staticmethod
	def reg_club(name,about):
		club = ClubInfo(clubName=name,aboutClub=about)
		db.session.add(club)
		db.session.commit()
		return True


class Events(db.Model):
	""" List of events """

	__tablename__ = "events"
	id = db.Column(db.Integer, primary_key=True)
	eventName = db.Column(db.String, nullable=False)
	eventInfo = db.Column(db.Text, nullable=False)
	startDate = db.Column(db.DateTime,nullable=False)
	endDate = db.Column(db.DateTime, nullable=False)
	startTime = db.Column(db.DateTime, nullable=False)
	endTime = db.Column(db.DateTime)
	totalSeats = db.Column(db.Integer)
	occupiedSeats = db.Column(db.Integer)
	leftSeats = db.Column(db.Integer)
	eventVenue = db.Column(db.String)
	verified = db.Column(db.Boolean, default=False)	#If the event is verified
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id')) # The id of the admin it was created by.
	orgClub = db.Column(db.Integer, db.ForeignKey('clubs.id'))   # The club ,the admin belongs to!
	contacts = db.relationship('ContactsForEvent',backref='event',lazy='dynamic')	# List of contacts for the event


class ContactsForEvent(db.Model):
	""" List of contacts """

	__tablename__ = "contacts_events"
	id = db.Column(db.Integer, primary_key=True)
	contactName = db.Column(db.String)
	contactNumber = db.Column(db.Integer)
	event_id = db.Column(db.Integer,db.ForeignKey('event.id'))


# FUNCTIONS

def get_current_user():
	""" Find user object if it has valid token or username-password. """
	user = request.authorization
	username_or_token = user.username
	
	if UserReg.verify_auth_token(username_or_token):
		return UserReg.verify_auth_token(username_or_token)

	elif UserReg.query.filter_by(userName=username_or_token).first():
		return UserReg.query.filter_by(userName=username_or_token).first()

	else :
		return None 


def get_user_info(user):
	info = UserInfo.query.filter_by(user_id=user.id).first()
	if info:
		return info
	else :
		return None


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
	if user.isadmin:
		return True
	else :
		return False
