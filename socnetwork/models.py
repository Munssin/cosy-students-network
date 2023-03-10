from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Group:
    pass



class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
