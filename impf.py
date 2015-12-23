from models import *
from config import *
from __init__ import *

def get_current_user():
	user = request.authorization
	username_or_token = user.username
	
	if UserReg.verify_auth_token(username_or_token):
		return UserReg.verify_auth_token(username_or_token)

	elif UserReg.query.filter_by(userName=username_or_token).first():
		return UserReg.query.filter_by(userName=username_or_token).first()

	else :
		return None