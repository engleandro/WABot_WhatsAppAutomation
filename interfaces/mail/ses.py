import os, sys
import logging, traceback
from datetime import datetime
import json
import dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# add to requirements import pytest, boto3 

from flask import render_template
#from flask_restx import Namespace, Resource, reqparse

import boto3
from botocore.config import Config as ConfigBoto3
from botocore.exceptions import ClientError

dotenv.load_dotenv()


class AWS(): # import AWS in the future

    AWS_SERVICE = {
        "instance": "ec2",
        "email": 'ses',
        "storage": "s3",
        "default": "ses",
        }
    CHARSET = {
        'default': 'UTF-8',
        }
    CONFIG = {
        "default": "ConfigSet",
        }
    LANGUAGE = {
        "default": "pt-br",
        }
    REGION_NAME = {
        "default": "us-east-1",
        }


class SES(AWS):
    """Class SES - Simple Email Service (AWS) Object
    Returns:
        AWS Client: A connection with Simple Email Service (SES) on AWS.
    """


    # SETTINGS OPTIONS
    SMTP_SERVER = {
        'aws-us-east-1': ['email-smtp.us-east-1.amazonaws.com', 587],
        'gmail.com': ['smtp.gmail.com', 587],
        'hotmail.com': [None, None],
        'outlook.com': [None, None],
        'default': ['smtp.gmail.com', 587],
        }
    

    # STANDARD CONFIG
    DEFAULT_SETTINGS = {
        'charset': 'UTF-8',
        'config': 'ConfigSet',
        'language': 'pt-br',
        'region_name': 'us-east-1',
        'aws_service': 'ses',
        }
    DEFAULT_CONFIG = {
        'region_name': 'us-east-1',
        'signature_version': 'v4',
        's3': {},
        'proxies': {},
        'proxies_config': {},
        'retries': {'max_attempts': 2, 'mode': 'standard'},
        }
    
    # CONTRUCTORS
    def __init__(self,
            user: str="no-reply",
            domain: str="gmail.com",
            settings: dict={'region_name': 'us-east-1'},
            ):
        """Constructor __init__ => SES Object"""
        self.user = user
        self.domain = domain
        self.from_address = f"{user}@{domain}"
        #self.config = SES.to_config(settings)
        self.region_name = 'us-east-1' # self.region_name = self.config.region_name 
        self.client = boto3.client('ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1')
            #config=self.config)
        self.logger = logging.getLogger(f'app.ses::{self.from_address}')
        self.buffer = None
    

    # CLASS METHODS
    @classmethod
    def to_config(cls, settings: dict):
        """class method: to_config(settings: dic) => obj ConfigBoto3
        Args:
            settings (dict, optional): [description]. Defaults to {'region_name': 'us-east-1'}.
        Returns:
            [type]: [description]
        """
        settings = settings or SES.DEFAULT_CONFIG
        boto_settings = {
            'region_name': settings.get('region_name') or 'us-east-1',
            'signature_version': settings.get('signature_version') or 'v4',
            's3': settings.get('s3') or {},
            'proxies': settings.get('proxies') or {},
            'proxies_config': settings.get('proxies_config') or {},
            'retries': settings.get('retries') \
                or {'max_attempts': 2, 'mode': 'standard'},
            }
        return ConfigBoto3(**boto_settings)
        #proxies = dict:{'https': 'https://proxy.amazon.org:2010'}
    
    @classmethod
    def get_client(cls, settings: dict={'region_name': "us-east-1"}):
        """static method: SES.get_client => obj ClientBoto3
        Args:
            settings (dict, optional): [description]. Defaults to {'region_name': "us-east-1"}.
        Returns:
            [type]: [description]
        """
        boto_config = cls.to_config(settings)
        object = boto3.client('ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=boto_config)
        return object
    

    # STATIC METHODS
    def to_config(self, settings: dict={}):
        my_config = SES.to_config(settings)
        self.config = my_config
        #return my_config
    
    def connect(self, service: str='ses',
            settings: dict={'region_name': "us-east-1"}):
        """staticmethod: client => attribute obj SES
        Args:
            service (str, optional): [description]. Defaults to 'ses'.
            settings (dict, optional): [description]. Defaults to {'region_name': "us-east-1"}.
        """
        boto_config = SES.to_config(settings)
        self.client = boto3.client(service,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=boto_config)
    
    def get_client(self, service: str='ses',
            settings: dict={'region_name': "us-east-1"}):
        """staticmethod: SES.set_client => obj ClientBoto3
        Args:
            service (str, optional): AWS Services. Defaults to 'ses'.
            settings (dict, optional): [description]. Defaults to {'region_name': "us-east-1"}.
        Returns:
            [type]: [description]
        """
        boto_config = SES.to_config(settings)
        object = boto3.client(service,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            config=boto_config)
        return object
    
    def verify_email_identity(self, email_address: str=""):
        """static method
        Args:
            email_address (str, optional): [description]. Defaults to "".
        Returns:
            [type]: [description]
        """
        email_address = email_address or self.from_address
        response = self.client.verify_email_identity(
            EmailAddress=email_address)
        return response
    
    def send_by_template(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str="<no-reply>",
            template: str="",
            ):
        """static method: send_by_html => bool response_status
        response = client.send_email(
            Source='string',
            Destination={
                'ToAddresses': [
                    'string',
                ],
                'CcAddresses': [
                    'string',
                ],
                'BccAddresses': [
                    'string',
                ]
            },
            Message={
                'Subject': {
                    'Data': 'string',
                    'Charset': 'string'
                },
                'Body': {
                    'Text': {
                        'Data': 'string',
                        'Charset': 'string'
                    },
                    'Html': {
                        'Data': 'string',
                        'Charset': 'string'
                    }
                }
            },
            ReplyToAddresses=[
                'string',
            ],
            ReturnPath='string',
            SourceArn='string',
            ReturnPathArn='string',
            Tags=[
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            ConfigurationSetName='string')
        """
        try:
            if os.path.exists(template):
                with open(template, 'r') as file:
                    html = file.read()
            source = from_address or self.from_address
            destination = {'ToAddresses': to_addresses or self.to_addresses}
            message = {
                'Subject': {'Data': subject,'Charset': 'UTF-8'},
                'Body': {'Html': {"Data": html,'Charset': 'UTF-8'} }
                }
            response = self.client.send_email(Source=source,
                Destination=destination, Message=message)
            return response
        except ClientError as Error:
            print(Error.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
    
    def send_by_text(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str='<no-reply>',
            text: str='Please, no reply this email.',
            template: str='',
            ):
        """staticmethod: send_by_text => bool response_status"""
        try:
            if not text and template:
                if os.path.exists(template):
                    with open(template, 'r') as file:
                        text = file.read()
            source = from_address or self.from_address
            destination = {'ToAddresses': to_addresses or self.to_addresses}
            message = {
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {'Text': {"Data": text, 'Charset': 'UTF-8'}}
                }
            response = self.client.send_email(Source=source,
                Destination=destination, Message=message)
            return response
        except ClientError as Error:
            print(Error.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
    
    def send(self,
            from_address: str="",
            to_addresses: list=[],
            subject: str="<no-reply>",
            text: str='',
            template: str='__template__',
            html: str='',
            context: dict={},
            attachment: str='',
            ):
        """static method: send => bool response_status"""
        try:
            source = from_address or self.from_address
            destination = {'ToAddresses': to_addresses or self.to_addresses}
            dir = os.getcwd()
            if template != '__template__':
                if template.find('/') == -1:
                    templatepath = os.path.join(dir, "intexfyInternalPlatform/templates", template)
                elif template.find('\\') == -1:
                    templatepath = os.path.join(dir, "intexfyInternalPlatform/templates", template)
            if not html and os.path.exists(templatepath):
                with open(templatepath, 'r') as file:
                    html = file.read()
            if html and context:
                html = render_template(html, **context)
            message = {
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {}
                }
            if text: message.get('Body')['Text'] = {"Data": text, 'Charset': 'UTF-8'}
            if html: message.get('Body')['Html'] = {"Data": html, 'Charset': 'UTF-8'}
            response = self.client.send_email(
                Source=source,
                Destination=destination,
                Message=message
                )
            # ATTACHMENT
            return response
        except ClientError as Error:
            print(Error.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])


#===== METHODS =====#


if __name__ == '__main__':
    template = os.getcwd()
    os.chdir('../../../')
    try:
        ses = SES()
        response = ses.send(
            to_addresses=['alves.engleandro@gmail.com'],
            subject="NOVO EMAIL",
            template=os.getcwd() + '/templates/whatsapp_authentication.html'
            )
    except Exception:
        print(traceback.format_exc())

