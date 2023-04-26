
from rest_framework.serializers import ModelSerializer 
from .models import User
from rest_framework import serializers
from common.enums import Message

class UserLoginSerializer (ModelSerializer):
    password = serializers.CharField(required=True,allow_null=False)
    email = serializers.EmailField(required = True , allow_null=False)

    class Meta : 
        model = User
        fields = ['email','password']
        extra_kwargs ={
            'password' : {'write_only':True}
        }


class UserSignupSerializer (ModelSerializer):
    
    class Meta : 
        model = User
        fields = ['email','password','first_name' , 'last_name' , 'phone' , 'institute']

        extra_kwargs ={
            'password' : {'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user


