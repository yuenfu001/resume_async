from django.urls import path
from . import views
urlpatterns = [
    path("all_resumes/",views.getAllResume, name="getall"),
    path("resume/<str:pk>/",views.getSpecificResume, name="specific_resume"),
    path("all_users/",views.getAllUser, name="allusers"),
    path("user/<str:pk>/",views.getSpecificUser, name="specific_user"),
    path("register_user/",views.ResgisterAPI, name="register"),
    path("login/",views.login, name="login"),
    
]
