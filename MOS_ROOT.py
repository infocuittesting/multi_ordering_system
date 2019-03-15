from flask import Flask,request
mos = Flask(__name__) #here i set environment varible for flask framework web application

#--------------configuration-------------------------------
from Configure_Alexa_With_Department import *
from Configure_Department import *
from Configure_Items import *

#-------------Signup----------------------------------------
from Employee_Signup import *
#----------------Raise Request------------------------------
from Raise_Request import *
#------------------Report----------------------------------
from Report_Service import *

#below i set path for web application

@mos.route("/",methods=['GET','POST'])
def mos_index():
    return "Hello MOS Manager"

@mos.route("/<string:name>",methods=['GET','POST'])
def pass_param(name):
    return (name)

#--------------Configure Alexa route------------------
@mos.route("/Configure_Insert_Alexa_With_Department",methods=['POST'])
def insertalexa():
    return (Insert_Configure_Alexa_With_Department(request))
@mos.route("/Configure_Update_Alexa_With_Department",methods=['POST'])
def updatealexa():
    return (Update_Configure_Alexa_With_Department(request))
@mos.route("/Configure_Select_Alexa_With_Department",methods=['GET','POST'])
def selectalexa():
    return(Select_Configure_Alexa_With_Department())
@mos.route("/Configure_Delete_Alexa_With_Department",methods=['POST'])
def deletealexa():
    return (Delete_Confgure_Alexa_With_Department(request))

#--------------Configure Department route--------------------
@mos.route("/Configure_Insert_Department",methods=['POST'])
def insertdept():
    return (Insert_Configure_Department(request))
@mos.route("/Configure_Update_Department",methods=['POST'])
def updatedept():
    return (Update_Configure_Department(request))
@mos.route("/Configure_Select_Department",methods=['GET','POST'])
def selectdept():
    return (Select_Configure_Department())
@mos.route("/Configure_Delete_Department",methods=['POST'])
def deletedept():
    return (Delete_Configure_Department(request))
#-------------Employee Signup--------------------------------
@mos.route("/Employee_Signup_Insert",methods=['POST'])
def insertemployee():
    return (Insert_Employee_Signup(request))
@mos.route("/Employee_Signup_Update",methods=['POST'])
def updateemployee():
    return (Update_Employee_Signup(request))
@mos.route("/Employee_Signup_Select",methods=['POST','GET'])
def selectemployee():
    return (Select_Employee_Signup(request))
@mos.route("/Employee_LoginandLogout",methods=['POST'])
def Loginemployee():
    return (Employee_Login(request))
@mos.route("/Employee_Log",methods=['POST','GET'])
def employee_logs():
    return (Employee_Log(request))

#-------------------Configure Items--------------------------
@mos.route("/Configure_Insert_Items",methods=['POST'])
def insertfooditems():
    return (Insert_Configure_Items(request))
@mos.route("/Configure_Update_Items",methods=['POST'])
def updatefooditems():
    return (Update_Configure_items(request))
@mos.route("/Configure_Select_Items",methods=['GET','POST','DELETE'])
def selectallitems():
    return (Select_Configure_Items(request))

#-----------------------Raise Request---------------
@mos.route("/Raise_Request",methods=['POST','PUT'])
def guestrequest():
    return (Raise_Request(request))

@mos.route("/Query_Request",methods=['GET','POST'])
def queryrequest():
    return (Query_Request(request))

@mos.route("/Query_Requests_Activity_Log",methods=['GET','POST'])
def queryrequestlog():
    return (Query_Requests_Log(request))


#-----------------------Report----------------

@mos.route("/Query_Multi_Ordring_System_Report",methods=['POST'])
def queryreports():
    return (Query_All_Reports(request))
if __name__ == "__main__":
    mos.run(host ='192.168.99.1',port =5000)#run web application
