from pushjack import GCMClient
from models import GCMRegIds
from config import db
from gmail_logs import *
import time
# arr=[]
# for i in range(0,1005):
#     arr.append("{0}".format(i))



def push_notif(eve_id,title,eve_time):
    client = GCMClient(api_key='AIzaSyBEJoy74kmV32OCl8NdrEBC6cbRV8EqEbo')
    abc = GCMRegIds.query.filter_by(id=1).one()
    # reg_ids = "du3sRJ52mRs:APA91bHQkitOjhZNtCh3NeavKryBPQFt6nlFcq-LbWMD2NQR3oIyEVmE0MZ6k6rJ2N71o-sBuBG_HIqivEuzsASSmI85Lo1eHJuSXLPYA3pDyPE5o5uxtlCYH6ur_jS8WeP6sVkQjsnZ"
    # reg_ids = "dzE1l5awBr0:APA91bElQFZbT-iZX5WCGxVe_FUomE5WwsyhMGqCwqaBr8TTsyzGHzGNRAXCM3kGKZzMGc93geWh3CyrfWGRFS34_FpYjDA8hfD6QHLCaUZ1e6MOIl7BkC3UqTcPXrDhC1PunSpwWtk"
    # reg_ids = "cwpbqZlk7mI:APA91bF_zSd5vd7gP1jUXwm8eXvaXshtUjMIMfA4ROOHdEqm-017auybSCarAx_waL0Qc7X-d9eyIkH8rXLOcSl2glp5ScPh0I_Rs7Xj19p9DccAO_vmFN_4x89MeQHPWyL1Ipx6LeE8"
    alert = {'id':eve_id,'title':title,'time':eve_time}

    res = client.send(abc.data,
                      alert,
                      collapse_key='{0}'.format(time.time())

                      )
    print res.responses
    print res.errors
    ## Catching exceptions

    #1 - GCM Device Unregistered
    for err in res.errors:
        if err.code == "NotRegistered" or err.code == "InvalidRegistration":
            abc.data.remove(err.identifier)

            print abc.data

        if err.code == "Unavailable" or err.code == "InvalidTtl":
            ### ADD TO SCHEDULER ###
            pass

    #2 - CANONICAL IDS

    for ids in res.canonical_ids:
        abc.data.remove(ids.old_id)
        abc.data.append(ids.new_id)
        db.session.add(abc)

    db.session.commit()


if __name__ == "__main__":
    push_notif("hello")