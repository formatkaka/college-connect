import logging, logging.handlers
class TitledSMTPHandler(logging.handlers.SMTPHandler):
    def getSubject(self, record):
        formatter = logging.Formatter(fmt=self.subject)
        return formatter.format(record)

# below is to test
logging.getLogger().addHandler(TitledSMTPHandler(
    ('smtp.gmail.com',587),
    'college.connect01@gmail.com', 'college.connect28@gmail.com',
    '%(asctime)s Error: %(message)s',
    ('college.connect01@gmail.com', 'collegeconnect1234'), ()
))