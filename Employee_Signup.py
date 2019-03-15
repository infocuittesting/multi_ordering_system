from sqlwrapper import *
from Fetch_Current_Datetime import application_datetime
from sqlwrapper import gensql,dbget,dbput
import json
def Insert_Employee_Signup(request):
    #try:

     d = request.json

     d['enrolled_on'] = application_datetime()
     print(d)
     gensql('insert','employee',d)
     
     return (json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent=2))
  # except:
     # return(json.dumps({"Return": "Record Failure","ReturnCode": "RF","Status": "Failure","StatusCode": "200"},indent=4))

def Update_Employee_Signup(request):
    d = request.json
    print(d)
    emp_code = {k:v for k,v in d.items() if k in ('employee_email')}
    print(emp_code)
    emp_details = {k:v for k,v in d.items() if v!="" if k not in ('employee_email')}
    gensql('update', 'employee', emp_details, emp_code)
    return (json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent=4))

def Select_Employee_Signup(request):
    if request.method == 'GET':
       all_employees = json.loads(dbget("select employee_role.role_name,department.department_name,login_status.login_description,employee.* from employee \
	left join employee_role on employee_role.role_id = employee.employee_role_id \
	left join department on department.department_code = employee.employee_dept_id \
	left join login_status on login_status.login_status_id = employee.emp_status_id"))
       return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":all_employees,"Status": "Success","StatusCode": "200"},indent=4))
    else:
        d = request.json
        employee = json.loads(dbget("select employee_role.role_name,department.department_name,login_status.login_description,employee.* from employee \
	left join employee_role on employee_role.role_id = employee.employee_role_id \
	left join department on department.department_code = employee.employee_dept_id \
	left join login_status on login_status.login_status_id = employee.emp_status_id \
	where employee.employee_email = '"+str(d['employee_email'])+"'"))
        return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":employee,"Status": "Success","StatusCode": "200"},indent=4))

def Employee_Login(request):
    d = request.json
    pw = d['emp_password']
    emp_code = {k:v for k,v in d.items() if k in ('employee_email')}
    emp_status = {'emp_status_id':d['login_status_id']}
    if pw == json.loads(gensql('select','employee','emp_password',emp_code))[0]['emp_password']:
       d = {k:v for k,v in d.items() if k not in ('emp_password')}
       d['log_time'] = application_datetime()
       gensql('insert','employee_log',d)
       gensql('update','employee',emp_status, emp_code)
       
       return (json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent=2))
    else:
       return (json.dumps({"Return": "Record Not Inserted Successfully","ReturnCode": "RNIS","Status": "Success","StatusCode": "200"},indent=2))
        
def Employee_Log(request):
    if request.method == 'POST':
        print("its workng")
        d = request.json
        employee_log = json.loads(dbget("select login_status.login_description,employee.employee_name,employee_log.* from employee_log \
	left join employee on employee.employee_email = employee_log.employee_email \
	left join login_status on login_status.login_status_id =employee_log.login_status_id where employee_log.employee_email = '"+str(d['employee_email'])+"'"))
        return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":employee_log,"Status": "Success","StatusCode": "200"},indent=4))
       
    elif request.method =='GET':
        employee_log = json.loads(dbget("select login_status.login_description,employee.employee_name,employee_log.* from employee_log \
	left join employee on employee.employee_email = employee_log.employee_email \
	left join login_status on login_status.login_status_id =employee_log.login_status_id "))
        return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":employee_log,"Status": "Success","StatusCode": "200"},indent=4))
     
