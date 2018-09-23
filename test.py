import traceback
from email.MIMEMultipart import MIMEMultipart
import email.utils
from email.MIMEText import MIMEText
import smtplib
import requests
from pytz import timezone
from datetime import datetime, date as pythondate, timedelta
from property_file_tml import *
import psycopg2
import json

EMAIL_USE_TLS = True
EMAIL_SMTP_HOST = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587


def send_email(status,msg_table=''):

    try:
        time_utc = datetime.now(timezone('UTC'))
        time_ist = time_utc.astimezone(timezone('Asia/Kolkata'))
        msgid = '<153140213984.30092.17215005559157838087@testeguruskin.api.tatamotors>'
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROMADDR
        msg['To'] = ",".join(EMAIL_TOADDR)
        msg['Cc'] = ",".join(EMAIL_CCADDR)
        msg.add_header("In-Reply-To", msgid)
        msg.add_header("References", msgid)
        msg['Subject'] = "Monitoring production server"
        msg.attach(MIMEText(msg_table, 'html'))
        server = smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROMADDR, EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        recipients_list = EMAIL_TOADDR + EMAIL_CCADDR
        server.sendmail(EMAIL_FROMADDR, recipients_list, text)
        server.quit()
    except Exception as em:
        traceback.print_exc()
        print "Exception in email ", str(em)

#def get_msg_body(login_resp_code_one_skin, login_resp_code_two_skin, login_resp_code_one_core, login_resp_code_two_core):
    
def test_login_skin_one(msg_table):
    login_resp = requests.post(url = Skin_server_one, data=payload_crm)
    login_resp_code_one_skin = login_resp.status_code
    if login_resp_code_one_skin == 200:
        token = 'Bearer '+login_resp.json().get('token').get('access_token')
        logout_resp = requests.post(url = 'http://eguruskin.api.tatamotors/api/logout/', data=payload_crm,headers={'Authorization':token})

def test_login_skin_two():
    login_resp = requests.post(url = Skin_server_two, data=payload_crm)
    login_resp_code_two_skin = login_resp.status_code
        #return login_resp_code_one_skin
    #print login_resp_code_one_skin
    if login_resp_code_two_skin == 200:
        token = 'Bearer '+login_resp.json().get('token').get('access_token')
        logout_resp = requests.post(url = 'http://eguruskin.api.tatamotors/api/logout/', data=payload_crm,headers={'Authorization':token})
    # else:
    #     send_email(False,msg_table=msg_table)   


def test_login_core_one():
    login_resp = requests.post(url = Core_server_one, data=payload_crm)
    login_resp_code_one_core = login_resp.status_code
    # if login_resp_code_one_core != 200:
    #     send_email(False,msg_table=msg_table)   

def test_login_core_two():
    login_resp = requests.post(url = Core_server_one, data=payload_crm)
    login_resp_code_two_core = login_resp.status_code
    # if login_resp_code_two_core != 200:
    #     send_email(False,msg_table=msg_table)

def status_mail(msg_table):
    msg_table = """\
                <html>
                <head></head>
                <body>
                <h4>STATUS:SERVER IS DOWN!!!</h4>
                <table border= "2">
                <tr><th>Server Name</th><th>Status</tr>
                <tr><td>"{Skin_server_one}"</td><td>"{login_resp_code_one_skin}"</td></tr>
                <tr><td>"{Skin_server_two}"</td><td>"{login_resp_code_two_skin}"</td></tr>
                <tr><td>"{Core_server_one}"</td><td>"{login_resp_code_one_core}"</td></tr>
                <tr><td>"{Core_server_two}"</td><td>"{login_resp_code_two_core}"</td></tr>
                </table>
                </body>
                </html>
                """.format(
                    Skin_server_one=Skin_server_one, login_resp_code_one_skin = login_resp_code_one_skin 
                  , Skin_server_two=Skin_server_two, login_resp_code_two_skin = login_resp_code_two_skin
                  , Core_server_one=Core_server_one, login_resp_code_one_core = login_resp_code_one_core 
                  , Core_server_two=Core_server_two, login_resp_code_two_core = login_resp_code_two_core  )

    if (login_resp_code_one_skin or login_resp_code_two_skin or login_resp_code_one_core or login_resp_code_two_core != 200):
        send_email(False,msg_table=msg_table)

if __name__ == '__main__':
    test_login_skin_one(msg_table=msg_table)



                       
                                                                                                                             

