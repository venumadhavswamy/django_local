from django.db import models
from  django.contrib.auth import hashers
import uuid

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30,help_text="Enter your name")
    mobile_number = models.CharField(primary_key = True, max_length = 10)
    password = models.CharField(max_length=256,help_text="Enter password")

    @classmethod
    def create(cls, name, password, mobile_number):
        user = cls(name =name, password =password, mobile_number =mobile_number)
        return user
    
    def __str__(self):
        return self.name
