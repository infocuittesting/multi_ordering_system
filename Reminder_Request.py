from Fetch_Current_Datetime import *
from sqlwrapper import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from apscheduler.schedulers.blocking import BlockingScheduler
#sched = BlockingScheduler()
def sendemailadmin(get_employee,msges):
                 print("hiiiiiiiii")
                 #email = ['infocuit.daisy@gmail.com','infocuit.aravindh@gmail.com']
                 name = "Hotel Manager"
                 print("message",msges)
                 message = "hotels"
                 conf_no = "343243245"
                 hotel_name = 'Quality in'
                 address = 'Chennai'
                 state = 'Tamilnadu'
                 country = 'India'
                 email = 'sedwe@gmail.com'
                 mobile1 = '9878909890'
                 mobile2 = '7898765678'
                 arrival = "mar 3"
                 depature = "mar 4"
                 room_type ="delux"
                 id1 = "324"
                 book_date = "2019-02-13"
                 
                 #print("daisy","infocuit.aravindh@gmail.com",type(email),"eruma suhutup","98789098","mar 2","mar 3", "delux")
                 sender = "infocuit.testing@gmail.com"
                 ids = id1
                 for i in get_employee:

                      receiver = i['employee_email']
                      #print(sender,type(sender),receiver,type(receiver))
                      subject = "Hotel Booking"
                      msg = MIMEMultipart()
                      msg['from'] = sender
                      msg['to'] = receiver
                      msg['subject'] = msges
                      print(ids)
                      html = """\
                      <!DOCTYPE html>
                      <html>
                      <head>
                      <meta charset="utf-8">
                      </head>
                      <body>
                      <dl>
                      <font size="3" color="black">Dear """+name+""",</font>
                      <dd><p><font size="3" color="black">I am writing this letter to inform you about delay request from multi ordering system.
                      Please take the action immediately, to close the guest request.
                      </font></p></dd>
                       
                     
                     
                     <dd>     
                     <font size="3" color="black">With best regards / Yours sincerely,</font></dd>
                     <dd>
                     <dd><font size="3" color="black">Hotel Manager</font></dt></dd>
                     
                     <dd>
                     <font size="3" color="black">Address:</font></dd>
                     <dd><font size="2.5" color="blue">"""+hotel_name+"""</font></dd>
                     <dd><font size="2.5" color="blue"> """+address+"""</font></dd>
                     <dd><font size="2.5" color="blue">"""+state+"""</font></dd>
                     <dd><font size="2.5" color="blue">"""+country+"""</font></dd>
                     <dd><font size="2.5" color="blue">"""+email+"""</font></dd>
                     <dd><font size="2.5" color="blue">"""+str(mobile1)+"""</font></dd>
                     <dd><font size="2.5" color="blue">"""+str(mobile2)+"""</font></dd>
                        
                      </dl>        
                      </body>
                      </html>
                      """

                      msg.attach(MIMEText(html,'html'))
                      
                      gmailuser = 'infocuit.testing@gmail.com'
                      password = 'infocuit@123'
                      server = smtplib.SMTP('smtp.gmail.com',587)
                      server.starttls()
                      server.login(gmailuser,password)
                      text = msg.as_string()
                      server.sendmail(sender,receiver,text)
                      print ("the message has been sent successfully")
                      server.quit()

#@sched.scheduled_job('interval', seconds=30)
def timed_job():
   string,string1,esca_string,esca_string1 = '','','',''
   today_date = application_datetime().strftime('%Y-%m-%d')
   today_datetime = datetime.datetime.strptime(application_datetime().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
   print("today_datetime", today_datetime, type(today_datetime))
   query_reminder_count = json.loads(dbget("select * from requests where date(current_datetime)='"+str(today_date)+"' and requests.request_status_id=1"))
   print(query_reminder_count)
   if len(query_reminder_count) != 0:        
    for query_reminder in query_reminder_count:
           initial = datetime.datetime.strptime(query_reminder['current_datetime'], "%Y-%m-%d %H:%M:%S")
           print('initial',initial, type(initial))
           current  = today_datetime - initial
           print(current)
           minutes = int(current.seconds % 3600 / 60.0)
           print("minutes",minutes)
           if 10 <= minutes < 20 :
               
                if query_reminder['reminder_count'] ==0:
                   if len(string) == 0:
                       string  = "'"+str(query_reminder['ticket_no'])+"'"
                   else:
                       string += ',' +"'"+str(query_reminder['ticket_no'])+"'"
                   print("ticket_no",string)
                   get_employee = json.loads(dbget("select employee_role.role_name, * from employee\
	                  left join employee_role on employee_role.role_id = employee.employee_role_id \
	                      where employee_dept_id in ("+str(query_reminder['department_no'])+")"))
                     
                   message = "reminder 1"
                   
                   var = sendemailadmin(get_employee,message)
           elif 20 <= minutes < 30 :
               if query_reminder['reminder_count'] ==1:
                   if len(string1) == 0:
                       string1  = "'"+str(query_reminder['ticket_no'])+"'"
                   else:
                       string1 += ',' +"'"+str(query_reminder['ticket_no'])+"'"
                   print("ticket_no",string1)
                   get_employee = json.loads(dbget("select employee_role.role_name, * from employee\
	                  left join employee_role on employee_role.role_id = employee.employee_role_id \
	                      where employee_dept_id in ("+str(query_reminder['department_no'])+")"))
                     
                   message = "reminder 2"
                   var = sendemailadmin(get_employee,message)
           elif 30 <= minutes < 40 :
               if query_reminder['escalation_count'] == 0:
                   if len(esca_string) == 0:
                       esca_string  = "'"+str(query_reminder['ticket_no'])+"'"
                   else:
                       esca_string += ',' +"'"+str(query_reminder['ticket_no'])+"'"
                   get_employee = json.loads(dbget("select employee_role.role_name, * from employee\
	                  left join employee_role on employee_role.role_id = employee.employee_role_id \
	                      where employee_dept_id in ("+str(query_reminder['department_no'])+")"))
                     
                   message= "escalation 1"
                   var = sendemailadmin(get_employee,message)
                           
                
           elif 40 >= minutes  :
              if query_reminder['escalation_count'] == 1:
                if len(esca_string1) == 0:
                       esca_string1  = "'"+str(query_reminder['ticket_no'])+"'"
                else:
                       esca_string1 += ',' +"'"+str(query_reminder['ticket_no'])+"'"
                get_employee = json.loads(dbget("select employee_role.role_name, * from employee\
	                  left join employee_role on employee_role.role_id = employee.employee_role_id \
	                      where employee_role_id  = 2"))
                message = "escalation 2"
                var = sendemailadmin(get_employee,message)
                 
           else:
               pass
    if len(string) == 0:
             pass
    else:
             dbput("update requests set reminder_count = reminder_count+'1'  where ticket_no in ("+str(string)+")")
             string = ''
    if len(string1) ==0:
        pass
    else:
        dbput("update requests set reminder_count = reminder_count+'1'  where ticket_no in ("+str(string1)+")")
        string1 = ''
    if len(esca_string) == 0:
        pass
    else:
        
      dbput("update requests set escalation_count = escalation_count+'1'  where ticket_no in( "+str(esca_string)+")")
      esca_string = ''
    if len(esca_string1) == 0:
        pass
    else:
        
      dbput("update requests set escalation_count = escalation_count+'1'  where ticket_no in( "+str(esca_string1)+")")
      esca_string1  = ''
              
         #print(current.strftime('%M'), type(current.strftime('%M')))
   else:
           pass
   return json.dumps({"Return":"Success"})
#sched.start()

