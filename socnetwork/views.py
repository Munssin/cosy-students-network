from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Message, Message_url, ResumeF, UsersProfile
from .forms import UsersProfileForm
from django.conf import settings
from django.urls import reverse
import os
import re
from django.views.generic.detail import DetailView

class ShowProfilePageView(DetailView):
    model = UsersProfile
    template_name = 'profile/user-profile.html'

    def get_context_data(self, *args, **kwargs):
        users = UsersProfile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(UsersProfile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context

def edit_profile(request):
    userid = request.user.id
    user_profile = get_object_or_404(UsersProfile, user_id=userid)

    if request.method == "POST":
        if request.POST.get("about"):
            user_profile.about = request.POST.get("about")
        if request.POST.get("university"):
            user_profile.university = request.POST.get("university")
        user_profile.avatar = request.FILES['avatar-profile']
        user_profile.save()
        return redirect(reverse('user_profile', args=[user_profile.id]))
    else:
        return render(request, 'profile/edit-profile.html')

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
        
      

    return render(request, "auth/login.html")


def LoginPage(request):
    if request.method=='POST': 
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)

        if user is not None:
            login(request,user)
        else: 
            return HttpResponse("Username or password is incorrect!")
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, "auth/index.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')

def user_workplace(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('login')

    if request.method == 'POST':
        uploaded_file = request.FILES['myfiles[]']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        name = name
        new_ResumeF=ResumeF.objects.create(user=username,file_name=name,size=0,file=f'/media/{name}')
        new_ResumeF.save()
        return HttpResponseRedirect(request.path)

    return render(request, 'profile/user-workplace.html', {'username': username})

def send(request):
    message = request.POST.get('message')
    username = request.user.username

    if len(message) != 0:
        url_regex = r'(https?://[^\s]+)'
        match = re.search(url_regex, message)

        if match:
            new_message_url_c = Message_url.objects.create(value=message, user=username)
            new_message_url_c.save()
        else:
            new_message = Message.objects.create(value=message, user=username)
            new_message.save()
    else:
        print("error message empty")

def send_url(request):
    message = request.POST.get('message_url')
    username = request.user.username
    
    if len(message) != 0:
        url_regex = r'(https?://[^\s]+)'
        match = re.search(url_regex, message)

        if match:
            new_message_url = Message_url.objects.create(value=message, user=username)
            new_message_url.save()
        else:
            print("not url in message")
    else:
        print("error message empty")

def getMessages(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')
    messages = Message.objects

    return JsonResponse({"messages":list(messages.values()), "nickname": username})

def getMessages_url(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')
    messages = Message_url.objects

    return JsonResponse({"messages_url":list(messages.values()), "nickname": username})

def getFiles(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')
    files = ResumeF.objects

    return JsonResponse({"files":list(files.values()), "nickname": username})

def user_profile_my(request):
    if request.user.is_authenticated:
        userid = request.user.id
        page_user = get_object_or_404(UsersProfile, user_id=userid)
        return redirect(reverse('user_profile', args=[page_user.id]))
    else:
        return redirect('/')

def settings_group(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')

    return render(request, 'profile/settings-groups.html')