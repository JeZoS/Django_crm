from django.contrib import admin
from .models import Agent,User,Lead
# Register your models here.

admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
