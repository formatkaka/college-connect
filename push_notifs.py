from models import GCMRegIds
from pushjack import *


# GCM API_KEY
def push_notif(message):
	client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')

	abc = GCMRegIds.query.filter_by(id=1).one()

	reg_ids = "du3sRJ52mRs:APA91bHQkitOjhZNtCh3NeavKryBPQFt6nlFcq-LbWMD2NQR3oIyEVmE0MZ6k6rJ2N71o-sBuBG_HIqivEuzsASSmI85Lo1eHJuSXLPYA3pDyPE5o5uxtlCYH6ur_jS8WeP6sVkQjsnZ"
	alert = message

	res = client.send(reg_ids,
				  alert,
				  delay_while_idle=True,
                  time_to_live=604800)



