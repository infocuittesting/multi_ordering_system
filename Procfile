web: gunicorn MOS_ROOT:mos

worker: gunicorn Configure_Alexa_With_Department.py
worker: gunicorn Configure_Department.py
worker: gunicorn Configure_Items.py
worker: gunicorn Employee_Signup.py
worker: gunicorn Fetch_Current_Datetime.py
worker: gunicorn Raise_Request.py
worker: gunicorn Report_Service.py
worker: gunicorn Fetch_Iso_Current_Datetime.py
clock: python Reminder_Request.py
