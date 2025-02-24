from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     email = models.EmailField(max_length=100, null=True, blank=True, unique=False)
     phone_number = models.CharField(max_length=20, blank=True,null=True)
     address = models.CharField(max_length=100)
     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
     brief_description = models.TextField(max_length=250, null=True, blank=True)

     def __str__(self):
         return f"{self.user.first_name} {self.user.last_name}"