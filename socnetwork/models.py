from django.db import models
from django.conf import settings

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000000)
  
class Message_url(models.Model):
    value = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000000)

class ResumeF(models.Model):
    user = models.CharField(max_length=100, null=True)
    file_name = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='../media/', null=True)

    def __str__(self):
        return self.file_name

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)