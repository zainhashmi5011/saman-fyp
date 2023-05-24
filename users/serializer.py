
from rest_framework.serializers import ModelSerializer , SerializerMethodField
from .models import *

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
        fields = ['id','email','password' , 'phone' , 'institute', 'designation']

        extra_kwargs ={
            'password' : {'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer (ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'
        extra_kwargs ={
            'password' : {'write_only':True}
        }

    def to_representation(self, instance):
        data = {
            "id" : instance.id,
             "email" : instance.email,
             "first_name" : instance.first_name,
             "last_name" : instance.last_name,
             "institute" : instance.institute,
             "phone" : instance.phone,
             "designation" : instance.designation,
             "biography" : instance.biography,
             "lab_details" : instance.lab_details,
             "postal_address" : instance.postal_address,
             "bg_color" : instance.bg_color
        }
        try:
            data["image"] = self.context["request"].build_absolute_uri(instance.image.url)
        except Exception as e:
            print(e)
        return data



class EducationSerializer (ModelSerializer):
    class Meta :
        model = Education
        fields = '__all__'


class AwardsSerializer (ModelSerializer):
    class Meta :
        model = Awards
        fields = '__all__'

class AcedemicSerializer (ModelSerializer):
    class Meta :
        model = AcademicExp
        fields = '__all__'

class AchievmentSerializer (ModelSerializer):
    class Meta :
        model = Achievements
        fields = '__all__'

class BlogSerializer (ModelSerializer):
    class Meta :
        model = Blogs
        fields = '__all__'


class JobSerializer (ModelSerializer):
    class Meta :
        model = Jobs
        fields = '__all__'


class FundingSerializer (ModelSerializer):
    class Meta :
        model = Funding
        fields = '__all__'



class PictureSerializer (ModelSerializer):

    class Meta :
        model = Pictures
        fields = ['id', 'user', 'title', 'image']


    def to_representation(self, instance):
        try:
            image_url = self.context['request'].build_absolute_uri(instance.image.url)
        except:
            image_url = None

        data = {
            'id': instance.id,
            'user': instance.user_id,
            'title': instance.title,
            'image': image_url
        }
        return data



class CollaborationSerializer (ModelSerializer):

    class Meta :
        model = Collaborations
        fields = ['id', 'user', 'title', 'image', 'role']


    def to_representation(self, instance):
        try:
            image_url = self.context['request'].build_absolute_uri(instance.image.url)
        except :
            image_url = None

        data = {
            'id' : instance.id,
            'user': instance.user_id,
            'title' : instance.title,
            'image' :  image_url,
            'role' : instance.role
        }
        return data