from __init__ import *
from config import *
from models import *
import os, flask, scrap
import base64
from schemas import *
from opschemas import *
from flask.ext.restful import abort
from push_notifs import push_notif
from sqlalchemy.exc import SQLAlchemyError
# from gmail_logs import *
from functools import wraps
from config import mail
from flask_mail import Message
import hashlib
import datetime
from threading import Thread
import time
from datetime import datetime
import settings

settings.init()
import signal
import time
import sys


# global checkList

# settings.checkList = Scheduler_list.query.filter_by(id=1).first().notverifiedNotifs
# print Scheduler_list.query.filter_by(id=1).first().notverifiedNotifs
# firstNotif = None
# requestedTime = None

class Testing(Resource):
    """Test Class for API"""

    def get(self):
        hello = '<h1>It Works!</h1>'
        response = flask.make_response(hello)
        response.headers['content-type'] = 'text/html'
        return response


class UserRegistration(Resource):
    """ API to register a new user or obtain token for a user"""

    def post(self, s1):
        """ Register a user """

        if s1 != "reg":
            abort(400)

        user = request.authorization

        if not user:
            abort(401, message="ERR01")

        email = user.username
        password_hash = user.password
        json_data = request.get_json()
        data, errors = info_schema.load(json_data)

        if email == "":  # Check if any of auth headers are empty
            abort(401, message="ERR02")

        if password_hash == "":
            abort(401, message="ERR03")

        if errors:
            return jsonify(errors)

        if UserReg.if_unique(data.rollno, email, data.mobno):
            try:
                if data.svnit == "true":
                    foo = True

                else:
                    foo = False
                user_1 = UserReg(passwordHash=password_hash, fullName=data.name
                                 , rollNo=data.rollno, emailId=email, mobNo=data.mobno,
                                 hostelName=data.hostelname, svnitOrNot=foo, metaData=data.metadata1)
                db.session.add(user_1)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                # logging.error(e)
                abort(500)

            recieve = [email]
            token = user_1.gen_auth_token(expiration=60 * 60 * 24 * 15)
            op = UserReg_class(token)
            result = userreg_schema.dump(op)

            s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 24 * 3)
            token = s.dumps({'id': user_1.id})

            link = 'https://sheltered-fjord-8731.herokuapp.com/verify/' + token

            msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
                          sender="college.connect01@gmail.com",
                          recipients=recieve)

            msg.body = "please click on the link {0}".format(link)
            mail.send(msg)

            return result.data
        # except SQLAlchemyError:
        #     db.session.rollback()
        #     abort(500)

        # except Exception as e:

        # 	try:
        # 		db.session.delete(user_1)
        # 		db.session.commit()
        # 	except:
        # 		db.session.rollback()
        # 	logging.error(e)
        # 	abort(500)

    def get(self, s1):
        """ Obtain/Generate token for user """
        if s1 != "token":
            abort(400)
        user = get_current_user()
        token = user.gen_auth_token(expiration=60 * 60 * 24 * 15)
        op = UserReg_class(token)
        result = userreg_schema.dump(op)
        return result.data

    def put(self, s1):
        if s1 != "edit":
            abort(400)
        user = get_current_user()
        json_data = request.get_json()
        data, errors = info_schema.load(json_data)
        if errors:
            return jsonify(errors)
        try:
            UserReg.if_unique(data.rollno, data.mobno, user)
            user.mobNo = data.mobno
            user.rollNo = data.rollno
            user.fullName = data.name
            db.session.add(user)
            db.session.commit()
        # except SQLAlchemyError:
        #     db.session.rollback()
        #     logging.error(e)
        #     abort(500)
        except Exception as e:
            # logging.error(e)
            abort(500)

        return jsonify({"message": "edited"})


class ForgotPassword(Resource):
    """ API to Reset Password """

    def post(self):
        json_data = request.get_json()
        data, errors = forgot_pass.load(json_data)
        if errors:
            return jsonify(errors)

        user = UserReg.query.filter_by(emailId=data['email']).first_or_404()

        s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 30)
        token = s.dumps({'id': user.id})

        link = 'https://sheltered-fjord-8731.herokuapp.com/reset/' + token

        msg = Message(subject="Reset password",
                      sender="college.connect01@gmail.com",
                      recipients=[data['email']])

        msg.body = "please click on the link {0}".format(link)
        mail.send(msg)
        return jsonify({"message": "email sent"})

    def get(self):
        pass


class UserInformation(Resource):
    """ API to GET user info """

    def get(self):
        user = get_current_user()
        events_attending = [user.events[i].id for i in range(0, len(user.events))]
        clubs_following = [user.f_clubs[i].id for i in range(0, len(user.f_clubs))]
        events_created = EventsReg.query.filter_by(createdBy=user.id).all()
        my_events = [events_created[i].id for i in range(0, len(events_created))]
        club_admin = [user.a_clubs[i].id for i in range(0, len(user.a_clubs))]

        info = UserInfo_class(user.fullName, user.rollNo, user.emailId, str(user.isVerified),
                              user.mobNo, club_admin, my_events, clubs_following, events_attending)

        data, errors = userinfo_schema.dump(info)
        if errors:
            return jsonify({"Errors": errors})
        else:
            return jsonify(data)
        # else:
        #     return jsonify({"message": "Invalid"})


class UserUnique(Resource):
    """API to check whether username or password unique"""

    field = ["email"]

    def get(self, attr):
        user = request.authorization
        if attr == self.field[0]:
            email = UserReg.query.filter_by(emailId=user.username).first()
            if email is None:
                return jsonify({"message": "True"})
            else:
                abort(409, message="ERR14")

        else:
            abort(400, message="Invalid URL")


class EmailVerification(Resource):
    """API to Verify Email"""

    # def post(self):
    #     return ({"message": "Invalid Method."})

    def get(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)

        except SignatureExpired:
            abort(400)

        except BadSignature:
            abort(400)

        user = UserReg.query.filter_by(id=data['id']).first_or_404()
        user.isVerified = True
        db.session.add(user)
        db.session.commit()

        hello = '<h1>You are now a verified user.</h1>'
        response = flask.make_response(hello)
        response.headers['content-type'] = 'text/html'
        return response


class EventCheck(Resource):
    def get(self, foo):
        if foo is "date":
            get_current_user()
            json_data = request.get_json()
            data, errors = date_schema.load(json_data)
            if errors:
                return jsonify(errors)
            date = data['date']
            date1 = conv_time(date) + datetime.timedelta(hours=1)
            date2 = conv_time(date) - datetime.timedelta(hours=1)
            eve_list = [eve.id for eve in
                        EventsReg.query.filter(EventsReg.startDateTime > date2, EventsReg.startDateTime < date1).all()]
            return jsonify({"message": eve_list})


        elif foo is "version":
            version = EventsVersion.get_event_version()
            return jsonify({"message": version})


        else:
            abort(400)


class EventRegistration(Resource):
    def post(self):
        user = get_current_user()
        if user.isVerified is False:
            abort(401, message="ERR08")
        json_data = request.get_json()
        data, errors = eventreg_schema.load(json_data)
        if errors:
            return jsonify(errors)
        else:
            # try:
            event, val = EventsReg.register_one(data.name,
                                                data.about,
                                                data.venue,
                                                conv_time(data.sdt),
                                                user,
                                                data.contacts,
                                                data.image,
                                                data.seats,
                                                conv_time(data.edt),
                                                conv_time(data.lastregtime),
                                                conv_time(data.notifone),
                                                conv_time(data.notiftwo),
                                                data.notifmessage,
                                                data.prize,
                                                data.fees,
                                                data.color,
                                                )
            if val: push_notif(event.id, event.eventName, data.sdt)

            return jsonify({"message": event.id})

    def get(self):
        events_list = EventsReg.query.filter_by(verified=True).all()
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
                event.clubName,
                event.id,
                conv_time(event.startDateTime),
                event.e_clubs[0].id,
                event.createdTime,
                event.imageLink,
                conv_time(event.endDateTime),
                conv_time(event.lastRegDateTime),
                event.totalSeats,
                event.leftSeats,
                event.occupiedSeats,
                event.eventPrizeMoney,
                event.eventRegFees,
                event.eventColorHex,
            )
            events.append(e)

        result, errors = event_schema.dump(events)
        return {"events": result}

    # events = Events.query.all()
    def put(self):
        user = get_current_user()
        json_data = request.get_json()
        data, errors = eventreg_schema.load(json_data)
        if errors:
            return jsonify(errors)

        eve = EventsReg.query.filter_by(id=data.eventid).first_or_404()
        eve.eventName = data.name
        eve.eventInfo = data.about
        eve.eventVenue = data.venue
        eve.startDateTime = conv_time(data.sdt)
        eve.user = user
        eve.image = data.image
        eve.edit_seats(data.seats)
        eve.totalSeats = data.seats
        eve.startDateTime = conv_time(data.sdt)
        # eve.reschedule_gcm(conv_time(data.sdt))
        eve.lastRegDateTime = conv_time(data.lastregtime)
        eve.endDateTime = conv_time(data.edt)
        eve.edit_contacts(data.contacts)
        db.session.add(eve)
        db.session.commit()
        return jsonify({"message": "success"})


class Clubsget(Resource):
    def get(self):
        clubs_list = ClubInfo.query.all()
        indiv = ClubInfo.query.filter_by(id=1).first()
        clubs_list.remove(indiv)
        clubs = []
        for club in clubs_list:
            admins = get_admin_info(club)
            events = [club.eventsList[i].id for i in range(0, len(club.eventsList))]
            c = Club_class(club.clubName, club.aboutClub, admins, events, club.id, club.clubImage)
            clubs.append(c)
        result = club_schema.dump(clubs)
        # if result.error == {}:
        return {"clubs": result.data}


class User_Follow_message(Resource):
    def post(self, s1, event_or_club_id, s2):
        user = get_current_user()
        if user:

            if s1 == "club" and s2 == "follow":
                club = ClubInfo.query.filter_by(id=event_or_club_id).first_or_404()
                club.add_follower(user)
                return jsonify({"message": "Successfully followed."})

            elif s1 == "event" and s2 == "follow":
                event = EventsReg.query.filter_by(id=event_or_club_id).first_or_404()
                event.add_follower(user)
                return jsonify({"message": "Successfully followed."})

            elif s1 == "club" and s2 == "unfollow":
                club = ClubInfo.query.filter_by(id=event_or_club_id).first_or_404()
                club.remove_follower(user)
                return jsonify({"message": "Successfully unfollowed"})

            elif s1 == "event" and s2 == "unfollow":
                event = EventsReg.query.filter_by(id=event_or_club_id).first_or_404()
                event.remove_follower(user)
                return jsonify({"message": "Successfully unfollowed"})

            else:
                return jsonify({"message": "Invalid Request"})


sources = ["notice", "seminar", "quick"]


class GCMessaging(Resource):
    def post(self):
        json_data = request.get_json()
        data, errors = gcm_schema.load(json_data)
        my_gcm = data['gcmid']
        gcm_id_arr = GCMRegIds.query.filter_by(id=1).first()
        if not my_gcm in gcm_id_arr.data:
            gcm_id_arr.data.append(my_gcm)
            try:
                db.session.add(gcm_id_arr)
                db.session.commit()
            except:
                db.session.rollback()
                abort(500)
        return jsonify({"message": "saved"})

    # except:
    #     abort(500, message="ERR")


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
            return jsonify({"message": 'Invalid request'})


class AddRemoveAdmin(Resource):
    def post(self):
        json_data = request.get_json()
        data, errors = admin_schema.load(json_data)
        if errors:
            return jsonify(errors)
        else:
            club = ClubInfo.query.filter_by(id=data['club_id']).first_or_404()
            user = UserReg.query.filter_by(rollNo=data['rollno']).first_or_404()
            if not user.isVerified:
                abort(401, message="ERR08")
            if user.isAdmin:
                abort(409, message="ERR26")
            else:
                club.adminsList.append(user)
                user.isAdmin = True
                db.session.add_all([club, user])
                db.session.commit()
                return jsonify({"message": "admin added"})


class Notice(Resource):
    def post(self):
        user = get_current_user()
        user.is_council_admin()
        json_data = request.get_json()
        data, errors = noticereg_schema.load(json_data)
        notice = NoticeSection(noticeTitle=data.name, aboutNotice=data.about,
                               noticeImage=data.image, createdBy=user.id)
        db.session.add(notice)
        db.session.commit()
        push_notif("{0}".format(data.name))
        return jsonify({"message": "success"})

    def put(self):
        pass

    def get(self):
        notices_list = NoticeSection.query.all()
        notices = []
        for notice in notices_list:
            user = UserReg.query.filter_by(id=notice.createdBy).first()
            n = Notice_class(name=notice.noticeTitle, time=conv_time(notice.createdTime),
                             creator=user.fullName, about=notice.aboutNotice,
                             image=notice.noticeImage)
            notices.append(n)
        result = notice_schema.dump(notices)
        return jsonify({"notices": result.data})


class Testing1(Resource):
    def get(self):
        # json_data = request.get_json()
        # data, errors = abc_sch.load(json_data)
        return ({"image": "sdg"})

    # user = get_current_user()
    # if user:
    # json_data = request.get_json()
    # base = json_data['file']
    # drive = DriveApi()
    # flag = drive.upload(base, 'qwerty')
    # if flag:
    # 	return jsonify({"Status": "Success"})
    # else:
    # 	return jsonify({"Status": "Upload Failed."})


class Reauthenticate(Form):
    new_password = PasswordField('Enter new password', validators=[DataRequired()])
    re_password = PasswordField('Re-enter new password', validators=[DataRequired(), EqualTo('new_password',
                                                                                             message=' New Passwords do not match')])
    submit = SubmitField('Change Password')


@app.route('/reset/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        user = UserReg.query.filter_by(id=data['id']).first_or_404()
    except:
        abort(400)
    form = Reauthenticate()
    if form.validate_on_submit():
        user.passwordHash = hashlib.sha1(form.new_password.data).hexdigest()
        db.session.add(user)
        db.session.commit()
        flash('Password Changed')
        return render_template('reset.html')

    return render_template('reset.html', form=form)


def exit_gracefully(self, signum, frame):
    kill_now = True
    print "Outside while"
    while True:
        time.sleep(1)
        print("killlllling")
        if kill_now:
            break


def cron():
    # global checkList


    while (True):
        foo = Scheduler_list.query.filter_by(id=1).first()
        # checkList = settings.checkList
        # checkList = foo.notverifiedNotifs
        print "NO WHERE"
        print settings.checkList

        if settings.checkList == []:
            print "IF"
            print settings.checkList
            time.sleep(30)
        else:
            print "ELSE"
            print settings.checkList
            print Scheduler_list.query.filter_by(id=1).first().notverifiedNotifs

            settings.checkList.sort(key=lambda tup: -float(tup[1]))
            firstNotif = settings.checkList[-1]
            notif_message = firstNotif[0]
            notif_time = float(firstNotif[1])
            if (time.time() >= notif_time):
                # print notif_time
                send_mail()
                # push_notif(notif_message)
                # print checkList
                try:
                    # settings.checkList.remove(firstNotif)
                    foo.notverifiedNotifs.remove(firstNotif)

                    db.session.add(foo)
                    db.session.commit()
                    settings.checkList = Scheduler_list.query.filter_by(id=1).first().notverifiedNotifs
                    print "committed"
                    print settings.checkList
                    print Scheduler_list.query.filter_by(id=1).first().notverifiedNotifs
                    notif_time = None
                except:
                    pass
        # foo = foo_bar()
        # foo = Scheduler_list.query.filter_by(id=1).first()
        time.sleep(60)


def send_mail():
    msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
                  sender="college.connect01@gmail.com",
                  recipients=["siddhantloya2008@gmail.com"])

    msg.body = "please click on the link "
    with app.app_context():
        mail.send(msg)
    print "sent"


# send_mail()
api.add_resource(UserRegistration, '/api/user/<string:s1>')
api.add_resource(UserInformation, '/api/user/info')
api.add_resource(EventRegistration, '/api/events')
api.add_resource(Clubsget, '/api/clubs/list')
api.add_resource(UserUnique, '/api/unique/<string:attr>')
api.add_resource(Testing1, '/test')
api.add_resource(WebScrap, '/api/scrap/<string:source>')
api.add_resource(User_Follow_message, '/api/<string:s1>/<int:event_or_club_id>/<string:s2>')
api.add_resource(EmailVerification, '/verify/<string:token>')
# api.add_resource(NotificationCron, '/api/test')
api.add_resource(GCMessaging, '/api/gcm')
api.add_resource(ForgotPassword, '/api/password')
api.add_resource(AddRemoveAdmin, '/api/admin')
api.add_resource(EventCheck, '/api/check/<string:foo>')
api.add_resource(Notice, '/api/notice')
api.add_resource(Testing, '/')

if __name__ == "__main__":
    # manager.run()
    # db.create_all ()

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=8080, debug=True)
    # except Keyboard   Interrupt:
    # 	raise KeyError('j')

    # TODO - 1. not,None
    # TODO - 2. imports
    # TODO - 3. Events Version
    # TODO - 4. Flush, No result error(first_or_404)
    # TODO - 5. Update Cron with gcm (For now send to all users. Customised notification by ID can be done later by saving ids to database and accessing them in cron)
    # TODO - 6. Remove OrgBy
    # TODO - 7. filter_by , first
