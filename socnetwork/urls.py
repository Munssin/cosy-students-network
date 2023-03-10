from django.urls import path
from . import views

urlpatterns = [
    # інші URL-шляхи ...
    path('create_group/', views.create_group, name='create_group'),
]

urlpatterns = [
]
