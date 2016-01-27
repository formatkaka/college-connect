                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   from flask_mail import Message
from config import mail, app
from pushjack import GCMClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
import logging
logging.basicConfig()

client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')


def push_notif():
    # client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')

    # abc = GCMRegIds.query.filter_by(id=1).one()

    # reg_ids = "du3sRJ52mRs:APA91bHQkitOjhZNtCh3NeavKryBPQFt6nlFcq-LbWMD2NQR3oIyEVmE0MZ6k6rJ2N71o-sBuBG_HIqivEuzsASSmI85Lo1eHJuSXLPYA3pDyPE5o5uxtlCYH6ur_jS8WeP6sVkQjsnZ"
    # # reg_ids = "dzE1l5awBr0:APA91bElQFZbT-iZX5WCGxVe_FUomE5WwsyhMGqCwqaBr8TTsyzGHzGNRAXCM3kGKZzMGc93geWh3CyrfWGRFS34_FpYjDA8hfD6QHLCaUZ1e6MOIl7BkC3UqTcPXrDhC1PunSpwWtk"
    # alert = {'message': 'sg'}
    #
    # res = client.send([reg_ids],
    #                   alert
    #                   # delay_while_idle=True,
    #                   )
    # print res.successes
    # msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
    #           sender="college.connect01@gmail.com",
    #           recipients="college.connect28@gmail.com")
    #
    # msg.body = "please click on the link "
    # mail.send(msg)
    print "sent"

jobstores = {
    'default': SQLAlchemyJobStore(url='postgresql://postgres:1234@localhost:5432/databse')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20}
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler()
scheduler.configure( executors=executors, )
scheduler.add_jobstore('sqlalchemy', url=app.config['SQLALCHEMY_DATABASE_URI'])
# scheduler.add_executor(executors)

job = scheduler.add_job(push_notif)
# print type(job)
# GCM API_KEY
scheduler.start()
# scheduler.print_jobs()
# scheduler.print_jobs()
# scheduler.remove_all_jobs()
