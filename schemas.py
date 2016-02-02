from marshmallow import fields, Schema, post_load

## USER REGISTRATION SCHEMA


class UserInfoSchema_Request(Schema):
    rollno = fields.Str()
    name = fields.Str()
    mobno = fields.Int()
    hostelname = fields.Str()
    hostel_or_local = fields.Bool()   #TRUE if Hostelite!!

    @post_load
    def make_event(self,data):
        return UserInfo_class(**data)

class UserInfo_class(object):
    def __init__(self,name,hostel_or_local=None,hostelname=None,rollno=None,mobno=None):
        self.name = name
        self.rollno = rollno
        self.mobno = mobno
        self.hostelname = hostelname
        self.hostel_or_local = hostel_or_local

class ClubRegSchema_Request(Schema):
    name = fields.Str()
    about = fields.Str()

class ContactEvent_class(object):
    def __init__(self, contactname, contactnumber, contactid=None ,contactemail=None):
        self.contactname = contactname
        self.contactnumber = contactnumber
        self.contactemail = contactemail
        self.contactid = contactid

class ContactSchema_Request(Schema):
    contactid = fields.Int()
    contactname = fields.Str()
    contactnumber = fields.Int()
    contactemail = fields.Email()

    @post_load
    def make_event(self,data):
        return ContactEvent_class(**data)

class OrganisedBySchema_Request(Schema):
    club_by_id = fields.Int()


class Date_Request(Schema):
    sdt = fields.Int()

# EVENT REGISTRATION SCHEMA

class EventRegSchema_Request(Schema):
    eventid = fields.Int()
    name = fields.Str()
    about = fields.Str()
    sdt = fields.Float()
    edt = fields.Float()
    seats = fields.Int()
    venue = fields.Str()
    contacts = fields.Nested(ContactSchema_Request, many=True)
    lastregtime = fields.Float()
    image = fields.Str()
    notifone = fields.Float()
    notiftwo = fields.Float()
    notifmessage = fields.Str()
    regfees = fields.Int()
    prizemoney = fields.Int()

    @post_load
    def make_event(self,data):
        return EventRegSchema_class(**data)

class EventRegSchema_class(object):
    def __init__(self,name,about,sdt,venue,contacts,eventid=None,seats=None,image=None,edt=None,
                 lastregtime=None, notifone=None, notiftwo=None, notifmessage=None,regfees=None,
                 prizemoney=None):

        self.name = name
        self.about = about
        self.sdt = sdt
        self.edt = edt
        self.seats = seats
        self.venue = venue
        self.contacts = contacts
        self.lastregtime = lastregtime
        self.image = image
        self.eventid = eventid
        self.notifone = notifone
        self.notiftwo = notiftwo
        self.notifmessage = notifmessage
        self.regfees = regfees
        self.prizemoney = prizemoney

# organised_by = fields.Nested(OrganisedBySchema_Request, many=True)
# organised_for = fields.Nested(OrganisedForSchema_Request, many=True)

class GCM_Schema(Schema):
    gcmid = fields.Str()

class AdminSchema_Request(Schema):
    rollno = fields.Str()
    club_id = fields.Int()

class Forgot_Password(Schema):
    email = fields.Email()





#####   NOTICES   #####

class Notice_class(object):
    def __init__(self,name,about,image=None):
        self.name = name
        self.about = about
        self.image= image

class Notice_Rquest(Schema):
    name = fields.Str()
    about = fields.Str()
    image = fields.Str()


contact_schema = ContactSchema_Request(many=True)
eventreg_schema = EventRegSchema_Request(partial=True)
club_schema = ClubRegSchema_Request()
info_schema = UserInfoSchema_Request()
gcm_schema = GCM_Schema()
forgot_pass = Forgot_Password()
admin_schema = AdminSchema_Request()

