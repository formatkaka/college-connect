#####################
#### O/P Schemas ####
#####################

from marshmallow import fields, Schema

##### User Registration #####
class UserReg_class():
	def __init__(self,status_code,username,token):
		self.status_code = status_code
		self.username = username
		self.token = token

class UserReg_Response(Schema):
	status_code = fields.Int()
	username = fields.Str()
	token = fields.Str()


##### User Information #####

# 1 - Personal Info

class UserInfo_P_class():
	def __init__(self,status_code,name,rollno,email,mobno):
		self.status_code = status_code
		self.name = name
		self.rollno = rollno
		self.email = email
		self.mobno = mobno


class UserInfo_P_Response(Schema):
	status_code = fields.Int()
	name = fields.Str()
	rollno = fields.Str()
	email = fields.Email()
	mobno = fields.Int()

# 2 - Clubs/Events
	
class Nested_output():
	def __init__(self,status_code,my_arr):
		self.status_code = status_code
		self.my_arr = my_arr



class Nested_response(Schema):
	clubName = fields.Str()
	aboutClub = fields.Str()

class Error_Response(Schema):
	status_code = fields.Int()
	err_message = fields.Str()
	extra_1 = fields.Str()
	extra_2 = fields.Str()

userreg_schema = UserReg_Response()
err_schema = Error_Response()
userinfo_p_schema = UserInfo_P_Response()
userinfo_c_schema = Nested_response(many=True)