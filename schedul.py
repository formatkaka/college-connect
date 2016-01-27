from datetime import datetime
import time
import os

from config import mail
from flask_mail import Message
from apscheduler.schedulers.background import BackgroundScheduler
import logging
logging.basicConfig()

def tick():
    msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
                  sender="college.connect01@gmail.com",
                  recipients=["college.connect28@gmail.com"])

    msg.body = "please click on the link "
    mail.send(msg)
    print "sent"

scheduler = BackgroundScheduler()
scheduler.add_job(tick, 'interval', seconds=10)
scheduler.start()

# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(tick, 'interval', seconds=10)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#     # scheduler.remove_all_jobs()
#     # print "done"
#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()
