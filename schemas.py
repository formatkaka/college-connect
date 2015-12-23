from marshmallow import fields, Schema


class UserInfoSchema(Schema):
	rollno = fields.Str()
	name = fields.Str()
	email = fields.Email()
	# dob = fields.DateTime()
	mobno = fields.Int()


class ClubRegSchema(Schema):
	name = fields.Str()
	about = fields.Str()


class EventRegSchema(Schema):
	name = fields.Str()
	about = fields.Str()
	sdate = fields.DateTime()
	edate = fields.DateTime()
	stime = fields.DateTime()
	etime = fields.DateTime()
	seats = fields.Int()
	venue = fields.Str()
	contacts = fields.Nested(ContactSchema, many=True)

class ContactSchema(Schema):
	contactname = fields.Str()
	contactnumber = fields.Int()

class AdminSchema(Schema):
	rollno = fields.Str()
	clubname = fields.Str()
	club_id = fields.Int()



event_schema = EventRegSchema()
club_schema = ClubRegSchema()
info_schema = UserInfoSchema()
# class UserSchema(Schema):
# name = fields.Str()
# email = fields.Email()
# created_at = fields.DateTime()
# @post_load
# def make_user(self, data):
# return User(**data)