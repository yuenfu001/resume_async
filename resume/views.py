from django.shortcuts import render,get_object_or_404
from .models import Resume
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer,ResumeSerializer
from rest_framework.decorators import api_view, APIView
from asgiref.sync import sync_to_async
# Create your views here.

#GET All resume and POST a new resume
@swagger_auto_schema(
        methods=["POST"],
        request_body=ResumeSerializer,
        operation_description= "Add Resume"
)
@sync_to_async
@api_view(["GET","POST"])
def getAllResume(request):
    if request.method == "GET":
        all_resume = Resume.objects.all()
        resume_serializer = ResumeSerializer(all_resume, many=True)
        return Response(resume_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        create_resume = ResumeSerializer(data=request.data)
        if create_resume.is_valid():
            create_resume.save()
            return Response(create_resume.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
        methods=["PUT","DELETE"],
        request_body=ResumeSerializer,
        operation_description= "Specific resume"
)
@sync_to_async
@api_view(["GET","PUT","DELETE"])
def getSpecificResume(request,pk):
    specific_resume = get_object_or_404(Resume, id=pk)
    if request.method == "GET":
        specific_resume_serializer = ResumeSerializer(specific_resume)
        return Response(specific_resume_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        update_resume_serializer = ResumeSerializer(specific_resume,data=request.data)
        if update_resume_serializer.is_valid():
            update_resume_serializer.save()
            return Response(update_resume_serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == "DELETE":
        specific_resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
        methods=["POST"],
        request_body=UserSerializer,
        operation_description= "Specific user"
)
@sync_to_async
@api_view(["POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"details": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        
        if not user.check_password(password):
            return Response({"details": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        token = str(token.key)
        
        login_serializer = UserSerializer(user)
        return Response({"token": token, "user": login_serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print("Error:", e)  # Debug statement
        return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(
        methods=["POST"],
        request_body=RegisterSerializer,
        operation_description= "Add user"
)
@sync_to_async
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

@sync_to_async
@api_view(["GET"])
def getAllUser(request):
    if request.method == "GET":
        all_users = User.objects.all()
        allusers_serializer = UserSerializer(all_users, many=True)
        return Response(allusers_serializer.data, status=status.HTTP_200_OK)  
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
        methods=["PUT","DELETE"],
        request_body=UserSerializer,
        operation_description= "Specific user"
)
@sync_to_async
@api_view(["GET","PUT","DELETE"])
def getSpecificUser(request, pk):
    specific_user = get_object_or_404(User, pk=pk)
    if request.method == "GET":
        specific_user_serializer = UserSerializer(specific_user)
        token = get_object_or_404(Token, user=specific_user)
        token = str(token)
        return Response({"token":token, "unique_user":specific_user_serializer.data}, status=status.HTTP_302_FOUND)
    elif request.method == "PUT":
        update_user_serializer = UserSerializer(specific_user,data=request.data)
        if update_user_serializer.is_valid():
            update_user_serializer.save()
            return Response(update_user_serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == "DELETE":
        specific_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
