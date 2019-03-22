from sqlwrapper import *
def Query_All_Reports(request):
    d = request.json
    request_based_reports = []
    #Request Based report
    request_based = json.loads(dbget("select date(current_datetime), (select count(request_status_id) from requests where request_status_id = 1  ) as requestcount,\
	(select count(request_status_id) from requests where request_status_id = 2  ) as completecount\
	from requests \
      where date(current_datetime) between '"+d['datefrom']+"' and '"+d['dateto']+"' group by room_no,date(current_datetime) order by date(current_datetime) "))
    from_date = datetime.datetime.strptime(d['datefrom'], '%Y-%m-%d').date()
    to_date=datetime.datetime.strptime(d['dateto'], '%Y-%m-%d').date()
    delta = to_date - from_date         # timedelta
    print(delta.days)
    for request_rep in request_based:
        for i in range(delta.days + 1):
            #print(i)
            #print(from_date + datetime.timedelta(i))
            if request_rep['date'] == str(from_date + datetime.timedelta(i)):
                 request_based_reports.append({"date":(from_date + datetime.timedelta(i)).strftime('%b %d'),
                                        "request_count":request_rep['requestcount'],
                                        "complete_count":request_rep['completecount']
                                        })
            else:
                   request_based_reports.append({"date":(from_date + datetime.timedelta(i)).strftime('%b %d'),
                                        "request_count":0,
                                        "complete_count":0
                                        })                    
            

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
                        "Device_based_report":device_based_reports,
                        "Reminder_based_report":reimnder_record,
                        "Escalation_based_report":escalation_record,
                        "Status": "Success","StatusCode": "200"},indent=4))
 
    

