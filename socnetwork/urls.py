from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('send/', views.send, name='send'),
    path('getMessages/', views.getMessages, name='getMessages'),
    path('getFiles/', views.getFiles, name='getFiles'),
    path('send_url/', views.send_url, name='send_url'),
    path('getMessages_url/', views.getMessages_url, name='getMessages_url'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)