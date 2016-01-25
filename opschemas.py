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
    def __init__(self, name, rollno, email, mobno=None, club_admin=None, my_events=None, clubs_following=None,
                 events_attending=None):
        self.club_admin = club_admin
        self.my_events = my_events
        self.clubs_following = clubs_following
        self.events_attending = events_attending
        self.name = name
        self.rollno = rollno
        self.email = email
        self.mobno = mobno


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


##### CLUBS INFORMATION #####

class Admins():
    def __init__(self, name, mobno):
        self.name = name
        self.mobno = mobno


class Admin_Response(Schema):
    name = fields.Str()
    mobno = fields.Int()


class Club_class():
    def __init__(self, name, about, admins, events, club_id):
        self.name = name
        self.about = about
        self.admins = admins
        self.events = events
        self.club_id = club_id

class Club_response(Schema):
    name = fields.Str()
    about = fields.Str()
    admins = fields.Nested(Admin_Response, many=True)
    events = fields.List(fields.Int)
    club_id = fields.Int()

##### EVENTS INFORMATION ##### 

class Events_class():
    def __init__(self, name, about, venue, createdby, verified, contacts,clubname,
                 event_id,sdt,edt=None,lrt=None,total_seats=None, available_seats=None, occupied_seats=None):
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
    contacts = fields.Nested(Admin_Response, many=True)
    event_id = fields.Int()
    sdt = fields.Float()
    edt = fields.Float()
    lrt = fields.Float()
    # createdby = fields.Str()


userreg_schema = UserReg_Response()
userinfo_schema = UserInfo_Response()
club_schema = Club_response(many=True)
event_schema = Events_Response(many=True)
