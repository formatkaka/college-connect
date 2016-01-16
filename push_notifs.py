from pushjack import *

from models import GCMRegIds
# GCM API_KEY

client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')

abc = GCMRegIds.query.filter_by(id=1).one()

reg_ids = abc.data


res = client.send(reg_ids, 
				  alert,
				  delay_while_idle=True,
                  time_to_live=604800)