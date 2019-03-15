#import packages,and filename
from sqlwrapper import gensql,dbget,dbput
import json

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

