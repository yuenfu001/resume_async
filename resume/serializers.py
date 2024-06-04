from rest_framework import serializers

from .models import Resume
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ('id', 'first_name', 'last_name', 'email','phone_number','address','middle_name')


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields =  "__all__"
        # fields =  ["id","company","school","college","achievement","hobbies"]