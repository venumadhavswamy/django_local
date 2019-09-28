from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import traceback

from locallibrary import settings
#Create, update, get and delete user
@method_decorator(csrf_exempt,name='dispatch')
class UserDetail(APIView):
    def post(self, request, *args, **kwargs):
        print('%%%%%%%')
        print(request.data)
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,"message":"User created","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"status":False,"message":"Invalid request","data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        data = request.data
        print(request.data)
        try:
            name = data['name']
            user = User.objects.get(name=name)
            serializer = UserSerializer(user)
            return Response({"status":True,"message":"Successfull","data":serializer.data},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        data = request.data
        name = data['name']
        try:
            user = User.objects.get(name=name)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#Filter users
@method_decorator(csrf_exempt,name='dispatch')
class UserFilter(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        name = data['name']
        users = User.objects.get(name__iexact=name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

from datetime import timedelta
import datetime
import traceback

def changeStatus(lot):
        lot.status = "changed"
        lot.save()
        print(lot.status)

@method_decorator(csrf_exempt,name='dispatch')
class LotView(APIView):
    def post(self, request):
        try:
            status = request.data['status']
            lot = Lot.objects.create(status=status)
            job = settings.scheduler.add_job(
                changeStatus, 
                trigger='date',
                jobstore='redis',
                run_date=datetime.datetime.now()+timedelta(minutes=2),
                id = str(1234),
                replace_existing=True,
                args = [lot]
                )
            print()
            return Response(status=200)
        except Exception as e:
            print(e)
            return Response(status=400)

@method_decorator(csrf_exempt,name='dispatch')
class TestView(APIView):
    def post(self, request):
        try:
            x_data = request.data['x_data']
            y_data = request.data['y_data']
            x_instance = X.objects.create(**x_data)
            y_instance = Y.objects.create(x_link=x_instance,**y_data)
            x_serializer = XSerializer(x_instance)
            y_serializer = YSerializer(y_instance)
            print(x_serializer)
            return Response(status=200,data = y_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(status=400)