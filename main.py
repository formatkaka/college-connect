from __init__ import *
from config import *
from models import *
import os, flask, scrap
from flask.ext.mail import Message
from flask_mail import Message
import base64
from sqlalchemy import exc
from schemas import *
from opschemas import *
from flask.ext.restful import abort

class Testing(Resource):
    """Test Class for API"""

    def get(self):
        hello = '<h1>It Works!</h1>'
        response = flask.make_response(hello)
        response.headers['content-type'] = 'text/html'
        return response


class UserRegistration(Resource):
    """ API to register a new user or obtain token for a user"""

    def post(self):
        """ Register a user """

        user = request.authorization
        if not user:
            abort(401,message="ERR01")

        username = user.username
        password_hash = user.password
        json_data = request.get_json()
        data, errors = info_schema.load(json_data)

        if username == "" :  # Check if any of auth headers are empty
            abort(401,message="ERR02")

        if password_hash == "" :
            abort(401,message="ERR03")

        if errors:
            return jsonify(errors)

        if 'mobno' not in data.keys():
            data['mobno'] = None
            stat = UserReg.if_unique(data['rollno'], data['email'], data['mobno'])

        else:
            stat= UserReg.if_unique(data['rollno'], data['email'], data['mobno'])

        if stat:

            user_1 = UserReg(userName=username, passwordHash=password_hash, fullName=data['name']
                             , rollNo=data['rollno'], emailId=data['email'], mobNo=data['mobno'])
            db.session.add(user_1)
            db.session.commit()


            recieve = ["sid.siddhant.loya@gmail.com", "murali.prajapati555@gmail.com"]
            token = user_1.gen_auth_token()  # TODO : Report if info commit fails
            op = UserReg_class(200, user_1.userName, token)
            result = userreg_schema.dump(op)

            link = 'https://sheltered-fjord-8731.herokuapp.com/api/verify/' + base64.b64encode(email_id)

            msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
                          sender="college.connect28@gmail.com",
                          recipients=recieve)

            msg.body = "please click on the link {0}".format(link)
            mail.send(msg)

            return result.data

    def get(self):
        """ Obtain/Generate token for user """

        user, message = get_current_user()

        if user:
            token = user.gen_auth_token()

            op = UserReg_class(200, user.userName, token)
            result = userreg_schema.dump(op)
            return user.fullName

        else:
            return jsonify({"Status": message})


class ForgotPassword(Resource):
    """ API to Reset Password """

    pass


class UserInformation(Resource):
    """ API to GET user info """

    def post(self):
        return ({"Status": "Invalid Method."})

    def get(self):
        user = get_current_user()
        events_attending = [user.events[i].id for i in range(0,len(user.events))]
        clubs_following = [user.f_clubs[i].id for i in range(0,len(user.f_clubs))]
        events_created = EventsReg.query.filter_by(createdBy=user.id).all()
        my_events = [events_created[i].id for i in range(0,len(events_created))]
        club_admin = [user.a_clubs[i].id for i in range(0,len(user.a_clubs))]

        info = UserInfo_class(user.userName,user.fullName,user.rollNo,user.emailId,
                user.mobNo, club_admin, my_events, clubs_following, events_attending)

        result, errors = userinfo_schema.dump(info)
        if errors is None:
            return jsonify({"Errors":errors})
        else :
            return jsonify({"Information":result})
        # else:
        #     return jsonify({"Status": "Invalid"})


class UserUnique(Resource):
    """API to check whether username or password unique"""

    field = ["username"]

    def post(self, attr):
        return ({"Status": "Invalid Method."})

    def get(self, attr):
        user = request.authorization
        if attr == self.field[0]:
            username = UserReg.query.filter_by(userName=user.username).first()
            if username is None:
                return jsonify({"Status": "True"})
            else:
                return jsonify({"Status": "False"})

        else:
            abort(400,message="Invalid URL")


class EmailVerification(Resource):
    """API to Verify Email"""

    def post(self):
        return ({"Status": "Invalid Method."})

    def get(self, code):
        email = base64.b64decode(code)
        user = UserReg.query.filter_by(emailId=email).first()
        user.isVerified = True  # TODO: Checking Email
        db.session.add(user)
        db.session.commit()
        return "<center><h1>You're Now Verified User</h1></center>"


class EventRegistration(Resource):
    def post(self):
        user = get_current_user()
        
        json_data = request.get_json()
        data, errors = eventreg_schema.load(json_data)
        if errors:
            return jsonify(errors)
        else:
            # result = eventreg_schema.load()
            event = EventsReg.register_one(data.name,
                                               data.about,
                                               data.venue,
                                               conv_time(data.sdt),
                                               user,
                                               data.contacts,
                                               data.seats,
                                               conv_time(data.edt),
                                               conv_time(data.lastregtime)                                         
                                               )
            return jsonify({"status":"event saved"})



    def get(self):
        user= get_current_user()
        events_list = EventsReg.query.all()
        events = []
        for event in events_list:
            contacts = get_contact_info(event)
            e = Events_class(
                             event.eventName,
                             event.eventInfo,
                             event.eventVenue,
                             event.createdBy,
                             event.verified,
                             contacts,                                
                             event.totalSeats,
                             event.leftSeats,
                             event.occupiedSeats
                             
                             )
            events.append(e)
        result,errors = event_schema.dump(events)
        if errors is None:
            return {"Error":errors}
        else:
            return {"events": result}

        # events = Events.query.all()


class Clubsget(Resource):
    def post(self, s1, s2):
        return {"Staus": "Not allowed"}

    def get(self, s1, s2):
        user = get_current_user()
        if user:
            if s1 == "list":

                clubs_list = ClubInfo.query.all()

                clubs = []
                for club in clubs_list:
                    admins = get_admin_info(club)
                    c = Club_class(club.clubName, club.aboutClub, admins)
                    clubs.append(c)
                result = club_schema.dump(clubs)
                # if result.error == {}:
                return {"clubs": result.data}
            # else :
            # 	return {"error":result.error}
            elif s2 == "info" and club:
                result = userinfo_c_schema.dump(club)
                return result.data
            elif s2 == "events" and club:
                pass

        else:
            return jsonify({"Status": message})


class User_Follow_Status(Resource):
    
    def post(self, s1, event_or_club_id, s2):
        user = get_current_user()
        if user:

            if s1 == "club" and s2 == "follow":
                club = ClubInfo.query.filter_by(id=event_or_club_id).first()
                club.add_follower(user)
                return jsonify({"Status": "Successfully followed."})

            elif s1 == "event" and s2 == "follow":
                event = EventsReg.query.filter_by(id=event_or_club_id).first()
                stat = event.add_follower(user)
                return jsonify({"Status": "Successfully followed."})

            elif s1 == "club" and s2 == "unfollow":
                club = ClubInfo.query.filter_by(id=event_or_club_id).first()
                club.remove_follower(user)
                return jsonify({"Status": "Successfully unfollowed"})

            elif s1 == "event" and s2 == "unfollow":
                event = EventsReg.query.filter_by(id=event_or_club_id).first()
                event.remove_follower(user)
                return jsonify({"Status": "Successfully unfollowed"})

            else:
                return jsonify({"Status": "Invalid Request"})


        else:
            return jsonify({"Status": message})


sources = ["notice", "seminar", "quick"]


class WebScrap(Resource):
    def get(self, source):
        scrapper = scrap.Scrap()
        if source == sources[0]:
            return jsonify(scrapper.get_notice())
        elif source == sources[1]:
            return jsonify(scrapper.get_seminar())
        elif source == sources[2]:
            return jsonify(scrapper.get_quicks())
        else:
            return jsonify({"Status": 'Invalid request'})


class Testing1(Resource):
    def get(self):
        user,message = get_current_user()
        user = request.authorization
        # if not user.username:
        return str(user.username=="")
        # 	return "No username"
        # elif not user.password:
        # 	return "No password"
        # elif user.password == "null":
        # 	return "Token"
        # else:
        # 	return "OK"


# @api.errorhandler(500)
# def some_error():
# 	db.session.rollback()
# 	return "Retry"




api.add_resource(UserRegistration, '/api/user/reg')
api.add_resource(UserInformation, '/api/user/info')
api.add_resource(EventRegistration, '/api/events/')
api.add_resource(Clubsget, '/api/clubs/<string:s1>/<string:s2>')
api.add_resource(UserUnique, '/api/unique/<string:attr>')
api.add_resource(Testing, '/')
api.add_resource(WebScrap, '/api/scrap/<string:source>')
api.add_resource(User_Follow_Status, '/api/<string:s1>/<int:event_or_club_id>/<string:s2>')
api.add_resource(EmailVerification, '/api/verify/<string:code>')
api.add_resource(Testing1, '/api/test')

if __name__ == "__main__":
    # db.create_all()
    # manager.run()
    port = int(os.environ.get('PORT', 5432))
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(port=8080,debug=True)
