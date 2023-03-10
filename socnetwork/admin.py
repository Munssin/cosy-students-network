from django.contrib import admin
from .models import Message, ResumeF, Message_url, UsersProfile

# Register your models here.
admin.site.register(Message)
admin.site.register(Message_url)
admin.site.register(ResumeF)
admin.site.register(UsersProfile)