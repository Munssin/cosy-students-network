from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from .models import Message, Message_url, ResumeF, UsersProfile, Room
from django.conf import settings
from django.urls import reverse
import json
import os
import re

class ShowProfilePageView(DetailView):
    model = UsersProfile
    template_name = 'profile/user-profile.html'

    def get_context_data(self, *args, **kwargs):
        users = UsersProfile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(UsersProfile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context

def user_workplace_full(request, room_id, under_room_id):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('login')

    room_c = get_object_or_404(Room, id=room_id)
    members_list = f'[{room_c.members}]'
    members_list = json.loads(members_list)

    if request.user.id in members_list:
        if request.method == 'POST':
            uploaded_file = request.FILES['myfiles[]']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            name = name
            new_ResumeF=ResumeF.objects.create(user=username,file_name=name,size=0,file=f'/media/{name}',room=f"{room_id}_{under_room_id}")
            new_ResumeF.save()
            return HttpResponseRedirect(request.path)


        room = Room.objects.all()
        page_workplace = get_object_or_404(room, id=room_id) 
        context = {
        'page_workplace':page_workplace,
        'room_id':room_id,
        'under_room_id':under_room_id,
        'username': username
        }

        return render(request, 'profile/user-workplace.html', context)
    else:
        return HttpResponse(f"You are not a member of this group! {request.user.id}")


def edit_profile(request):
    userid = request.user.id
    user_profile = get_object_or_404(UsersProfile, user_id=userid)

    if request.method == "POST":
        if request.POST.get("about"):
            user_profile.about = request.POST.get("about")
        if request.POST.get("university"):
            user_profile.university = request.POST.get("university")
        if 'avatar-profile' in request.FILES:
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
        user=authenticate(request, username=username, password=pass1)
        usermail=authenticate(request, email=username, password=pass1)

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

    return render(request, 'profile/user-workplace_null.html', {'username': username})

def send(request):
    message = request.POST.get('message')
    under_room = request.POST.get('under_room_id')
    room = request.POST.get('room_id')
    username = request.user.username

    if len(message) != 0:
        url_regex = r'(https?://[^\s]+)'
        match = re.search(url_regex, message)

        if match:
            new_message_url_c = Message_url.objects.create(value=message, user=username, room=f"{room}_{under_room}")
            new_message_url_c.save()
            new_message = Message.objects.create(value=message, user=username, room=f"{room}_{under_room}")
            new_message.save()
        else:
            new_message = Message.objects.create(value=message, user=username, room=f"{room}_{under_room}")
            new_message.save()
    else:
        print("error message empty")

def send_url(request):
    message = request.POST.get('message_url')
    username = request.user.username
    under_room = request.POST.get('under_room_id')
    room = request.POST.get('room_id')

    if len(message) != 0:
        url_regex = r'(https?://[^\s]+)'
        match = re.search(url_regex, message)

        if match:
            new_message_url = Message_url.objects.create(value=message, user=username, room=f"{room}_{under_room}")
            new_message_url.save()
        else:
            print("not url in message")
    else:
        print("error message empty")

def getMessages(request, room_id, under_room_id):

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')
    messages = Message.objects.all().filter(room=f"{room_id}_{under_room_id}")

    return JsonResponse({"messages":list(messages.values()), "nickname": username})

def getMessages_url(request, room_id, under_room_id):

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')
    messages = Message_url.objects.all().filter(room=f"{room_id}_{under_room_id}")

    return JsonResponse({"messages_url":list(messages.values()), "nickname": username})

def getFiles(request, room_id, under_room_id):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')
    files = ResumeF.objects.all().filter(room=f"{room_id}_{under_room_id}")

    return JsonResponse({"files":list(files.values()), "nickname": username})

def getRooms(request):
    room = Room.objects.all()
    username_r = request.user.id

    return JsonResponse({"room":list(room.values()), "username_r":username_r})

def user_profile_my(request):
    if request.user.is_authenticated:
        userid = request.user.id
        page_user = get_object_or_404(UsersProfile, user_id=userid)
        return redirect(reverse('user_profile', args=[page_user.id]))
    else:
        return redirect('/')

def settings_group(request, room_id):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect('/')

    if request.user.groups.filter(name='Moderation').exists():
        room = get_object_or_404(Room, id=room_id)
        pre_members = f'[{room.members}]'
        pre_members = json.loads(pre_members)
        members = []
        for r_user_id in pre_members:
            user_name = get_object_or_404(UsersProfile, user_id=r_user_id)
            members.append(user_name.user.username)

        avatars_list = []

        for id_for_avatars in pre_members:
            user_id_for_avatar = get_object_or_404(User, id=id_for_avatars)
            avatar = get_object_or_404(UsersProfile, user_id=user_id_for_avatar)
            avatars_list.append(avatar.avatar)

        context = {
        'room_id':room_id,
        'members_list':members,
        'avatars_list':avatars_list,
        }

        return render(request, 'profile/settings-groups.html', context)
    else:
        return HttpResponse("You are not in moderation!")

def send_member_username(request):
    member_username = request.POST.get('member_username')
    room_id = request.POST.get('room_id')
    room = get_object_or_404(Room, id=room_id)

    if len(member_username) != 0:
        user_id = get_object_or_404(User, username=member_username)

        pre_members = f'[{room.members}]'
        pre_members = json.loads(pre_members)
        members = []
        members.append(user_id.id)

        for r_user_id in pre_members:
            user_name = get_object_or_404(UsersProfile, user_id=r_user_id)
            members.append(user_name.user.id)

        members = f"{members}"
        members = members[1:-1]
        Room.objects.filter(id=room_id).update(members=members)
    else:
        print("error member_username empty")

def send_room_name(request):
    room_name = request.POST.get('room_name')
    room_id = request.POST.get('room_id')

    if len(room_name) != 0:
        Room.objects.filter(id=room_id).update(name=room_name)
    else:
        print("error name_room empty")

def download(request, document_id):
    document = get_object_or_404(ResumeF, pk=document_id)
    with open(f'{settings.BASE_DIR}{document.file}', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/adminupload")
        response['Content-Disposition'] = f'inline; filename={document.file_name}'
        return response

def create_room(request):
    username = request.user.username
    if request.user.groups.filter(name='Moderation').exists():
        if request.method == "POST":
            if len(request.POST.get("room_name")) != 0:
                c_room = Room.objects.create(name=request.POST.get("room_name"), members=request.user.id)
                c_room.save()

                return redirect('../')
            else:
                return redirect('../')
        else:
            return render(request, 'profile/create-room.html')
    else:
        return render(request, 'profile/error-page.html')

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()

    return redirect('/')