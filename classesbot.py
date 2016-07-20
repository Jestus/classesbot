#! python3
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
count = 0


@sched.scheduled_job('interval', seconds=10)
def check_availability():
    r = requests.get("http://api.purdue.io/odata/Sections?$expand=Class($expand=Term)&$filter=((CRN eq '11905') or "
                     "(CRN eq '65485')) and (Class/Term/Name eq 'Fall 2016')")

    global count

    jason = r.json()["value"]
    should_email = True
    for x in range(0, 2):
        if jason[x]["RegistrationStatus"] == 'NotAvailable' or jason[x]["RemainingSpace"] < 0:
            should_email = False

    if should_email:
            msg = MIMEMultipart()
            msg['From'] = 'jklan1453@gmail.com'
            msg['To'] = 'landisj@purdue.edu'
            msg['Subject'] = 'Your CGT Class is Available!'
            message = 'Head over to www.mypurdue.purdue.edu!'
            msg.attach(MIMEText(message))

            mailserver = smtplib.SMTP('smtp.gmail.com', 587)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.ehlo()
            mailserver.login('jklan1453@gmail.com', 'aaeteeyyjilotgyf')

            mailserver.sendmail('jklan1453@gmail.com', 'landisj@purdue.edu', msg.as_string())

            mailserver.quit()

    print("Run number: " + str(count) + "\nRegistration: \n" + str(jason[0]["RegistrationStatus"]) + " | " +
          str(jason[1]["RegistrationStatus"]) +
          "\nRemainingSpace: \n" + str(jason[0]["RemainingSpace"]) + " | " + str(jason[1]["RemainingSpace"]))
    count += 1

sched.start()