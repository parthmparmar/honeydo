from hdo import mail, app
from flask_mail import Message
from flask import render_template

def email_reset_password(send_to):
    subject = "Password Reset"
    recipents = [send_to]
    msg = Message(  subject=subject,
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=recipents)
    msg.html = render_template("/email_templates/password-reset.html")
    mail.send(msg)

def email_new_user(send_to):
    subject = "Welcome"
    recipents = [send_to]
    msg = Message(  subject=subject,
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=recipents)
    msg.html = render_template("/email_templates/new-user.html")
    mail.send(msg)

def email_forgot_password(send_to, new_password):
    subject = "Forgot Password - Reset"
    recipents = [send_to]
    msg = Message(  subject=subject,
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=recipents)
    msg.html = render_template("/email_templates/forgot-password.html", new_password = new_password)
    mail.send(msg)
