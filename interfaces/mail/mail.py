import os
import sys
from sys import exc_info
import json
import traceback
import logging
from datetime import datetime
import smtplib
from traceback import extract_tb
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request
from flask_restx import Namespace, Resource, reqparse

load_dotenv()

class Email():

    def __init__(self,
            user: str="no-reply",
            domain: str="gmail.com",
            password: str="",
            server: list=['smtp.gmail.com', 587]
            ):
        self.user = user
        self.domain = domain
        self.from_address = f"{user}@{domain}"
        if not password:
            password = os.getenv("EMAIL_PASSWORD")  # ALTER PSSWRD ON ENV FILE
        self.to_addresses = list()
        self.subject = str()
        self.content = MIMEMultipart() #.set_charset("utf-8")
        self.message = str()
        self.rendered = str()
        self.context = dict()
        self.template_path = str()
        self.template = str()
        self.logger = logging.getLogger(f'app.account_manager_{user}@{domain}')
        self.server_address = server[0]
        self.server_port = server[1]
        self.connect(self.user, self.domain, password, server)
    
    def duplicate(self, password: str):
        return __init__(
            self.user,
            self.domain,
            password,
            [self.server_address, self.server_port]
            )
    
    def create_localserver(self, password: str="", port: int=1025):
        import subprocess
        command = f"sudo python -m smtpd -c DebuggingServer -n localhost:{port}"
        #subprocess.Popen(args=command.split(),stdin=subprocess.PIPE).communicate(input=password)
        with subprocess.Popen(command.split(),
                stdin=subprocess.PIPE,
                universal_newlines=True) as process:
            print(password, file=process.stdin) # provide answer
            process.stdin.flush()

    def connect(self,
            user: str,
            domain: str,
            password: str,
            server: list=['smtp.gmail.com', 587]):
        SMTPFailedException = smtplib.SMTPConnectError
        try:
            self.user = user
            self.domain = domain
            self.from_address = f'{user}@{domain}'
            self.server_address = server[0]
            self.server_port = server[1]
            self.connection = smtplib.SMTP(
                self.server_address,
                self.server_port)
            self.connection.ehlo()
            self.connection.starttls()  # Enables security
            self.connection.ehlo()
            if all([self.from_address, password]):
                self.connection.login(self.from_address, password)
                return True
            return False
        except Exception as Error: # noqa
            self.logger.warning(''.join(traceback.format_tb(Error.__traceback__)))
            raise SMTPFailedException(0, 'Failed to login to SMTP')
    
    def create(self, to_addresses: list=[], subject: str=""):
        try:
            self.to_addresses = self.to_addresses if not to_addresses else to_addresses
            self.subject = self.subject if not subject else subject

            self.content = MIMEMultipart() #set_charset("utf-8")
            self.content['From'] = self.from_address
            if type(self.to_addresses) == str:
                self.content['To'] = self.to_addresses
            elif type(self.to_addresses) == list and len(self.to_addresses) > 1:
                self.content['To'] = ', '.joint(self.to_addresses)
            else:
                self.content['To'] = self.to_addresses[0]
            self.content['Subject'] = self.subject

            return True
        except Exception as _Error: # noqa
            print("Report: Error ("+str(_Error)+\
            ") on "+str(extract_tb(exc_info()[-1],1)[0][2])\
            +" at line "+str(exc_info()[-1].tb_lineno))
    
    def write_by_text(self, message: str=""):
        self.message = self.message if not message else message
        text = MIMEText(self.message, 'plain')
        self.content.attach(text)
    
    def write_by_template(self,
            app=None,
            context: dict={},
            template: str='',
            template_path: str=''):
        try:
            self.template = self.template if not template else template
            self.template_path = self.template_path if not template_path else template_path
            if not self.template_path: self.template_path = os.getcwd()+'/'
            else:
                if self.template_path[-1]!='/': self.template_path += '/'
            # Flask integration
            if app:
                self.rendered = render_template(template, **context)
                email_message = MIMEText(self.rendered, 'html')
                self.content.attach(email_message)
            else:
                if os.path.exists(self.template_path + self.template):
                    with open(self.template_path + self.template, 'r') as _file:
                        self.html = _file.read()
                    self.rendered = self.html # not rendering, should
                    email_message = MIMEText(self.rendered, 'html')
                    self.content.attach(email_message)
        except Exception as _Error: #noqa
            print("Report: Error ("+str(_Error)+\
            ") on "+str(extract_tb(exc_info()[-1],1)[0][2])\
            +" at line "+str(exc_info()[-1].tb_lineno))
    
    def send_email(self,
            to_addresses: list=[],
            subject: str="",
            content: str=""):
        """Sends template email to given address."""
        try:
            message = MIMEMultipart()
            message['From'] = self.from_address
            message['To'] = to_addresses
            message['Subject'] = subject
            message.attach(MIMEText(content, 'html'))
            text = message.as_string()
            self.connection.sendmail(self.from_address, to_addresses, text)
            #self.sent_today += 1
            #self.mongo_interface.update_email_as_sent(to_addresses)
            #self.mongo_interface.update_count(self.username, self.sent_today)
            return {'success': True, 'address': to_addresses}
        except (smtplib.SMTPRecipientsRefused, UnicodeEncodeError):    # noqa
            #self.logger.debug("Server Refused to send: {}".format(to_addresses))
            #self.mongo_interface.update_email_status(
            #    to_addresses,
            #    self.mongo_interface.INVALID)
            return {'success': False, 'address': to_addresses}
        except Exception as _Error: #noqa
            print("Report: Error ("+str(_Error)+\
            ") on "+str(extract_tb(exc_info()[-1],1)[0][2])\
            +" at line "+str(exc_info()[-1].tb_lineno))
            return {'success': False, 'address': to_addresses}
    
    def send(self):
        try:
            text = self.content.as_string()
            self.connection.sendmail(
                self.from_address,
                self.to_addresses,
                text)
            #self.sent_today += 1
            #self.mongo_interface.update_email_as_sent(to_addresses)
            #self.mongo_interface.update_count(self.username, self.sent_today)
            return {'success': True, 'address': self.to_addresses}
        except (smtplib.SMTPRecipientsRefused, UnicodeEncodeError):    # noqa
            self.logger.debug(f"Server Refused to send: {to_addresses}")
            #self.mongo_interface.update_email_status(to_addresses, self.mongo_interface.INVALID)
            return {'success': False, 'address': self.to_addresses}
        except Exception as _Error: #noqa
            print("Report: Error ("+str(_Error)+\
            ") on "+str(extract_tb(exc_info()[-1],1)[0][2])\
            +" at line "+str(exc_info()[-1].tb_lineno))

    def finish(self):
        self.connection.quit()
        self.connection.close()


## UNIT-TESTING

if __name__ == '__main__':
    try:
        email = Email(
            user="username",
            domain="gmail.com",
            password="test@123",
            server=['localhost', 1025]
            )
        email.create(to_addresses="receiver@gmail.com", subject="test")
        
        path = os.getcwd()
        print(f'path>{path}'); os.chdir('..')
        print(f'path>{os.getcwd()}'); os.chdir(path)

        email.write_by_template(template='whatsapp_authentication.html')

        email.send()
        email.finish()

    except Exception as _Error:
        print("Report: Error ("+str(_Error)+\
        ") on "+str(extract_tb(exc_info()[-1],1)[0][2])\
        +" at line "+str(exc_info()[-1].tb_lineno))
