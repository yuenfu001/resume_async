from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    college = models.CharField(max_length=50)
    achievement = models.TextField()
    hobbies = models.TextField()

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resume"
    def __str__(self):
        return f"{self.company}"
    
