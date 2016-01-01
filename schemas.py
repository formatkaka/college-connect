from marshmallow import fields, Schema


class UserInfoSchema_Request(Schema):
	rollno = fields.Str()
	name = fields.Str()
	email = fields.Email()
	# dob = fields.DateTime()
	mobno = fields.Int()


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

class EventRegSchema_Request(Schema):
	name = fields.Str()
	about = fields.Str()
	sdt = fields.Float()
	edt = fields.Float()
	seats = fields.Int()
	venue = fields.Str()
	contacts = fields.Nested(ContactSchema_Request,many=True)
	# organised_by = fields.Nested(OrganisedBySchema_Request, many=True)
	# organised_for = fields.Nested(OrganisedForSchema_Request, many=True)



class AdminSchema_Request(Schema):
	rollno = fields.Str()
	clubname = fields.Str()
	club_id = fields.Int()


contact_schema = ContactSchema_Request(many=True)
event_schema = EventRegSchema_Request()
club_schema = ClubRegSchema_Request()
info_schema = UserInfoSchema_Request()
# class UserSchema(Schema):
# name = fields.Str()
# email = fields.Email()
# created_at = fields.DateTime()
# @post_load
# def make_user(self, data):
# return User(**data)