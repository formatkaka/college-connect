import logging

# import socket
logging.basicConfig()
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, current_app
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import db, app



class APScheduler(object):
    def __init__(self, app=None):
        if not isinstance(app, Flask):
            raise TypeError('app must be flask application')
        self.app = app
        self.__scheduler = BackgroundScheduler(daemon=False)
        # self.app.apscheduler = self

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

        self.__scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    def run_job(self, func, job_id=None, date=None, message=None, eve=None, trigger=None):
        self.__scheduler.add_job(func, trigger, run_date=date, args=[message], id=job_id)

        if not eve.data:
            eve.scheduler_ids = [str(id)]
        else:
            eve.scheduler_ids.append(str(id))
        db.session.add(eve)
        db.session.commit()
        self.__scheduler.start()


    def delete_job(self, job_id):
        self.__scheduler.remove_job(job_id)
        return True


scheduler = APScheduler(app)


# print type(app)



# scheduler.run_job(tick)

# This is here to simulate application activity (which keeps the main thread alive).
# try:
#     # This is here to simulate application activity (which keeps the main thread alive).
#     while True:
#         time.sleep(2)
# except (SystemExit):
#     # Not strictly necessary if daemonic mode is enabled but should be done if possible
#     scheduler.shutdown()
