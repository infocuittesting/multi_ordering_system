
from sqlwrapper import *
def Query_All_Reports(request):
    d = request.json
    request_based_reports,results_record = [],[]
    #Request Based report
    request_based = json.loads(dbget("select date(current_datetime),count(*) as requestcount,0 as  completecount\
	from requests \
      where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' and request_status_id = 1  group by date(current_datetime) order by date(current_datetime) "))
    compllete_based =json.loads(dbget("select date(current_datetime),count(*) as completecount,0 as  requestcount \
	from requests \
     where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' and request_status_id = 2  group by date(current_datetime) order by date(current_datetime) "))
  #  request_reports = request_based + compllete_based
    print("issdsa")
    print(request_based)
    from_date = datetime.datetime.strptime(d['datefrom'], '%Y-%m-%d').date()
    to_date=datetime.datetime.strptime(d['dateto'], '%Y-%m-%d').date()
    delta = to_date - from_date         # timedelta
    print(delta.days)
    
    
    for i in range(delta.days + 1):
        
            #print(request_rep['date'])
            print(from_date + datetime.timedelta(i))
           
            request_based_reports.append({"date":(from_date + datetime.timedelta(i)).strftime('%b %d'),
                                          "match_date":str(from_date + datetime.timedelta(i)),
                                          "request_count":0,
                                        "complete_count":0
                                        })
    for req_base in request_based_reports:
        for s in request_based:
            if req_base['match_date'] == s['date']:
                req_base['request_count']=s['requestcount']
    for req_base in request_based_reports:
        for l in compllete_based:
            
            if req_base['match_date'] ==l['date']:
                req_base['complete_count']=l['completecount']
                
    #Room based Report
    Room_based = json.loads(dbget("select room_no, count(*) from requests \
      where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' group by room_no"))
    
    #department based request count
    Department_based = json.loads(dbget("select department_name, count(*) from  requests \
	left join department on department.department_code = requests.department_no \
	 where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' group by department_name"))

    #device based report
    device_based_reports = json.loads(dbget("select configure_alexa.alexa_app_id, count(*) from requests \
	  left join configure_alexa on configure_alexa.room_id = requests.room_no \
	  where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' group by alexa_app_id"))
    if len(device_based_reports) == 0:
        pass
    else:
        
        devicess = 0
        for devs in device_based_reports:
            devicess += 1
            results_record.append({"device":"device"+str(devicess),"alexa_app_id":devs['alexa_app_id'],"count":devs['count']})
    #reminder based report

    reimnder_record = json.loads(dbget("select department_name,(select count(reminder_count) from requests where reminder_count = 1  ) as reminderone,(select count(reminder_count) from requests where reminder_count = 2  ) as remindertwo from  requests \
	left join department on department.department_code = requests.department_no \
	 where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' group by department_name"))
    

    #Escalation based report
    escalation_record = json.loads(dbget("select department_name,(select count(escalation_count) from requests where escalation_count = 1  ) as escalationone,(select count(escalation_count) from requests where escalation_count = 2  ) as escalationtwo from  requests \
	left join department on department.department_code = requests.department_no \
	 where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' group by department_name"))
    
    
    return (json.dumps({"Return": "Record Retrived Successfully",
                        "ReturnCode": "RRS",
                        "Request_based_report":request_based_reports,
                        "Room_based_report":Room_based,
                        "Dept_based_report":Department_based,
                        "Device_based_report":results_record,
                        "Reminder_based_report":reimnder_record,
                        "Escalation_based_report":escalation_record,
                        "Status": "Success","StatusCode": "200"},indent=4))
 
    

