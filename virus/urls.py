from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'virus'

urlpatterns = [
    path('', views.viruses, name='virus'),
    path('<str:virus_id>/', views.virus_detail, name='virus_detail'),
]
