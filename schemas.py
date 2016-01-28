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


class ContactSchema_Request(Schema):
    contactname = fields.Str()
    contactnumber = fields.Int()


class OrganisedBySchema_Request(Schema):
    club_by_id = fields.Int()


class Date_Request(Schema):
    sdt = fields.Int()

# EVENT REGISTRATION SCHEMA

class EventRegSchema_Request(Schema):
    name = fields.Str()
    about = fields.Str()
    sdt = fields.Float()
    edt = fields.Float()
    seats = fields.Int()
    venue = fields.Str()
    contacts = fields.Nested(ContactSchema_Request, many=True)
    lastregtime = fields.Float()
    image = fields.Str()


    @post_load
    def make_event(self,data):
        return EventRegSchema_class(**data)

class EventRegSchema_class(object):
    def __init__(self,name,about,sdt,venue,contacts,seats=None,image=None,edt=None,lastregtime=None):
        self.name = name
        self.about = about
        self.sdt = sdt
        self.edt = edt
        self.seats = seats
        self.venue = venue
        self.contacts = contacts
        self.lastregtime = lastregtime
        self.image = image


# organised_by = fields.Nested(OrganisedBySchema_Request, many=True)
# organised_for = fields.Nested(OrganisedForSchema_Request, many=True)

class GCM_Schema(Schema):
    gcmid = fields.Str()



class AdminSchema_Request(Schema):
    rollno = fields.Str()
    club_id = fields.Int()

class Forgot_Password(Schema):
    email = fields.Email()





contact_schema = ContactSchema_Request(many=True)
eventreg_schema = EventRegSchema_Request(partial=True)
club_schema = ClubRegSchema_Request()
info_schema = UserInfoSchema_Request()
gcm_schema = GCM_Schema()
forgot_pass = Forgot_Password()
admin_schema = AdminSchema_Request()
# class UserSchema(Schema):
# name = fields.Str()
# email = fields.Email()
# created_at = fields.DateTime()
# @post_load
# def make_user(self, data):
# return User(**data)
