# college-connect

1. REGISTER USER(POST)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/user/reg

REQUEST -
* Add email and password in auth-headers

* Request json = {
          "name" : "FULL NAME", 
          "rollno" : "ROLL NO",
          "mobno" : "MOBILE NO",
          "hostelname" : "HOSTEL NAME",
          "hostel_or_local":"BOOLEAN VALUE" # True if hostelite, False otherwise.
          }
RESPONSE -      
Response json = {
        "token" : "TOKEN"
                }
                
 
2. USER LOGIN(GET)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/user/token

REQUEST -
* Add email and password in auth-headers

RESPONSE -
Response json = {
        "token" : "TOKEN"
                }

3. USER UPDATE(PUT)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/user/edit

REQUEST - 
* Add email and password in auth-headers

* Request json will be same as the one in USER REG.

RESPONSE -
{"message":"success"}






3.EVENT REGISTRATION(POST)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/events/
REQUEST -
* Add username and password in auth-headers
* json = {
          "name" : "FULL NAME",
          "about":"ABOUT EVENT",
          "sdt":EVENT START TIME(Unixstamp(Float)),
          "edt":EVENT END TIME(Unixstamp(Float)),
          "venue":"EVENT VENUE",
          "contacts":[ 
                      {
                          "contactname":"CONTACT NAME",
                          "contactnumber":CONTACT NUMBER
                      },
                      {
                          "contactname":"CONTACT NAME",
                          "contactnumber":CONTACT NUMBER
                      }
                     ],
          "seats":SEATS, 
          "lastregtime":LAST REGISTRATION TIME(Unixstamp(Float)),
          "image":"IMAGE BASE64"
          }
#1 - Contact array must have minimum one contact.

RESPONSE -
  event_id will be returned if the event has been successfully saved.event_id must be saved offline.
  In case the admin wants to edit event details, the event_id must be sent along with json.
  
  
4. EVENTS LIST(GET)
api_url = https://sheltered-fjord-8731.herokuapp.com/api/events/

REQUEST -
* Add username and password in auth-headers

RESPONSE -
{
    "events": [
        {
            "name" : "EVENT_NAME", 
            "about" : "ABOUT_EVENT" , 
            "contacts" : [
                {
                    "mobno": MOB_NO, 
                    "name": "CONTACT_NAME"
                }, 
                {
                    "mobno": MOB_NO, 
                    "name": "CONTACT_NAME"
                }
            ],
            "total_seats" : TOTAL_SEATS,
            "occupied_seats" : OCCUPIED_SEATS, 
            "available_seats" : AVAILABLE_SEATS, 
            "sdt" : START_DATE_TIME(UnixTimeStamp) ,
            "edt" : END_DATE_TIME(UnixTimeStamp) ,
            "lrt" : LAST_REG_TIME(UnixTimeStamp) ,
            "club_id" : CLUB_ID , 
            "venue": "EVENT_VENUE", 
            "verified": "False",
            "event_id":EVENT_ID,
        }
    ]
}

#1. EVENTS RESPONSE WILL BE ARRAY.
#2. BEFORE ACCESSING THIS API, VERIFY IF EVENTS HAVE BEEN UPDATED THRU EVENT VERSION API.

5. FOLLOWING/UNFOLLOWING  CLUB/EVENT

api_url = https://sheltered-fjord-8731.herokuapp.com/api/event/event_id/S1

S1 - follow / unfollow

REQUEST -
* Add username and password in auth-headers

RESPONSE - 
  Successfully followed/unfollowed response

6. 

P.S - 
  Apart from responses mentioned above , check exceptions file for error codes in case of error in any of the above
  request data.
  
  At present token shall be valid for 20 mins.
