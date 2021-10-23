import os

from flask import Flask, render_template, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.co'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)


def send_email(from_address,
        to_addresses: list=[],
        subject: str="",
        template: str="",
        context: dict={}
        ):
    """method: send_email => """
    try:
        message = Message(subject, from_address, recipients=to_addresses)
        message.html = render_template(template, **context)
        mail.send(message)
        return {'status': True}
    except Exception:
        raise Exception('An error occurs on send_email')
        return {'status': False}

