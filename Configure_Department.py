from sqlwrapper import *
import json
def Insert_Configure_Department(request):
    #configure department
   try:

     d = request.json
     get_dept_code = json.loads(gensql('select','department_code_num','*'))
     d['department_code'] = get_dept_code[0]['department_code']
     gensql('insert','department',d)
     dbput("update department_code_num set department_code = department_code + 1")
     #print(d,type(d))
     return (json.dumps({"Return": "Record Inserted Successfully","ReturnCode": "RIS","Status": "Success","StatusCode": "200"},indent=2))
   except:
      return(json.dumps({"Return": "Record Failure","ReturnCode": "RF","Status": "Failure","StatusCode": "200"},indent=4))
def Update_Configure_Department(request):
    d = request.json
    s = {k:v for k,v in d.items() if v!="" if k not in ('department_id')}
    e = {k:v for k,v in d.items() if k in ('department_id')}
    gensql('update','department',s,e)
    return (json.dumps({"Return": "Record Updated Successfully","ReturnCode": "RUS","Status": "Success","StatusCode": "200"},indent=4))

  
def Select_Configure_Department():
    dept_config = json.loads(gensql('select','department','*'))
    return (json.dumps({"Return": "Record Retrived Successfully","ReturnCode": "RRS","Returnvalue":dept_config,"Status": "Success","StatusCode": "200"},indent=4))

def Delete_Configure_Department(request):
    d = request.json
    dbput("delete from department where department_id = '"+str(d['department_id'])+"'")
    return(json.dumps({"Return": "Record Deleted Successfully","ReturnCode": "RDS","Status": "Success","StatusCode": "200"},indent=4))

