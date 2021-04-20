from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL)


class Agent(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


def post_user_create_signal(sender, instance, created, **kwargs):
    # print(instance)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_create_signal, sender=User)
