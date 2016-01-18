from config import *
# from impf import *
from opschemas import *
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import Mutable
from flask_mail import Message
####### Reference table for many-many relationships #######

# 1 ---> CLUBS FOLLOWED BY USERS
user_clubs = db.Table('user_clubs',
                      db.Column('club_id', db.Integer, db.ForeignKey('clubs.id')),
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                      )

# 2 ---> EVENTS ATTENDING BY USERS
user_events = db.Table('user_events',
                       db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                       )

# 3 ---> ADMINS LIST OF A CLUB
club_admins = db.Table('club_admins',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'))
                       )
# 4 ---> EVENTS-CLUBS TABLE
club_events = db.Table('club_events',
                       db.Column('clubs_id', db.Integer, db.ForeignKey('clubs.id')),
                       db.Column('events_id', db.Integer, db.ForeignKey('events.id'))
                       )


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


#################
#### MODELS #####
#################


class UserReg(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String, unique=True, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)
    isadmin = db.Column(db.Boolean, default=False)
    currentAdmin = db.Column(db.Boolean, default=True)  # Current admin or Previous admin.
    activeStatus = db.Column(db.Boolean, default=True)  # Account active or not.
    isVerified = db.Column(db.Boolean, default=False)  # Verified by Email.
    fullName = db.Column(db.String, nullable=False)
    rollNo = db.Column(db.String, nullable=False, unique=True)
    emailId = db.Column(db.String, unique=True)
    mobNo = db.Column(db.Integer, unique=True)

    @staticmethod
    def if_username_unique(username):
        if UserReg.query.filter_by(userName=username).first():
            return False
        else:
            return True

    def check_password_hash(self, password_hash):
        if password_hash == self.passwordHash:
            return True
        else:
            return False

    @staticmethod
    def register_user(username, password_hash):
        user = UserReg(userName=username, passwordHash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

    def gen_auth_token(self, expiration=None):

        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None, 0  # valid token, but expired
        except BadSignature:
            return None, 1  # invalid token
        user = UserReg.query.get(data['id'])
        return user, None

    def add_club(self, clubname):
        """ Add a user to list of club followers """

        club = ClubInfo.query.filter_by(clubName=clubname).first()
        club.followers.append(self)
        db.session.add(club)
        db.session.commit()

    def add_event(self, eventname):
        """ Add a user to list of event followers """

        event = EventsReg.query.filter_by(eventName=eventname).first()
        event.followers.append(self)
        db.session.add(event)
        db, session.commit()

    @staticmethod
    def if_unique(rollno=None, email=None, mobno=None):
        a, b, c = 0, 0, 0
        if UserReg.query.filter_by(rollNo=rollno).first():
            a = 1
        if UserReg.query.filter_by(emailId=email).first():
            b = 1
        if mobno is not None:
            if UserReg.query.filter_by(mobNo=mobno).first():
                c = 1
        return err_stat(a, b, c)

    def user_is_admin(self):

        if self.isadmin and self.currentAdmin:
            return True
        else:
            return False

    def is_attending_event(self, event):
        if event in self.events:
            return True
        else:
            return False


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
    eventsList = db.relationship('EventsReg', secondary=club_events,
                                 backref='e_clubs')

    @staticmethod
    def reg_club(name, about):
        club = ClubInfo(clubName=name, aboutClub=about)
        db.session.add(club)
        db.session.commit()
        return True

    @staticmethod
    def reg_admin(club_name, rollno):
        club = ClubInfo.query.filter_by(clubName=club_name).first()
        admin = UserReg.query.filter_by(rollNo=rollno).first()
        club.adminsList.append(admin)
        db.session.add(club)
        db.session.commit()

    def add_follower(self, user):
        if user in self.followers:
            abort(409, message="ERR23")
        else:
            self.followers.append(user)
            db.session.commit()

    def remove_follower(self, user):
        if user not in self.followers:
            abort(409, message="ERR25")
        else:
            self.followers.remove(user)
            db.session.commit()


class EventsReg(db.Model):
    """ List of events """

    __table_args__ = {'extend_existing': True}
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String)
    eventInfo = db.Column(db.String, nullable=True)
    startDateTime = db.Column(db.DateTime, nullable=True)
    endDateTime = db.Column(db.DateTime, nullable=True)
    lastRegDateTime = db.Column(db.DateTime)
    totalSeats = db.Column(db.Integer)
    occupiedSeats = db.Column(db.Integer)
    leftSeats = db.Column(db.Integer)
    eventVenue = db.Column(db.String)
    verified = db.Column(db.Boolean, default=False)  # If the event is verified
    createdBy = db.Column(db.Integer, db.ForeignKey('users.id'))  # The id of the admin it was created by.
    orgBy = db.relationship('OrgBy', backref='event', lazy='dynamic')
    contacts = db.relationship('ContactsForEvent', backref='event', lazy='dynamic')  # List of contacts for the event
    followers = db.relationship('UserReg', secondary=user_events,
                                backref='events')
    activeStatus = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime, default=datetime.now())

    @staticmethod
    def register_one(name, about, venue, sdt, user, contacts, seats=None, edt=None, lastregtime=None):
        try:
            val = user.user_is_admin()
            if seats is None:
                leftseats = 9999
                occupiedseats = 0
            else:
                leftseats = seats
                occupiedseats = 0
            eve = EventsReg(eventName=name,
                            eventInfo=about,
                            eventVenue=venue,
                            startDateTime=sdt,
                            createdBy=user.id,
                            totalSeats=seats,
                            endDateTime=edt,
                            verified=val,
                            lastRegDateTime=lastregtime,
                            activeStatus=True,
                            leftSeats=leftseats,
                            occupiedSeats=occupiedseats
                            )
            eve.add_contacts(contacts)
            db.session.add(eve)
            db.session.commit()
            send_email(val,user,eve.id)
            return eve
        except:
            abort(400,message="some error occured.")

    def add_contacts(self, contacts):
        for item in contacts:
            contact = ContactsForEvent(contactName=item['contactname'], contactNumber=item['contactnumber'])
            self.contacts.append(contact)

    def set_active(self):
        self.activeStatus = True
        db.session.add(self)
        db.session.commit()

    def add_follower(self, user):
        if user in self.followers:
            abort(409, message="ERR23")
        else:
            if self.leftSeats > 0:
                self.leftSeats = self.leftSeats - 1
                self.occupiedSeats = self.occupiedSeats + 1
                self.followers.append(user)
                db.session.add(self)
                db.session.commit()


            elif self.leftSeats == 0:
                abort(409, message="ERR24")

    def remove_follower(self, user):
        if user not in self.followers:
            abort(409, message="ERR25")
        else:
            self.followers.remove(user)
            self.leftSeats = self.leftSeats + 1
            self.occupiedSeats = self.occupiedSeats - 1
            db.session.commit()




            # def __repr__(self):
            # 	return "<Name> {0} <Info> {1} <Seats> {2} <Venue> {3} <Verified> {4} <createdBy> {5} ".format(self.eventName,self.eventInfo,self.seats,self.eventVenue,self.verified,self.createdBy)


class OrgBy(db.Model):
    """ Table containing Club ids which have organised an event (One club or more than one club combined) """
    __tablename__ = "orgby"

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    orgBy = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class OrgFor(db.Model):
    """ Table containing Club ids for which a given event is organised """
    __tablename__ = "orgfor"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    orgFor = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class ContactsForEvent(db.Model):
    """ List of contacts """
    __table_args__ = {'extend_existing': True}
    __tablename__ = "contacts_events"

    id = db.Column(db.Integer, primary_key=True)
    contactName = db.Column(db.String)
    contactNumber = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class GCMRegIds(db.Model):
    """ List of GCM reg Ids"""
    __tablename__ = "gcmids"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(MutableList.as_mutable(ARRAY(db.String(100))))


####################################
######## HELPER FUNCTIONS ##########
####################################

def get_user_club(user):
    """ Returns a list of clubs of which the user is admin
    """

    admin = Admins.query.filter_by(student_id=user.id).all()
    clubs = []
    for i in range(0, len(admin)):
        club = ClubInfo.query.filter_by(id=admin[i].club_id).first()
        clubs.append(club)

    return clubs


def get_current_user():
    """ Find user object if it has valid token or username-password. """

    # Incorrect credentials

    user = request.authorization

    if user is None:
        abort(401, message="ERR01")

    if user is not None:

        if user.username == "":
            abort(401, message="ERR02")

        if user.password == "":
            abort(401, message="ERR03")

        username_or_token = user.username
        password = user.password

        verified, value = UserReg.verify_auth_token(username_or_token)

        if user.password == "None":

            if verified:
                return verified

            elif not verified and value == 0:
                abort(401, message="ERR07")

            elif not verified and value == 1:
                abort(401, message="ERR06")

            else:
                abort(400)  # SOME UNKNOWN PROBLEM OCCURED

        if user.password != "None":
            user_get = UserReg.query.filter_by(userName=username_or_token).first()
            if user_get:
                if user_get.check_password_hash(password):
                    return user_get
                else:
                    abort(401, message="ERR05")
            else:
                abort(401, message="ERR04")
        else:
            return abort(400)  # SOME UNKNOWN PROBLEM OCCURED


def err_stat(a, b, c):
    if a == 0 and b == 0 and c == 0:
        return True

    if a == 0 and b == 0 and c == 1:
        abort(409, message="ERR15")

    if a == 0 and b == 1 and c == 0:
        abort(409, message="ERR16")

    if a == 0 and b == 1 and c == 1:
        abort(409, message="ERR17")

    if a == 1 and b == 0 and c == 0:
        abort(409, message="ERR18")

    if a == 1 and b == 0 and c == 1:
        abort(409, message="ERR19")

    if a == 1 and b == 1 and c == 0:
        abort(409, message="ERR20")

    if a == 1 and b == 1 and c == 1:
        abort(409, message="ERR21")


def conv_time(unixstamp_or_datetime):
    if unixstamp_or_datetime is None:
        return None

    if isinstance(unixstamp_or_datetime, datetime):
        return time.mktime(unixstamp_or_datetime.timetuple())

    elif isinstance(unixstamp_or_datetime, float):
        return datetime.fromtimestamp(unixstamp_or_datetime)

        # return dt


def get_admin_info(club):
    admins = []

    for admin in club.adminsList:
        a = Admins(admin.fullName, admin.mobNo)
        admins.append(a)
    return admins


def get_contact_info(event):
    contacts = []
    for contact in event.contacts:
        a = Admins(contact.contactName, contact.contactNumber)
        contacts.append(a)
    return contacts

def send_email(val,user,eve_id):
    if val:
        message = "Your response has been saved and shall be published shortly."
    else:
        message = "Your response has been saved . It shall be pusblished after verification."

    recieve1 = "college.connect28@gmail.com"
    recieve2 = user.emailId
    msg1 = Message(subject="Response Saved",
              sender="college.connect28@gmail.com",
              recipients=[recieve2])

    msg1.body = message
    mail.send(msg1)

    msg2 = Message(subject="Response Saved",
              sender="college.connect28@gmail.com",
              recipients=[recieve1])
    msg2.body = "Event recieved from user name:{0} , rollno:{1} , eve_id {2}".format(user.fullName,user.rollNo,
                                                                                  eve_id)
    mail.send(msg2)