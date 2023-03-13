from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import *
from django.contrib.auth import views as auth_views
from .models import UsersProfile
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('user_profile_my/', user_profile_my, name='user_profile_my'),
    path('send/', send, name='send'),
    path('getMessages/', getMessages, name='getMessages'),
    path('getFiles/', getFiles, name='getFiles'),
    path('send_url/', send_url, name='send_url'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('getMessages_url/', getMessages_url, name='getMessages_url'),
    path('settings_group/', settings_group, name='settings_group'),
    path('download/<int:document_id>/', download, name='download'),


    path('password-reset/', PasswordResetView.as_view(template_name='login/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'),name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)