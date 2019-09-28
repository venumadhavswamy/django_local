from django.db import models
from django.contrib.postgres.fields import JSONField


class User(models.Model):
    name = models.CharField(max_length=30,primary_key = True)
    password = models.CharField(max_length=256)
    laptop_json = JSONField(null=True)

class MobileNumber(models.Model):
    mobile_number = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Lot(models.Model):
    status = models.CharField(max_length=50)

class X(models.Model):
    x_var1 = models.CharField(max_length=50)
    x_var2 = models.CharField(max_length=50)

class Y(models.Model):
    y_var1 = models.CharField(max_length=50)
    y_var2 = models.CharField(max_length=50)
    x_link = models.OneToOneField(X,on_delete=models.CASCADE,related_name='link_to_x')