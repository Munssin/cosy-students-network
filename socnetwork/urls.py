from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import *
from django.contrib.auth import views as auth_views
from .models import UsersProfile

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

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="login/password_reset_form.html"),name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="login/password_reset_done.html"),name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="login/password_reset_cofirm.html"),name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="login/password_reset_complete.html"),name="pasword_reset_complete"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)