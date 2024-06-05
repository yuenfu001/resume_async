from rest_framework import serializers

from .models import Resume
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

#User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","password")
        # fields = ('id', 'first_name', 'last_name', 'email','phone_number','address','middle_name')

#Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","password")
        extra_kwargs = {'password':{'write_only':True}}
        # fields = ('id', 'first_name', 'last_name', 'email','phone_number','address','middle_name')


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields =  "__all__"
        # fields =  ["id","company","school","college","achievement","hobbies"]