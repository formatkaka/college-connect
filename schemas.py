from marshmallow import fields, Schema, post_load

## USER REGISTRATION SCHEMA


class UserInfoSchema_Request(Schema):
    rollno = fields.Str()
    name = fields.Str()
    email = fields.Email()
    mobno = fields.Int()

    @post_load
    def make_event(self,data):
        return UserInfo_class(**data)

class UserInfo_class(object):
    def __init__(self,email,rollno,name=None,mobno=None):
        self.name = name
        self.email = email
        self.rollno = rollno
        self.mobno = mobno


class ClubRegSchema_Request(Schema):
    name = fields.Str()
    about = fields.Str()


class ContactSchema_Request(Schema):
    contactname = fields.Str()
    contactnumber = fields.Int()


class OrganisedBySchema_Request(Schema):
    club_by_id = fields.Int()


class OrganisedForSchema_Request(Schema):
    clubs_for_id = fields.Int()

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

    @post_load
    def make_event(self,data):
        return EventRegSchema_class(**data)

class EventRegSchema_class():
    def __init__(self,name,about,sdt,seats,venue,contacts,edt=None,lastregtime=None):
        self.name = name
        self.about = about
        self.sdt = sdt
        self.edt = edt
        self.seats = seats
        self.venue = venue
        self.contacts = contacts
        self.lastregtime = lastregtime


# organised_by = fields.Nested(OrganisedBySchema_Request, many=True)
# organised_for = fields.Nested(OrganisedForSchema_Request, many=True)

class GCM_Schema(Schema):
    gcmid = fields.Str()



class AdminSchema_Request(Schema):
    rollno = fields.Str()
    clubname = fields.Str()
    club_id = fields.Int()

class Forgot_Password(Schema):
    email = fields.Email()
    rollno = fields.Str()

contact_schema = ContactSchema_Request(many=True)
eventreg_schema = EventRegSchema_Request(partial=True)
club_schema = ClubRegSchema_Request()
info_schema = UserInfoSchema_Request()
gcm_schema = GCM_Schema()
forgot_pass = Forgot_Password()
# class UserSchema(Schema):
# name = fields.Str()
# email = fields.Email()
# created_at = fields.DateTime()
# @post_load
# def make_user(self, data):
# return User(**data)
