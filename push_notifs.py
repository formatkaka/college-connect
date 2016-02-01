from pushjack import GCMClient
from models import GCMRegIds
from gmail_logs import *

arr=[]
for i in range(0,1005):
    arr.append("{0}".format(i))



def push_notif(message):
    client = GCMClient(api_key='AIzaSyCqASidjonjOKkFmtChfFJ2xC5NWWNthRo')

    abc = GCMRegIds.query.filter_by(id=1).one()
    # reg_ids = "du3sRJ52mRs:APA91bHQkitOjhZNtCh3NeavKryBPQFt6nlFcq-LbWMD2NQR3oIyEVmE0MZ6k6rJ2N71o-sBuBG_HIqivEuzsASSmI85Lo1eHJuSXLPYA3pDyPE5o5uxtlCYH6ur_jS8WeP6sVkQjsnZ"
    # reg_ids = "dzE1l5awBr0:APA91bElQFZbT-iZX5WCGxVe_FUomE5WwsyhMGqCwqaBr8TTsyzGHzGNRAXCM3kGKZzMGc93geWh3CyrfWGRFS34_FpYjDA8hfD6QHLCaUZ1e6MOIl7BkC3UqTcPXrDhC1PunSpwWtk"
    alert = message

    res = client.send(abc.data,
                      alert
                      # delay_while_idle=True,
                      )


    ## Catching exceptions

    #1 - GCM Device Unregistered
    for err in res.errors:
        if err.code == "NotRegistered" or err.code == "InvalidRegistration":
            abc.data.remove(err.identifier)
            # db.session.add(abc)
            print abc.data

        if err.code == "Unavailable" or err.code == "InvalidTtl":
            ### ADD TO SCHEDULER ###
            pass

    #2 - CANONICAL IDS

    for ids in res.canonical_ids:
        abc.data.remove(ids.old_id)
        abc.data.append(ids.new_id)
        # db.session.add(abc)

    # db.session.commit()


if __name__ == "__main__":
    push_notif("hello")