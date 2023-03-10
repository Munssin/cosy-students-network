#Зразок коду створення ноих груп код має бути розкиданий по таких файлах



#models.py
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)



#urls.py
from django.urls import path
from . import views

urlpatterns = [
    # інші URL-шляхи ...
    path('create_group/', views.create_group, name='create_group'),
]




#views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        members = request.POST.getlist('members')

        # перевірка чи введено назву групи
        if not name:
            return render(request, 'create_group.html', {'error': 'Please enter a group name.'})

        # створення нової групи
        group = Group.objects.create(name=name)

        # додавання користувачів до групи
        if members:
            for member_id in members:
                member = User.objects.get(id=member_id)
                group.members.add(member)

        # перенаправлення на сторінку зі списком груп
        return redirect('groups')

    # відображення форми для створення нової групи
    return render(request, 'create_group.html')