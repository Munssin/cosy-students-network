from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    about = models.TextField(max_length=2000, null=True)
    university = models.CharField(max_length=50, null=True)
    avatar = models.ImageField(upload_to='media/profile/', null=True)

    def __str__(self):
        return str(self.user)

class Message(models.Model):
    value = models.CharField(max_length=5000)
    user = models.CharField(max_length=1000000)
  
class Message_url(models.Model):
    value = models.CharField(max_length=5000)
    user = models.CharField(max_length=1000000)

class ResumeF(models.Model):
    user = models.CharField(max_length=100, null=True)
    file_name = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='media/', null=True)

    def __str__(self):
        return self.file_name

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UsersProfile.objects.create(user=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.UsersProfile.save()