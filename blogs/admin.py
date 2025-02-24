from django.contrib import admin
from .models import PostModel
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display=('title', 'date_created','date_updated','content','author','picture')

admin.site.register(PostModel, PostModelAdmin)