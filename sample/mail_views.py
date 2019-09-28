from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import traceback

from celery.decorators import task
from django.core import mail
import copy
import datetime

from locallibrary.celery import app
@app.task
def send_mails(connection, emails):
    for email in emails:
        email.send(fail_silently=False)
@method_decorator(csrf_exempt,name='dispatch')
class MailTest(APIView):
    def get(self, request):
        try:
            mail_connection = mail.get_connection()
            emailx = mail.EmailMessage(
                'Hello1111111111',
                'Body goes here111111',
                "admin@krinati.co",
                ['venu@selekt.in'],
            )
            emailx.send()
            emails = []
            for i in range(0,30):
                email = copy.copy(emailx)
                email.subject = "subject"+str(i)
                email.connection = mail_connection
                emails.append(email)
            # send_mails.delay(mail_connection,emails)
            return Response(status=200)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response(status=400)

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from locallibrary import settings
import requests
import json

@method_decorator(csrf_exempt,name='dispatch')
class SendGrid(APIView):
    def get(self, request):
        response = {}
        try:
            # message = Mail(
            #     from_email='venu@selekt.in',
            #     to_emails='n130944@rguktn.ac.in',
            #     subject='Sending with Twilio SendGrid is Fun',
            #     html_content='<strong>and easy to do anywhere, even with Python</strong>'
            # )
            # sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            # response = sg.send(message)
            # print(response.status_code)
            emails = []
            emailx = {"to": [{"email": "venu@selekt.in"}],
                "subject": "YOUR SUBJECT LINE GOES HERE1",
            }
            for i in range(0,30):
                email = copy.copy(emailx)
                email['subject'] = "subject"+str(i)
                emails.append(email)
            
            data = {"personalizations":emails,
                "from": {"email": "shri.bhirud@outlook.com"},
                "content": [{"type": "text/plain","value": "Hello, World!"}]
            }
            # sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            # response = sg.send(data)
            # print(response.headers)
            # return Response(status=200,data={"status":response.status_code,"data":response.body})

            url ="https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer "+settings.SENDGRID_API_KEY
            }
            print(data)
            response = requests.post(url, data=json.dumps(data), headers=headers)
            return Response(status=response.status_code,data={"data":response})
        except Exception as e:
            traceback.print_exc()
            return Response(status=400)