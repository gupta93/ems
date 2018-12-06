import os
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_mail(sender, receiver, name=None, subject=None, text=None):

    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        MAIL_PORT=587,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True
    )
    LOGIN_USER_NAME = os.environ['MAIL_USERNAME']
    LOGIN_PASSWD = os.environ['MAIL_PASSWORD']
    SMTP_SERVER = 'smtp.gmail.com'
    try:
        message = MIMEMultipart('alternative')
        message['From'] = '{}<{}>'.format(name, LOGIN_USER_NAME)
        message['To'] = ",".join(receiver)
        message['Subject'] = subject
        all_receivers = list()
        all_receivers += receiver
        if text:
            text_part = MIMEText(text, 'plain')
            message.attach(text_part)
        connection = smtplib.SMTP_SSL(host=SMTP_SERVER,port=465)
        connection.ehlo()
        connection.set_debuglevel(True)
        connection.login(LOGIN_USER_NAME, LOGIN_PASSWD)
        try:
            connection.sendmail(sender, all_receivers, message.as_string())
            print "SMTP mail sent:"
        finally:
            connection.quit()
    except Exception, ex:
        import traceback
        print traceback.print_exc()
        print "Mail Sending Failed: %s" % str(ex)