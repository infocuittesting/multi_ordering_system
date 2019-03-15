from Fetch_Current_Datetime import *
from sqlwrapper import *
import json
import datetime
import re
def Raise_Request(request):
    if request.method == 'POST':
        d = request.json
        d['read_status_id']= 2
        d['request_status_id'] = 1
        d['reminder_count'] = 0
        d['escalation_count'] = 0
        datetime_field = application_datetime()
        d['room_no'] = json.loads(dbget("select room_id from configure_alexa where alexa_app_id= '"+str(d['alexa_app_id'])+"'"))[0]['room_id']
        d['current_datetime']=(datetime_field.strftime("%Y-%m-%d %H:%M:%S"))
        get_items = json.loads(dbget("select * from configure_items where item_name = '"+str(d['request'])+"'"))
        d['department_no'] = get_items[0]['respective_dept_id']
        d['request_no'] =  get_items[0]['item_code']
        ticket_no = str((datetime_field).strftime("%Y-%m-%d%H:%M:%S"))+str(d['room_no'])+str(d['department_no'])+str(d['request_no'])
        d['ticket_no'] = re.sub("-|:","",ticket_no)
        d = {k:v  for k,v in d.items() if k not in ('alexa_app_id')}
        print(d)
        gensql('insert','requests',d)
        return (json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent=2))
    elif request.method == 'PUT':
        d = request.json
        dbput("update requests set read_status_id = '1',request_status_id = '2' where ticket_no = '"+str(d['ticket_no'])+"'")
        datetime_field = application_datetime()
        d['request_time']=(datetime_field.strftime("%Y-%m-%d %H:%M:%S"))
        d['read_status_id'] = '1'
        d['request_status_id'] = '2'
        gensql('insert','requests_log',d)
        return (json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent=4))


def Query_Request(request):
    if request.method == 'GET':
        
        all_data =  json.loads(dbget("	select date(current_datetime),configure_alexa.alexa_app_id,read_status_id.read_status,request_status_id.request_status,* from requests \
	left join read_status_id on read_status_id.read_status_id = requests.read_status_id \
	left join request_status_id on request_status_id.request_status_id = requests.request_status_id \
	left join configure_alexa on configure_alexa.room_id = requests.room_no"))
        return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":all_data,"Status": "Success","StatusCode": "200"},indent=4))
    elif request.method == 'POST':
       today_date = application_datetime().strftime('%Y-%m-%d') 
       all_datas = json.loads(dbget("select date(current_datetime),configure_alexa.alexa_app_id,read_status_id.read_status,request_status_id.request_status,* from requests \
	left join read_status_id on read_status_id.read_status_id = requests.read_status_id \
	left join request_status_id on request_status_id.request_status_id = requests.request_status_id \
	left join configure_alexa on configure_alexa.room_id = requests.room_no where date(current_datetime)='"+str(today_date)+"' and requests.read_status_id  = 2"))
       return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":all_datas,"Status": "Success","StatusCode": "200"},indent=4))
def Query_Requests_Log(request):
      if request.method == 'GET':
          ALL_DATA = json.loads(dbget("select requests.request,read_status_id.read_status,request_status_id.request_status,requests_log.* from requests_log \
                                       left join read_status_id on read_status_id.read_status_id = requests_log.read_status_id \
                                       left join request_status_id on request_status_id.request_status_id = requests_log.request_status_id \
                                       left join requests on requests.ticket_no = requests_log.ticket_no"))
          return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":ALL_DATA,"Status": "Success","StatusCode": "200"},indent=4))
      elif request.method == 'POST':
          d = request.json
          ALL_DATAs = json.loads(dbget("select requests.request,read_status_id.read_status,request_status_id.request_status,requests_log.* from requests_log \
                                       left join read_status_id on read_status_id.read_status_id = requests_log.read_status_id \
                                       left join request_status_id on request_status_id.request_status_id = requests_log.request_status_id \
                                       left join requests on requests.ticket_no = requests_log.ticket_no where requests_log.employee_email = '"+str(d['employee_email'])+"'"))
         
          return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":ALL_DATAs,"Status": "Success","StatusCode": "200"},indent=4))
