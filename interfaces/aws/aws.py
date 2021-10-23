import os
import sys
import json
import traceback
import logging
from datetime import datetime
from dotenv import load_dotenv
from sys import exc_info
from traceback import extract_tb

#import smtplib
#import email
#from flask import render_template, request
#from flask_restx import Namespace, Resource, reqparse

import boto3
from botocore.config import Config as ConfigBoto3
from botocore.exceptions import ClientError


load_dotenv()


class AWS(boto3):
    """class AWS based on boto3"""

    # SETTINGS OPTIONS
    LANGUAGE = {
        "default": 'pt-br'
        }
    REGION = {
        "ap": ["ap-northeast-1", "ap-south-1", "ap-southeast-1", "ap-southeast-2"],
        "global": ["aws-global"],
        "ca": ["ca-central-1"],
        "eu": ["eu-central-1", "eu-north-1", "eu-west-1", "eu-west-2", "eu-west-3"],
        "sa": ["sa-east-1"],
        "us": ["us-east-1", "us-east-2", "us-west-1", "us-west-2"],
        "default": "us-east-1",
        }
    # DEFAULT SETTINGS
    DEFAULT_CONFIG = {
        'region_name': 'us-east-1',
        'signature_version': 'v4',
        's3': {},
        'proxies': {},
        'proxies_config': {},
        'retries': {'max_attempts': 1, 'mode': 'standard'},
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        }
    
    # CONSTRUCTOR
    def __init__(self):
        self.name = 'AWS Wrapper'
