from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resume(User):
    company = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    college = models.CharField(max_length=50)
    achievement = models.TextField()
    hobbies = models.TextField()

    def __str__(self):
        return f"{self.company}"
    
