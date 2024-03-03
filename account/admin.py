from django.contrib import admin

from .models import MyUser, Profile 

admin.site.register(MyUser)
admin.site.register(Profile)

