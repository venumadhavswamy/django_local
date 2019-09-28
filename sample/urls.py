from django.urls import path
from .views import *
from .mail_views import *

urlpatterns = [
    path('user', UserDetail.as_view()),
    path('test',LotView.as_view()),
    path('test-serializer',TestView.as_view()),
    path('test2',MailTest.as_view()),
    path('sendgrid',SendGrid.as_view()),
]