from django.contrib import admin
from .models import Author
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from .models import UserProfile


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name','username','email', 'phone_number','address','profile_picture')

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def username(self, obj):
        return obj.user.username
    
    def email(self, obj):
        return obj.user.email
    
    def phone_number(obj):
        return obj.author.phone_number
    

admin.site.register(Author, AuthorAdmin)


class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (AuthorInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)