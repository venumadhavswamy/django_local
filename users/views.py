from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view

#from django import forms

import jwt,json

from django.views.decorators.csrf import csrf_exempt

from users.models import User
from locallibrary.settings import SECRET_KEY, SOCIAL_AUTH_FACEBOOK_KEY

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect

@method_decorator(require_POST, name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        message =""
        status =""

        try:
            data = request.data
            print(data)
            name = data["name"]
            mobile_number = data["mobile_number"]
            password = data["password"]
            new_user = User.objects.create(name=name, password =password, mobile_number=mobile_number)
            print("newuser"+new_user.name)
            status = 201 #Created record
            message = "New user created"

        except Exception as e:
            print(e)
            message = "Invalid Request"
            status = 400 #Bad request

        finally:
            return JsonResponse({"message":message, "status":status})

@method_decorator(require_POST, name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        response_data = {'message':'','status':''}
        if not request.data:
            response_data['message'] = 'Please provide username and password'
            response_data['status'] = '400'
            return Response(response_data)
        mobile_number = request.data['mobile_number']
        password = request.data['password']

        try:
            user = User.objects.get(mobile_number = mobile_number, password = password)
            if user:
                payload = {
                    'mobile_number':mobile_number,
                    'password': password,
                }
                jwt_token = jwt.encode(payload, SECRET_KEY)
                response_data['message'] = 'Login successful'
                response_data['status'] = '200'
                response_data['token'] = jwt_token
                return Response(response_data)
        except User.DoesNotExist:
            response_data['message'] = 'Invalid username/password'
            response_data['status'] = '400'
            return Response(response_data) 

@method_decorator(require_POST, name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class LoginUserToken(APIView):
    def post(self, request, *args, **kwargs):
        headers = request.headers
        response_data = {'message':'','status':''}
        if headers and 'Bearer' in headers.keys():
            token = headers['Bearer']
            payload = jwt.decode(token,SECRET_KEY)
            mobile_number = payload['mobile_number']
            password = payload['password']
            try:
                user = User.objects.get(mobile_number = mobile_number, password = password)
                jwt_token = jwt.encode(payload, SECRET_KEY)
                response_data['message'] = 'Login successful'
                response_data['status'] = '200'
                response_data['token'] = jwt_token
                return Response(response_data)
            except User.DoesNotExist:
                response_data['message'] = 'Invalid token'
                response_data['status'] = '400'
                return Response(response_data)


import requests, urllib
import urllib

@api_view(['POST','GET'])
@csrf_exempt
def facebook_login(request):
    fb_url = 'https://www.facebook.com/v4.0/dialog/oauth'
    #                 client_id={'''+SOCIAL_AUTH_FACEBOOK_KEY+'''}
    #                 &redirect_uri={"https://www.domain.com/login"}
    #                 &state={"{st=state123,ds=123456789}"}'''
    print('fblogin')
    data = {
        'client_id': SOCIAL_AUTH_FACEBOOK_KEY,
        'redirect_uri': 'http://localhost:8000/users/fb-login-redirect',
        'state': '{"st":"state123"}',
        'scope': 'email',
        'response_type': 'token'
    }
    url = 'https://www.facebook.com/v4.0/dialog/oauth?client_id='+SOCIAL_AUTH_FACEBOOK_KEY+'&redirect_uri=http://localhost:8000/users/fb-login-redirect&response_type=token'
    # r = requests.get(fb_url,data)#html login response
    # r = HttpResponseRedirect(fb_url+ urllib.urlencode(data))
    response = urllib.request.urlopen(url)
    print(response.read())
    return HttpResponse(response)

    # print(r.url)
    # return HttpResponse(r)


from urllib import parse
from django.urls import reverse, resolve

@method_decorator(csrf_exempt,name='dispatch')
class FacebookLoginRedirect(APIView):
    def get(self, request, *args, **kwargs):
        print(request.get_absolute_url())
        return Response({'msg':'gotit'})