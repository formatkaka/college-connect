#####################
#### O/P Schemas ####
#####################

from marshmallow import fields, Schema


##### User Registration #####
class UserReg_class():
    def __init__(self, token):
        self.token = token


class UserReg_Response(Schema):
    token = fields.Str()


##### User Information #####

# 1 - Personal Info

class UserInfo_class(Schema):
    def __init__(self, name, rollno, email,verified, mobno=None, club_admin=None, my_events=None, clubs_following=None,
                 events_attending=None):
        self.club_admin = club_admin
        self.my_events = my_events
        self.clubs_following = clubs_following
        self.events_attending = events_attending
        self.name = name
        self.rollno = rollno
        self.email = email
        self.mobno = mobno
        self.verified = verified

class UserInfo_Response(Schema):
    username = fields.Str()
    name = fields.Str()
    rollno = fields.Str()
    email = fields.Email()
    mobno = fields.Int()
    events_attending = fields.List(fields.Int)
    clubs_following = fields.List(fields.Int)
    club_admin = fields.List(fields.Int)
    my_events = fields.List(fields.Int)
    verified = fields.Str()

##### CLUBS INFORMATION #####

class Admins():
    def __init__(self, name, mobno,email=None, id=None):
        self.name = name
        self.mobno = str(mobno)
        self.id = id
        self.email = email

class Admin_Response(Schema):
    name = fields.Str()
    mobno = fields.Str()
    id = fields.Int()
    email = fields.Email()

class Club_class():
    def __init__(self, name, about, admins, events, club_id, image):
        self.name = name
        self.about = about
        self.admins = admins
        self.events = events
        self.club_id = club_id
        self.image = image

class Club_response(Schema):
    name = fields.Str()
    about = fields.Str()
    admins = fields.Nested(Admin_Response, many=True)
    events = fields.List(fields.Int)
    club_id = fields.Int()
    image = fields.Str()
##### EVENTS INFORMATION ##### 
class Eve_Con():
    def __init__(self, name, mobno="NA",email=None, id=None):
        self.name = name
        self.mobno = mobno
        self.id = id
        self.email = email

class Eve_Contacts(Schema):
    name = fields.Str()
    mobno = fields.Str()
    id = fields.Int()
    email = fields.Email()

class Events_class():
    def __init__(self, name, about, venue, createdby, verified, contacts,clubname,
                 event_id,sdt,club_id,createdtime,image=None,edt=None,lrt=None,total_seats=None,
                 available_seats=None, occupied_seats=None, prize=None, fees=None, color=None):
        self.name = name
        self.about = about
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.occupied_seats = occupied_seats
        self.venue = venue
        self.createdby = createdby
        self.verified = verified
        self.contacts = contacts
        self.clubname = clubname
        self.event_id = event_id
        self.sdt = sdt
        self.edt = edt
        self.lrt = lrt
        self.club_id = club_id
        self.image = image
        self.prize = prize
        self.fees = fees
        self.color = color
        self.createdtime = createdtime

class Events_Response(Schema):
    name = fields.Str()
    about = fields.Str()
    total_seats = fields.Int()
    available_seats = fields.Int()
    occupied_seats = fields.Int()
    venue = fields.Str()
    createdby = fields.Int()
    verified = fields.Str()
    clubname = fields.Str()
    contacts = fields.Nested(Eve_Contacts, many=True)
    event_id = fields.Int()
    sdt = fields.Float()
    edt = fields.Float()
    lrt = fields.Float()
    club_id = fields.Int()
    image = fields.Str()
    prize = fields.Int()
    fees = fields.Int()
    color = fields.Str()
    createdtime = fields.Float()
    # createdby = fields.Str()

class Notice_class(object):
    def __init__(self,name,time,creator,about=None,image=None):
        self.name = name
        self.about = about
        self.image= image
        self.time = time
        self.creator = creator

class Notice_Schema(Schema):
    name = fields.Str()
    about = fields.Str()
    image = fields.Str()
    time = fields.Float()
    creator = fields.Str()

userreg_schema = UserReg_Response()
userinfo_schema = UserInfo_Response()
club_schema = Club_response(many=True)
event_schema = Events_Response(many=True)
notice_schema = Notice_Schema(many=True)
eve = Eve_Contacts(many=True)