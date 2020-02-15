from . import mail
from flask_mail import Mail, Message
from flask import render_template

mail = Mail()

def mail_message(subject,template,to,**kwargs):
    sender_email= 'monicaoyugi@gmail.com'
    email = Message(subject,sender=sender_email,recipients=[to])
    email.body = render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)