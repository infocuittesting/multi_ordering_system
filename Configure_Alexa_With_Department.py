#import packages,and filename
from sqlwrapper import gensql,dbget,dbput
import json
import requests
import datetime
from datetime import timedelta
from Fetch_Iso_Current_Datetime import *
def Insert_Configure_Alexa_With_Department(request):
     #configure alexa with hotelrooms
    try:

     d = request.json
     gensql('insert','configure_alexa',d)
     #print(d,type(d))
     return (json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent=2))
    except:
      return(json.dumps({"Return": "Record Failure","ReturnCode": "RF","Status": "Failure","StatusCode": "200"},indent=4))
  
def Update_Configure_Alexa_With_Department(request):
    # update configure alexa wth hotelrooms
    d  = request.json
    s = {k:v for k,v in d.items() if v!=""}
    e = {k:v for k,v in d.items() if k in ('config_alexa_id')}
    gensql('update','configure_alexa',s,e)
    return (json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent=4))

    
def Select_Configure_Alexa_With_Department():
    alexa_config = json.loads(gensql('select','configure_alexa','*'))
    return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":alexa_config,"Status": "Success","StatusCode": "200"},indent=4))

def Delete_Confgure_Alexa_With_Department(request):
    d = request.json
    dbput("delete from configure_alexa where config_alexa_id = '"+str(d['config_alexa_id'])+"'")
    return(json.dumps({"Return": "Record Deleted Successfully","ReturnCode": "RDS","Status": "Success","StatusCode": "200"},indent=4))




def Alexa_Notification(request):
   d = request.json
   get_id = json.loads(dbget("select * from configure_alexa where room_id='"+str(d['room_no'])+"'"))
   current_datetime=application_datetime()
   print(current_datetime[0])
   print(current_datetime[1])
   #print(d['user_Id'],type(d['user_Id']))
   url='https://api.amazon.com/auth/O2/token'
   headers = {
   'Content-Type': 'application/x-www-form-urlencoded',
   }
   payload={'grant_type':'client_credentials','client_id':get_id[0]['client_id'],
       'client_secret':get_id[0]['secret_id'],'scope':'alexa::proactive_events'
   }
   s = requests.post(url, headers=headers, data=payload)
   token_res = s.json()
   print(token_res['access_token'])
   request_header={'Authorization': 'Bearer {}'.format(token_res['access_token']),"Content-Type":"application/json"}
    
   if d['room_no']=='100':
       api_url='https://api.amazonalexa.com/v1/proactiveEvents/stages/development'
   else:
       api_url='https://api.eu.amazonalexa.com/v1/proactiveEvents/stages/development'





   notify_json = {


       "timestamp": str(current_datetime[0]),
       "referenceId": "orangetango2221800f44-436a-4c47-8d9f-e14356bb010c",


       "expiryTime": str(current_datetime[0]),
       "event": {

           "name": "AMAZON.MessageAlert.Activated",

           "payload": {

               "state": {

                   "status": "UNREAD",

                   "freshness": "NEW"

               },

               "messageGroup": {

                   "creator": {

                       "name": str(d['Object'])+"request has been closed"

                   },

                   "count": 1,

                   "urgency": "URGENT"

               }

           }

       },

       "relevantAudience": {

           "type": "Unicast",

           "payload": {

               "user":get_id[0]['alexa_app_id']
           }

       }

   }
   notifcation_send = requests.post(api_url,headers=request_header,json =notify_json )
   print("notification_send:",notifcation_send)
   return json.dumps({"Return": "Run Successfully"})
