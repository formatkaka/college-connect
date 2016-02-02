from config import *
# from impf import *
from opschemas import *
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import Mutable
from flask_mail import Message
from sqlalchemy.orm.exc import NoResultFound
from gmail_logs import *

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

    def remove(self, value):
        list.remove(self,value)
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
    emailId = db.Column(db.String, unique=True)
    passwordHash = db.Column(db.String, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    currentAdmin = db.Column(db.Boolean, default=True)  # Current admin or Previous admin.
    activeStatus = db.Column(db.Boolean, default=True)  # Account active or not.
    isVerified = db.Column(db.Boolean, default=False)  # Verified by Email.
    fullName = db.Column(db.String, nullable=False)
    rollNo = db.Column(db.String, unique=True)
    mobNo = db.Column(db.BigInteger, unique=True)
    hostelite_or_localite = db.Column(db.Boolean)
    hostelName = db.Column(db.String)



    def check_password_hash(self, password_hash):
        if password_hash == self.passwordHash:
            return True
        else:
            return False



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

    @staticmethod
    def if_unique(rollno, email,mobno, user=None):
        a, b, c = 0, 0, 0
        if rollno is not None:
            if UserReg.query.filter_by(rollNo=rollno).first():
                a = 1
        if UserReg.query.filter_by(emailId=email).first():
            b = 1
        if mobno is not None:
            if UserReg.query.filter_by(mobNo=mobno).first():
                c = 1
        if user:
            return err_stat2(a,b,c,rollno,mobno)
        return err_stat(a, b, c)

    def user_is_admin(self):

        if self.isAdmin and self.currentAdmin:
            club = self.a_clubs[0]
            return True,club
        else:
            club = ClubInfo.query.first()
            return False,club

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
    imageLink = db.Column(db.String, default=None)
    time_created = db.Column(db.DateTime, default=datetime.now())
    clubName = db.Column(db.String)
    imageB64 = db.Column(db.Text)
    eventColorHex = db.Column(db.String)
    schedulerList = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    notifOne = db.Column(db.DateTime, default=None)
    notifTwo = db.Column(db.DateTime, default=None)
    eventRegFees = db.Column(db.Integer, default=None)
    eventPrizeMoney = db.Column(db.Integer, default=None)
    notifMessage = db.Column(db.String)

    @staticmethod
    def register_one(name, about, venue, sdt, user, contacts,image, seats=None, edt=None, lastregtime=None,
                     notifone=None,notiftwo=None, notifmessage=None):
        # try:
        val,club = user.user_is_admin()
        clubname = club.clubName
        # club = ClubInfo.query.filter_by(id=club_id).first_or_404()
        if seats is None:
            leftseats = None
            occupiedseats = 0
        else:
            leftseats = seats
            occupiedseats = 0
        eve = EventsReg(eventName = name,
                        eventInfo = about,
                        eventVenue = venue,
                        startDateTime = sdt,
                        createdBy = user.id,
                        totalSeats = seats,
                        endDateTime = edt,
                        verified = val,
                        lastRegDateTime = lastregtime,
                        activeStatus = True,
                        leftSeats = leftseats,
                        occupiedSeats = occupiedseats,
                        clubName = clubname,
                        imageB64 = image,
                        notifOne = notifone,
                        notifTwo = notiftwo,
                        notifMessage = notifmessage,
                        )

        eve.add_contacts(contacts)
        club.eventsList.append(eve)
        eve.schedule_gcm(val,notifmessage,notifone,notiftwo)
        db.session.add(club)
        db.session.commit()
        # send_email(val,user,eve.id)

        return eve
        # except:
        #     abort(400,message="some error occured.")

    def add_contacts(self, contacts):
        for item in contacts:
            if not item.contactid:
                contact = ContactsForEvent(contactName=item.contactname, contactNumber=item.contactnumber
                                           , contactEmail = item.contactemail)
                self.contacts.append(contact)
            if item.contactid:
                contact = ContactsForEvent.query.filter_by(id=item.contactid).first_or_404()
                contact.contactName = item.contactname
                contact.contactNumber = item.contactnumber
                contact.contactEmail = item.contactemail

    def set_active(self):
        self.activeStatus = True
        db.session.add(self)
        db.session.commit()

    def add_follower(self, user):

        if user in self.followers:
            abort(409, message="ERR23")
        else:
            if self.totalSeats is None:
                self.occupiedSeats += 1
                self.followers.append(user)
                db.session.add(self)
                db.session.commit()

            elif self.leftSeats > 0:
                self.leftSeats -=  1
                self.occupiedSeats +=  1
                self.followers.append(user)
                db.session.add(self)
                db.session.commit()


            elif self.leftSeats == 0:
                abort(409, message="ERR24")

    def remove_follower(self, user):
        if user not in self.followers:
            abort(409, message="ERR25")
        else:
            if self.totalSeats is None:
                self.occupiedSeats -= 1
                self.followers.remove(user)
                db.session.add(self)
                db.session.commit()

            elif self.leftSeats > 0:
                self.leftSeats +=  1
                self.occupiedSeats -=  1
                self.followers.remove(user)
                db.session.add(self)
                db.session.commit()

    def edit_seats(self, seats):
        if seats < self.occupiedSeats:
            abort(400,message="ERR36")

    # @staticmethod
    def schedule_gcm(self, val,message,notifone=None,notiftwo=None):
        foo = Scheduler_list.query.filter_by(id=1).first()

        time1 = conv_time(notifone)
        time2 = conv_time(notiftwo)
        self.schedulerList = []
        foo.verifiedNotifs = []
        foo.notverifiedNotifs = []
        if time1:
            if val : foo.verifiedNotifs.append((message,str(time1)))
            if not val : foo.notverifiedNotifs.append((message,str(time1)))
            self.schedulerList.append((message,str(time1)))
        if time2:
            if val: foo.verifiedNotifs.append((message,str(time2)))
            if not val : foo.notverifiedNotifs.append((message,str(time2)))
            self.schedulerList.append((message,str(time1)))


        db.session.add(foo)

        db.session.commit()
        global checkList
        checkList = foo.notverifiedNotifs


    def reschedule_gcm(self,new_time):
        pass

class EventsVersion(db.Model):
    __tablename__ = "orgby"

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)

    @staticmethod
    def increment_version():
        try:
            ver = EventsVersion.query.first()
            ver.version += 0.01
            db.session.add(ver)
            db.sesion.commit()
        except NoResultFound:
            ver = EventsVersion()
            ver.version = 0.01
            db.session.add(ver)
            db.session.commit()
        except Exception as e:
            abort(500)
            logging.error(e)

    @staticmethod
    def get_event_version():
        try:
            ver = EventsVersion.query.first()
            return ver.version
        except Exception as e:
            logging.error(e)
            # def __repr__(self):
            # 	return "<Name> {0} <Info> {1} <Seats> {2} <Venue> {3} <Verified> {4} <createdBy> {5} ".format(self.eventName,self.eventInfo,self.seats,self.eventVenue,self.verified,self.createdBy)


class OrgBy(db.Model):
    """ Table containing Club ids which have organised an event (One club or more than one club combined) """
    __tablename__ = "orgby"

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    orgBy = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))



class ContactsForEvent(db.Model):
    """ List of contacts """
    __table_args__ = {'extend_existing': True}
    __tablename__ = "contacts_events"

    id = db.Column(db.Integer, primary_key=True)
    contactName = db.Column(db.String)
    contactNumber = db.Column(db.BigInteger)
    contactEmail = db.Column(db.String)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class GCMRegIds(db.Model):
    """ List of GCM reg Ids"""
    __tablename__ = "gcmids"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(MutableList.as_mutable(ARRAY(db.String())))

class NoticeSection(db.Model):
    """ Notices Section """
    __tablename__ = "notice"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    noticeName = db.Column(db.String)
    aboutNotice = db.Column(db.String)
    noticeImage = db.Column(db.String)

class Scheduler_list(db.Model):
    """ Scheduler list for gcm.   """
    __tablename__ = "schedule"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    verifiedNotifs = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    notverifiedNotifs = db.Column(MutableList.as_mutable(ARRAY(db.String())))

####################################
######## HELPER FUNCTIONS ##########
####################################



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
            user_get = UserReg.query.filter_by(emailId=username_or_token).first()
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

def err_stat2(a,b,c,rollno,mobno):
    user = get_current_user()
    b=0
    if a==1 :
        if  UserReg.query.filter_by(rollNo=rollno).first() is user:
            a=0
    # if b==1:
    #     if  UserReg.query.filter_by(emailId=email).first() is user:
    #         b=0
    if c==1:
        if  UserReg.query.filter_by(mobNo=mobno).first() is user:
            c=0
    return err_stat(a,b,c)

def conv_time(unixstamp_or_datetime):
    if unixstamp_or_datetime is None:
        return None

    if isinstance(unixstamp_or_datetime, datetime):
        return time.mktime(unixstamp_or_datetime.timetuple())

    else:
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
        a = Admins(contact.contactName, contact.contactNumber,contact.contactEmail ,contact.id)
        contacts.append(a)
    return contacts

def send_email(val,user,eve_id):
    if val:
        message = "Your response has been saved and shall be published shortly."
    else:
        message = "Your response has been saved . It shall be pusblished after verification."

    recieve1 = "college.connect28@gmail.com"
    recieve2 = "college.connect28@gmail.com"
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

def error_mail(e):
    recieve1 = "college.connect28@gmail.com"

    msg1 = Message(subject="Error occured",
              sender="college.connect28@gmail.com",
              recipients=[recieve1])

    msg1.body = e
    mail.send(msg1)

def foo_bar():
    foo = Scheduler_list.query.filter_by(id=1).first()
    return foo