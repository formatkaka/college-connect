# from datetime import datetime
# from threading import Thread, Timer
# from functools import wraps
# import time
# def tick():
#     print a.isAlive()
#     # msg = Message(subject="Thank You for Registration.Confirmation Link.Click Below.",
#     #               sender="college.connect01@gmail.com",
#     #               recipients=["college.connect28@gmail.com"])
#     #
#     # msg.body = "please click on the link "
#     # mail.send(msg)
#     print "sent"
#
#
# # a = Thread(group=None, target=tick )
#
# a = Timer(1, tick)
# print a.isAlive()
# # a = Thread(group=None, target=tick)
# a.daemon = True
# # a.run()
# print a.isAlive()
#
# # if __name__ =="__main__":
# a.run()
#
# try:
#     pass
# except KeyboardInterrupt:
#     pass

from threading import Thread

def hello():
    print "hello"



import time
# t.start()

while True:
    t = Thread(group=None, target=hello)
    t.daemon = True
    time.sleep(5)
    t.run()

# t = Timer(2.0, hello)
# t.start()
# hello()