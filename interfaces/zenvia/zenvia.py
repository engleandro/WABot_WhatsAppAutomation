import os, sys
import time, datetime
import traceback, logging, pytest
from dotenv import load_dotenv

from flask import jsonify, render_template
#from flask_restful import Resource, Api
#from flask_cors import CORS
#import urllib.request, json
import requests
from requests import Request, Session


#CORS(app)
#load_dotenv()


class Zenvia():
    """class Zenvia..."""


    # SETTINGs
    APPLICATION = {
        'facebook': {
            'application': 'facebook',
            'method': ['POST'],
            'path': 'channels/facebook/messages',
            'schema': 'components/schemas/message.facebook',
            },
        'instagram': {
            'application': 'instagram',
            'method': ['POST'],
            'path': 'channels/instagram/messages',
            'schema': 'components/schemas/message.instagram',
            },
        'sms': {
            'application': 'sms',
            'method': ['POST'],
            'path': 'channels/sms/messages',
            'schema': 'components/schemas/message.sms',
            },
        'telegram': {
            'application': 'telegram',
            'method': ['POST'],
            'path': 'channels/telegram/messages',
            'schema': 'components/schemas/message.telegram',
            },
        'voice': {
            'application': 'voice',
            'method': ['POST'],
            'path': 'channels/voice/messages',
            'schema': 'components/schemas/message.voice',
            },
        'whatsapp': {
            'application': 'whatsapp',
            'methods': ['POST'],
            'path': 'channels/whatsapp/messages',
            'schema': 'components/schemas/message.instagram',
            }
        }
    

    # CONSTRUCTORS
    def __init__(self,
            application: str='whatsapp',
            token: str='',
            ):
        """Object constructor: Zenvia 
        Args:
            application (str, optional): [description]. Defaults to 'whatsapp'.
            token (str, optional): [description]. Defaults to ''.
        """
        self.name = "Zenvia"
        self.version = "0.1"
        self.update_at = datetime.date(2021, 10, 8)
        self.address = os.getenv('ZENVIA_API')
        self.application = Zenvia.APPLICATION.get(application) \
            or Zenvia.APPLICATION.get('whatsapp')
        self.url = self.application.get('path')
        self.endpoint = self.address + self.url
        self.accounts = {'whatsapp': os.getenv('WHATSAPP_CONTACT')}
        self.auth = tuple()
        self.data = dict()
        self.json = dict()
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-TOKEN': token or os.getenv("TOKEN_ZENVIA"),
            }
        self.timeout = 5.0
        self.buffer = None
    

    # CLASS METHODS
    @classmethod
    def set_content(cls,
            content: str,
            context: dict,
            ):
        """static method: set_content
        Args:
            content (str): [description]
            context (dict): [description]
            template ([type]): [description]
        Returns:
            [type]: [description]
        """
        try:
            CONTENTS = {
                'button': [
                    {
                    'type': 'type',
                    'header': {
                        'type': 'filetype',
                        'fileUrl': 'fileUrl',
                        },
                    'body': 'body',
                    'footer': 'footer',
                    'buttons': [
                        {
                        'id': 'id1',
                        'title': 'title1'
                        },
                        {
                        'id': 'id2',
                        'title': 'title2'
                        },
                        {
                        'id': 'id3',
                        'title': 'title3'
                        }
                        ],
                    },
                    ],
                'contacts': [
                    {
                    'type': 'type',
                    'contacts': [
                        {
                        'addresses': [
                            {
                            'street': 'street',
                            'city': 'city',
                            'state': 'state',
                            'zip': 'cep',
                            'country': 'country',
                            'countryCode': 'countryCode',
                            'type': 'addresstype'
                            }
                            ],
                        'birthday': 'birthday',
                        'contactImage': 'contactImage',
                        'emails': [
                            {
                            'email': 'email',
                            'type': 'emailtype'
                            }
                            ],
                        'name': {
                            'formattedName': 'formattedName',
                            'firstName': 'firstName',
                            'lastName': 'lastName',
                            'middleName': 'middleName',
                            'suffix': 'suffix',
                            'prefix': 'prefix'
                            },
                        'org': {
                            'company': 'company',
                            'department': 'department',
                            'title': 'title'
                            },
                        'phones': [
                            {
                            'phone': 'phone',
                            'type': 'phonetype',
                            'waId': 'waId'
                            }
                            ],
                        'urls': [
                            {
                            'url': 'url',
                            'type': 'urltype'
                            }
                            ]
                        }
                        ]
                    }
                    ],
                'file': [
                    {
                    'type': 'type',
                    'fileUrl': 'fileUrl',
                    'fileMimeType': 'fileMimeType',
                    'fileCaption': 'fileCaption',
                    'fileName': 'fileName'
                    }
                    ],
                'list': [
                    {
                    'type': 'type',
                    'header': 'header',
                    'body': 'body',
                    'footer': 'footer',
                    'button': 'button',
                    'sections': [
                        {
                        'title': 'title',
                        'rows': [
                            {
                            'id1': 'id1',
                            'title1': 'title1',
                            'description1': 'description1'
                            },
                            {
                            'id2': 'id2',
                            'title2': 'title2',
                            'description2': 'description2'
                            },
                            {
                            'id3': 'id3',
                            'title3': 'title3',
                            'description3': 'description3'
                            }
                            ],
                        },
                        ],
                    }
                    ],
                'location': {
                    'type': 'type',
                    'latitude': 'latitude',
                    'longitude': 'longitude',
                    'name': 'name',
                    'address': 'address',
                    'url': 'url',
                    },
                'template': {
                    'type': 'type',
                    'templateId': 'templateId',
                    'fields': {
                        'name': 'name',
                        'product': 'product'
                        }
                    },
                'text': [
                    {
                    'type': 'type',
                    'text': 'text'
                    }
                    ]
                }
            contents = CONTENTS.get(content)
            if content == 'text':
                contents['type'] = context.get('type') or 'text'
                contents['text'] = context.get('text') or ''
            else:
                contents['type'] = context.get('type') or 'template'
                contents['templateId'] = context.get('templateId') or ''
                contents['name'] = context.get('name') or ''
                contents['product'] = context.get('product') or ''
            return contents
            # FILTER UNWANTED CONTENT
            #return CONTENTS.get(content)
        except Exception:
            print(traceback.format_exc())
    

    # STATIC METHODS
    def set_content(self,
            content: str,
            context: dict,
            ):
        """[summary]
        Args:
            content (str): [description]
            context (dict): [description]
        """
        return Zenvia.set_content(content=content, context=context)

    def wa_send_message(self,
            #sender,
            #receiver,
            #content: str='text',
            #context: list=[],
            endpoint: str="",
            data: dict={},
            json: dict={},
            headers: dict={},
            timeout: int=5.0,
            ):
        """statis method: wa_send_message > response
        Args:
            endpoint (str, optional): [description]. Defaults to "".
            json (dict, optional): [description]. Defaults to {'from': str, 'to': str, 'contents': list}.
            headers (dict, optional): [description]. Defaults to {}.
            timeout (int, optional): [description]. Defaults to 10.
        Returns:
            response (dict): [description]
        """
        try:
            response = requests.post(
                endpoint or self.endpoint,
                data=data or self.data,
                json=json or self.json,
                headers=headers or self.headers,
                timeout=timeout or self.timeout
                )
            return response
        except Exception:
            print(traceback.format_exc())


#=== TESTING ===#


if __name__ == '__main__':
    
    token = 'put-your-token-here'

    try:
        zenvia = Zenvia()
        template = {
            'from': '55DDNNNNNNNNN',
            'to': '55DDNNNNNNNNN',
            'contents': {
                "type": "template",
                "templateId": "template_id",
                "fields": {}
            }
        } # jsonify
        text = {
            'from': '55DDNNNNNNNNN',
            'to': '55DDNNNNNNNNN',
            'contents': [
                {
                "type": "text",
                "text": "Hello Zenvia",
                }
            ]
        } # jsonify
        response = zenvia.wa_send_message(json=text)
        print(response.json())
    except Exception:
        print(traceback.format_exc())

