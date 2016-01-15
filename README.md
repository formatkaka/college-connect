# college-connect

1. REGISTER USER(POST)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/user/reg

REQUEST -
* Add username and password in auth-headers
* json = {"name" : "FULL NAME",
          "rollno" : "ROLL NO",
          "mobno" : "MOBILE NO",
          "email" : "EMAIL_ID"
          }
RESPONSE-
 token
 
2. USER LOGIN(GET)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/user/reg

REQUEST -
* Add username and password in auth-headers

RESPONSE -
token

3.EVENT REGISTRATION(POST)

api_url = https://sheltered-fjord-8731.herokuapp.com/api/events/
REQUEST -
* Add username and password in auth-headers
* json = {"name" : "FULL NAME",
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
          "lastregtime":LAST REGISTRATION TIME(Unixstamp(Float))
          }

RESPONSE -
  event saved in json
  
4. EVENTS LIST(GET)
api_url = https://sheltered-fjord-8731.herokuapp.com/api/events/

REQUEST -
* Add username and password in auth-headers

RESPONSE -
{
    "events": [
        {
            "about": "", 
            "available_seats": , 
            "contacts": [
                {
                    "mobno": 1123, 
                    "name": "a"
                }, 
                {
                    "mobno": 1323, 
                    "name": "af"
                }
            ], 
            "createdby": "1", 
            "name": "", 
            "occupied_seats": , 
            "total_seats": , 
            "venue": "", 
            "verified": "False"
        }
    ]
}

EVENTS RESPONSE WILL BE ARRAY.

5. FOLLOWING/UNFOLLOWING  CLUB/EVENT

api_url = https://sheltered-fjord-8731.herokuapp.com/api/<S1>/<ID>/<S3>

S1 - club / event

ID - event / club id

S2 - follow / unfollow

REQUEST -
* Add username and password in auth-headers

RESPONSE - 
  Successfully followed/unfollowed response
  

P.S - 
  Apart from responses mentioned above , check exceptions file for error codes in case of error in any of the above
  request data.
  
  At present token shall be valid for 20 mins.
