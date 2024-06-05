from django.shortcuts import render,get_object_or_404
from .models import Resume
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer,ResumeSerializer
from rest_framework.decorators import api_view, APIView
from asgiref.sync import sync_to_async
# Create your views here.

#GET All resume and POST a new resume
@api_view(["GET","POST"])
async def getAllResume(request):
    if request.method == "GET":
        all_resume = await sync_to_async(Resume.objects.all)()
        resume_serializer = ResumeSerializer(all_resume, many=True)
        return Response(resume_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        create_resume = ResumeSerializer(data=request.data)
        if create_resume.is_valid():
            await sync_to_async(create_resume.save)()
            return Response(create_resume.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#GET, UPDATE,DELETE specific Resume
@api_view(["GET","PUT","DELETE"])
async def getSpecificResume(request,pk):
    specific_resume = await sync_to_async(get_object_or_404)(Resume, id=pk)
    if request.method == "GET":
        specific_resume_serializer = ResumeSerializer(specific_resume)
        return Response(specific_resume_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        update_resume_serializer = ResumeSerializer(specific_resume,data=request.data)
        if update_resume_serializer.is_valid():
            await sync_to_async(update_resume_serializer.save)()
            return Response(update_resume_serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == "DELETE":
        await sync_to_async(specific_resume.delete)()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


#Login API
@api_view(["POST"])
async def login(request):
    try:
        print("Request data:", request.data)  # Debug statement
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"details": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = await sync_to_async(get_object_or_404)(User, username=username)
        
        if not user.check_password(password):
            return Response({"details": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = await sync_to_async(Token.objects.get_or_create)(user=user)
        token = str(token.key)
        
        login_serializer = UserSerializer(user)
        return Response({"token": token, "user": login_serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print("Error:", e)  # Debug statement
        return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Register API
@api_view(["POST"])
async def ResgisterAPI(request):
    register_serializer = RegisterSerializer(data=request.data)
    if register_serializer.is_valid():
        await sync_to_async(register_serializer.save)()
        user = await sync_to_async(User.objects.get)(username=request.data['username'])
        user.set_password(request.data["password"])
        await sync_to_async(user.save)()
        token = await sync_to_async(Token.objects.create)(user=user)
        token=str(token)
        return Response({'token':token, "user":register_serializer.data}, status=status.HTTP_201_CREATED)    
    return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#GET All Users
@api_view(["GET"])
async def getAllUser(request):
    if request.method == "GET":
        all_users = await sync_to_async(User.objects.all)()
        allusers_serializer = UserSerializer(all_users, many=True)
        return Response(allusers_serializer.data, status=status.HTTP_200_OK)  
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
#GET, UPDATE,DELETE specific user
@api_view(["GET","PUT","DELETE"])
async def getSpecificUser(request, pk):
    specific_user = await sync_to_async(get_object_or_404)(User, pk=pk)
    if request.method == "GET":
        specific_user_serializer = UserSerializer(specific_user)
        token = await sync_to_async(get_object_or_404)(Token, user=specific_user)
        token = str(token)
        return Response({"token":token, "unique_user":specific_user_serializer.data}, status=status.HTTP_302_FOUND)
    elif request.method == "PUT":
        update_user_serializer = UserSerializer(specific_user,data=request.data)
        if update_user_serializer.is_valid():
            await sync_to_async(update_user_serializer.save)()
            return Response(update_user_serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == "DELETE":
        await sync_to_async(specific_user.delete)()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)