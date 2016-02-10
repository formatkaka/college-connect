# import logging, logging.handlers
# class TitledSMTPHandler(logging.handlers.SMTPHandler):
#     def getSubject(self, record):
#         formatter = logging.Formatter(fmt=self.subject)
#         return formatter.format(record)
#
# # below is to test
# logging.getLogger().addHandler(TitledSMTPHandler(
#     ('smtp.sendgrid.com',465),
#     'college.connect01@gmail.com', 'college.connect28@gmail.com',
#     '%(asctime)s Error: %(message)s',
#     ('collegeconnect', 'collegeconnect1234'), ()
# ))
#
# logging.error("sjdgfs")