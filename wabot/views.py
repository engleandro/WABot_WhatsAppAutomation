from os import environ
from time import monotonic, sleep
from traceback import format_exc

from rest_framework.views import APIView
from rest_framework.response import Response

from interfaces.whatsapp.whatsapp import WhatsApp
from interfaces.mail.django_ses import SES


def returnSuccess():
    return Response(
            {
            'code': 200,
            'status': True,
            'message': "Sucess on WABot.sendMessage()"
            }
        )

def returnFailure():
    return Response(
            {
            'code': 400,
            'status': False,
            'message': "Failure on WABot.sendMessage()"
            }
        )

def validateWhatsApp(
        whatsapp: WhatsApp,
        from_phone: str,
        email: str,
        timeout: float=15.0
        ):
    """docstring"""
    start = monotonic()
    try:
        ses = SES()
        whatsapp.toAccess()
        sleep(timeout)
        while (monotonic() - start) \
                < 110*timeout:
            if not whatsapp.is_connected:
                whatsapp.toComment(comment='printing screen...')
                whatsapp.takePrintScreen()
                whatsapp.toComment(comment='send email...')
                ses.sendRawEmail(
                    to_addresses=[email],
                    subject="<NO-REPLY> WHATSAPP AUTHENTICATION IS REQUIRED",
                    template='whatsapp_validation.html',
                    attachment="screenshot.png"
                    )
                sleep(4 * timeout) #change to 10
                whatsapp.is_connected = whatsapp.toCheck()
                whatsapp.dumpCookies()
                whatsapp.toAccess()
                sleep(timeout)
            elif whatsapp.is_connected:
                whatsapp.dumpCookies()
                return True
        return False
    except Exception: #noqa
        print(format_exc())
        return False


class SendMessageAPIView(APIView):
    #serializer_class=WABotMessageSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            # REQUEST DATA
            to_phone = request.data.get("to_phone")
            message = request.data.get("message")
            
            # LOAD DATA
            email = environ.get('MAIL_WHATSAPP_VALIDATION')
            from_phone = environ.get('WHATSAPP_NOREPLY')
            
            # SETTINGS
            headless = True
            
            #SEND MESSAGE
            whatsapp = WhatsApp(
                from_phone=from_phone,
                headless=headless
                )
            
            if not whatsapp.is_connected:
                validated = validateWhatsApp(
                    whatsapp,
                    from_phone=from_phone,
                    email=email
                    )
            
            status = False
            if whatsapp.is_connected:
                status = whatsapp.sendMessage(
                    phone=to_phone,
                    message=message
                    )
            
            if status:
                return returnSuccess()
            return returnFailure()

        except Exception: #noq
            print(format_exc())
            return returnFailure()
