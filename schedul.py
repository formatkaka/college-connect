# from datetime import datetime
# import time
# import os

# from config import mail
# from flask_mail import Message
# from apscheduler.schedulers.background import BackgroundScheduler
# import logging
# logging.basicConfig()

# def tick():
#     msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
#                   sender="college.connect01@gmail.com",
#                   recipients=["college.connect28@gmail.com"])

#     msg.body = "please click on the link "
#     mail.send(msg)
#     print "sent"

# scheduler = BackgroundScheduler()
# scheduler.add_job(tick, 'interval', seconds=10)
# scheduler.start()

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

from threading import Thread
import time
from datetime import datetime

check=[]                                 # Queue to be managed
check.append(("41", 1454087462.0))		 # Notif ("Message to be sent", Unix Timestamp)
check.append(("46", 1454087762.0))
check.append(("44", 1454087642.0))
check.append(("42", 1454087522.0))
check.append(("43", 1454087582.0))
check.append(("45", 1454087702.0))

def cron():
	check.sort(key=lambda tup: -tup[1])	#sorting of Queue ()

	first = check[-1]
	ct = first[1]

	while(True):						 
		if(time.time() >= ct):
			print(first[0]),			# GCM to be executed here
			print(" Done "),
			print(datetime.now())			
			check.pop()
			if not check:
				break
			first = check[-1]
			ct = first[1]
		print(first[0]),
		print(" "),
		print(datetime.now())
		time.sleep(15)							# Time Delay for time check 

def main():                                        # Code for the second thread
	thread_cron = Thread(target=cron, args=())
	thread_cron.start()
	while True:                                    # Placeholder code for main thread
		time.sleep(10)
		print("Running")

if __name__ == '__main__':
	main()