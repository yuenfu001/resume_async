from django.urls import path
from . import views
urlpatterns = [
    path("resume",views.getAll, name="getall"),
    path("all_users",views.getUser, name="allusers"),
    
]
