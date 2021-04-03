import requests
from dotenv import load_dotenv
import os
from twilio.rest import Client
import smtplib
import datetime as dt

load_dotenv()

TIME = dt.datetime.now().strftime('%m-%d %H:%M')
#print(TIME)

headers = {
    'Authorization': 'Bearer ' + os.getenv("LINODE_PERSONAL_ACCESS_TOKEN")
}

LINODE_API_ENDPOINT = 'https://api.linode.com/v4/linode/instances'

clusters = requests.get(LINODE_API_ENDPOINT, headers = headers).json()

print(clusters)

message = ''
for cluster in clusters['data']:
    message += f"{cluster['label']} is {cluster['status']}; watchdog enabled: {cluster['watchdog_enabled']}.\n"

#print(Message)
subject = f"Status report on Linode clusters {TIME}"
#print(subject)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
phone_num = os.getenv("MY_PHONE_NUM")
client = Client(account_sid, auth_token)

client.messages.create(messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"), body= \
subject + '\n' + message, to=phone_num)

my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_EMAIL_PASSWORD")
email_to = os.getenv("MY_EMAIL2")

with smtplib.SMTP("outlook.office365.com") as connection:
    connection.starttls()
    connection.login(my_email, my_password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=email_to,
        msg=f"Subject:{subject}\n\n{message}"
    )
