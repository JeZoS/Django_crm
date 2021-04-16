from django.db import models
from django.contrib.auth.models import AbstractUser  

# Create your models here.
class User(AbstractUser):
    pass

class Lead(models.Model):

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent",on_delete=models.CASCADE)

class Agent(models.Model):

    def __str__(self):
        return self.user.username 
    

    user = models.OneToOneField(User,on_delete=models.CASCADE)