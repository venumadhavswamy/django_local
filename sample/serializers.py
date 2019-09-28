from .models import *
from rest_framework import serializers, fields
import bcrypt

class MobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileNumber
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    mobile_numbers = MobileNumberSerializer(many=True)
    class Meta:
        model = User
        fields = ('name','mobile_numbers','laptop_json','password')
        extra_kwargs = {'password' : {'write_only':True}}
        
    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        return hashed_password

    def create(self, validated_data):
        mobile_numbers = validated_data.pop('mobile_numbers')
        print('*********')
        print(mobile_numbers)
        password = validated_data.get('password')
        validated_data['password'] = self.hash_password(password)
        user = User.objects.create(**validated_data)
        for mobile_number in mobile_numbers:
            MobileNumber.objects.create(user=user,**mobile_number)
        return user

    def update(self, user, validated_data):
        mobile_numbers_data = validated_data.pop('mobile_numbers')
        mobile_numbers = user.mobile_number.all()
        mobile_numbers = list(mobile_numbers)
        password = validated_data.get('password',user.password)
        user.password = hash_password(password)
        return user

class XSerializer(serializers.ModelSerializer):
    #link_to_x = YSerializer(many=False)
    class Meta:
        model = X
        fields = '__all__'

class YSerializer(serializers.ModelSerializer):
    x_link = XSerializer(many=False)
    class Meta:
        model = Y
        fields = '__all__'
