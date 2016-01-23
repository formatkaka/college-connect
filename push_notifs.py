# from models import GCMRegIds
from pushjack import *


# GCM API_KEY
def push_notif(message):
	client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')

	# abc = GCMRegIds.query.filter_by(id=1).one()

	# reg_ids = "du3sRJ52mRs:APA91bHQkitOjhZNtCh3NeavKryBPQFt6nlFcq-LbWMD2NQR3oIyEVmE0MZ6k6rJ2N71o-sBuBG_HIqivEuzsASSmI85Lo1eHJuSXLPYA3pDyPE5o5uxtlCYH6ur_jS8WeP6sVkQjsnZ"
	reg_ids = "dzE1l5awBr0:APA91bElQFZbT-iZX5WCGxVe_FUomE5WwsyhMGqCwqaBr8TTsyzGHzGNRAXCM3kGKZzMGc93geWh3CyrfWGRFS34_FpYjDA8hfD6QHLCaUZ1e6MOIl7BkC3UqTcPXrDhC1PunSpwWtk"
	alert = {'message': message}

	res = client.send(reg_ids,
				  alert
				  # delay_while_idle=True,
				  )



