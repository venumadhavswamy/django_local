from django.urls import path
from django.urls import re_path
from .views import *
from django.urls import include

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    path('signup', CreateUser.as_view(), name = 'signup'),
    path('login', LoginUser.as_view(), name = 'login'),
    path('tokenlogin', LoginUserToken.as_view(), name = 'tokenlogin'),
    path('accounts/', include('allauth.urls')),
    path('fb-login', facebook_login),
    path('fb-login-redirect', FacebookLoginRedirect.as_view(),name= 'fb_login_redirect'),
]