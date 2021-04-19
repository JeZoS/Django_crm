from django.contrib import admin
from .models import Agent,User,Lead,UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
