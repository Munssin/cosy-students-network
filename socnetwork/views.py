from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, "login/index.html")

@csrf_exempt
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2 :
            return HttpResponse("Your password and conform password are not Same!")
        else:
            new_user=User.objects.create_user(uname,email,pass1)
            new_user.save()
            return redirect('login')
        
      

    return render(request, "login/signup.html")


def LoginPage(request):
    if request.method=='POST': 
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            return HttpResponse("Username or password is incorrect!")

    return render(request, "login/login.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')

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