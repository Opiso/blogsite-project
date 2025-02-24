from django.contrib import admin
from .models import PostModel, Comment
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display=('title', 'date_created','date_updated','content','author','picture')

admin.site.register(PostModel, PostModelAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('comment_on_the_post', 'your_name','date','subject','your_email','message')

admin.site.register(Comment, CommentAdmin)