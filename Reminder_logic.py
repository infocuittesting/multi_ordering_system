from Fetch_Current_Datetime import *
from sqlwrapper import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
def sendemailadmin(get_employee):
                 #email = ['infocuit.daisy@gmail.com','infocuit.aravindh@gmail.com']
                 name = "daisy"
                 message = "Booking Confirmed"
                 conf_no = "343243245"
                 hotel_name = "SMARTMO"
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
                      msg['subject'] = subject
                      print(ids)
                      html = """\
                      <!DOCTYPE html>
                      <html>
                      <head>
                      <meta charset="utf-8">
                      </head>
                      <body>
                      <dl>
                      <dt>
                      <pre>
               
                      
                      <font size="4" color="black">Dear """+name+""",</font>
                      <font size="4" color="black">      We are delighted that you have selected our """""" On behalf of the entire team at the 
                  ,extend you a very welcome and trust stay with us will be both enjoyable and comfortable
                    offers a selection of business services and facilities.which are detailed in the booklet,
                   placed on the writing table in your room.Should you require any assistance or have any specific
                   requirements,please do not hesitate to contact me extension(999).</font>
                       </pre>
                 <pre>
                      <font size="4" color="blue">Confirmation Number: """+conf_no+"""</font>
                      <font size="4" color="blue">Arrival Date: """+arrival+"""</font>
                      <font size="4" color="blue">Depature Date: """+depature+"""</font>
                      <font size="4" color="blue">Room Type: """+room_type+"""</font>

                      <font size="4" color="black">With best regards / Yours sincerely,</font>
                      <font size="4" color="black">Hotel Manager</font></pre>
                        
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

@sched.scheduled_job('interval', hours=30)
def timed_job():
   string,esca_string,es_email = '','',''
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
           minutes = int(current.seconds % 3600 / 60.0)
           if minutes >= 10:
               if query_reminder['reminder_count'] < 2:

                   if len(string) == 0:
                       string  = "'"+str(query_reminder['ticket_no'])+"'"
                   else:
                       string += ',' +"'"+str(query_reminder['ticket_no'])+"'"
                   print("ticket_no",string)
    
               elif query_reminder['escalation_count']<2:
                
                 if query_reminder['escalation_count'] == 0:
                     get_employee = json.loads(dbget("select employee_role.role_name, * from employee\
	                  left join employee_role on employee_role.role_id = employee.employee_role_id \
	                      where employee_dept_id in ("+str(query_reminder['department_no'])+")"))
                     dbput("update requests set escalation_count = escalation_count+'1'  where ticket_no = '"+str(query_reminder['ticket_no'])+"'")
                 
                    
                     return sendemailadmin(get_employee)
                           
                 elif query_reminder['escalation_count'] == 1:
                     get_employee = json.loads(dbget("select employee_role.role_name, * from employee\
	                  left join employee_role on employee_role.role_id = employee.employee_role_id \
	                      where employee_dept_id in ('803')"))
                     dbput("update requests set escalation_count = escalation_count+'1'  where ticket_no = '"+str(query_reminder['ticket_no'])+"' ")
                 
                    
                     return sendemailadmin(get_employee)
           else:
               pass
    if len(string) == 0:
             pass
    else:
             dbput("update requests set reminder_count = reminder_count+'1'  where ticket_no in ("+str(string)+")")
   
                   
   
           #print(current.strftime('%M'), type(current.strftime('%M')))
   else:
           pass
sched.start()

