from sqlwrapper import *
from Fetch_Current_Datetime import *
import random
def Insert_Configure_Items(request):
    d = request.json
    d['item_name']=d['item_name'].title()
    d['item_code'] = random.randint(1000,9999)
    d['item_create_on']=application_datetime()
    gensql('insert','configure_items',d)     
    return (json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent=2))

def Update_Configure_items(request):
    d = request.json
    s = {k:v for k,v in d.items() if v!="" if k not in ('item_code')}
    e = {k:v for k,v in d.items() if k in  ('item_code')}
    gensql('update','configure_items',s,e)
    return (json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent=4))

def Select_Configure_Items(request):
    d = request.json
    if request.method=='GET':
       All_get_items = json.loads(dbget("Select department.department_name,employee.employee_name,employee.employee_email,  configure_items.* from configure_items \
	left join department on department.department_code = configure_items.respective_dept_id \
	left join employee on employee.employee_email = configure_items.item_created_by_id"))

       #view_request = json.loads(dbget("select department.department_name as view_department,view_request_dept.* from view_request_dept \
	     #                   left join department on department.department_code =view_request_dept.dept_id"))

       #for get_item in All_get_items:
          # for view in view_request:
              # if get_item['item_code'] == view['item_code']:
                 #  get_item['view_department'] = [view]


       return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":All_get_items,"Status": "Success","StatusCode": "200"},indent=4))

    elif request.method=='POST':
       All_get_items = json.loads(dbget("Select department.department_name,employee.employee_name,  configure_items.* from configure_items \
	left join department on department.department_code = configure_items.respective_dept_id \
	left join employee on employee.employee_email = configure_items.item_created_by_id where configure_items.item_code = '"+str(d['item_code'])+"'"))

       #view_request = json.loads(dbget("select department.department_name as view_department,view_request_dept.* from view_request_dept \
	#                        left join department on department.department_code =view_request_dept.dept_id where view_request_dept.item_code = '"+str(d['item_code'])+"'"))

      # for get_item in All_get_items:
        #   for view in view_request:
         #      if get_item['item_code'] == view['item_code']:
                 #  get_item['view_department'] = [view]


       return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":All_get_items,"Status": "Success","StatusCode": "200"},indent=4))
    elif request.method =='DELETE':
        print("delete working")
        dbput("delete from configure_items where item_code = '"+str(d['item_code'])+"';")
    return(json.dumps({"Return": "Record Deleted Successfully","ReturnCode": "RDS","Status": "Success","StatusCode": "200"},indent=4))
def Delete_Items(request):
    d = request.json
    print("delete working")
    dbput("delete from configure_items where item_code = '"+str(d['item_code'])+"';")
    return(json.dumps({"Return": "Record Deleted Successfully","ReturnCode": "RDS","Status": "Success","StatusCode": "200"},indent=4))



