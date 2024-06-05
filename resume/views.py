from django.shortcuts import render,get_object_or_404
from .models import Resume
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer,ResumeSerializer
from rest_framework.decorators import api_view, APIView
# Create your views here.

#Login API
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User,username=request.data(["username"]))
    if not user.check_password(request.data(["password"])):
        return Response({"details":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    token = str(token)
    login_serializer = UserSerializer(user)
    return Response({"token":token, "user":login_serializer.data}, status=status.HTTP_302_FOUND)
#Register API
@api_view(["POST"])
def ResgisterAPI(request):
    register_serializer = RegisterSerializer(data=request.data)
    if register_serializer.is_valid():
        register_serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        token=str(token)
        return Response({'token':token, "user":register_serializer.data}, status=status.HTTP_201_CREATED)    
    return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getAll(request):
    if request.method == "GET":
        all_resume = Resume.objects.all()
        resume_serializer = ResumeSerializer(all_resume, many=True)
        return Response(resume_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET","POST"])
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