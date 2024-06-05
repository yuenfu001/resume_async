from django.urls import path
from . import views
urlpatterns = [
    path("resume/",views.getAll, name="getall"),
    path("all_users/",views.getUser, name="allusers"),
    path("register_user/",views.ResgisterAPI, name="register"),
    path("login/",views.login, name="login"),
    
]
