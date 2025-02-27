from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostModel(models.Model):
    topic =  models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='blog_pics/',blank=True, null=True)
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title 

class Comment(models.Model):
    blog = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment_on_the_post = models.TextField(null=True, blank=True)
    your_name = models.CharField(max_length=30, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=30, null=True,blank=True)
    your_email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.your_name
    
class Contacts(models.Model):
    your_name = models.CharField(max_length=30, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=30, null=True,blank=True)
    your_email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"Hey {self.your_name} your message of {self.subject} was well received"