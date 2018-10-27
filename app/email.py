from flask_mail import Message
from flask import current_app, render_template, copy_current_request_context
from threading import Thread

from . import mail




def send_email(to, subject, template, **kwargs):
    app = current_app

    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + subject,
                  sender=app.config["MAIL_SENDER"], recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)

    @copy_current_request_context
    def send_async_email(msg):
        mail.send(msg)
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

    return thr
