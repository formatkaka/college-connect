from models import GCMRegIds
from pushjack import *


# GCM API_KEY
def push_notif(message):
	client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')

	abc = GCMRegIds.query.filter_by(id=1).one()

	reg_ids = abc.data
	alert = message

	res = client.send(reg_ids,
				  alert,
				  delay_while_idle=True,
                  time_to_live=604800)



