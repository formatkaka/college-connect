from __init__ import *
from config import *
from models import *

from schemas import *

class ClubRegistration(Resource):
	""" Register New Clubs """
	
	def post(self):
		json_data = request.get_json()
		data, errors = club_schema.load(json_data)
		if errors :
			return jsonify(errors)
		else :
			if ClubInfo.reg_club(data['name'],data['about']):
				return jsonify({"Status":"Club Saved"})
			else :
				return jsonify({"Status":"Some error occured"})

	# def get(self):
	# 	user = get_current_user()
	# 	if user:
	# 		return [json.dumps({"ClubName":item.clubName,"about":item.aboutClub}) for item in clubs]
	# 	else :
	# 		return jsonify({"Status":"Unauthorized access"})


class AdminRegistration(Resource):
	""" Give Admin access to registered user """

	def post(self):
		json_data = request.get_json()
		data, errors = club_schema.load(json_data)
		if errors :
			return jsonify(errors)
		else :
			s = UserInfo.query.filter_by(rollNo=data['rollno']).first()
			if s:
				student = UserReg.query.filter_by(id=s.user_id).first()
				
				club = ClubInfo.query.filter_by(clubName=data['clubname']).first()
				
				if club:
					admin = Admins(club_id=club.id,student_id=student.id)
					student.isadmin = True
					club.adminsList.append(admin)
					db.session.add([student,club])
					db.session.commit()
					return jsonify({"Status":"Admin added"})

				else :
					return jsonify({"Status":"No club with the name"})

			else :
				return jsonify({"Status":"No user exists with given roll number"})

