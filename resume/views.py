from django.shortcuts import render
from .models import Resume
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ResumeSerializer
from rest_framework.decorators import api_view, APIView
# Create your views here.

@api_view(["GET","POST"])
def getAll(request):
    if request.method == "GET":
        all_resume = Resume.objects.all()
        resume_serializer = ResumeSerializer(all_resume, many=True)
        return Response(resume_serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        create_resume_serializer = ResumeSerializer(data=request.data)
        if create_resume_serializer.is_valid():
            create_resume_serializer.save()
            return Response(create_resume_serializer.data, status=status.HTTP_201_CREATED)    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET,POST"])
def getUser(request):
    if request.method == "GET":
        all_users = User.objects.all()
        allusers_serializer = UserSerializer(all_users, many=True)
        return Response(allusers_serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        create_user_serializer = UserSerializer(data=request.data)
        if create_user_serializer.is_valid():
            create_user_serializer.save()
            return Response(create_user_serializer.data, status=status.HTTP_201_CREATED)   
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)