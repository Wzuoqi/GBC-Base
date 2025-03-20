from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'metagenome'

urlpatterns = [
    path('', views.metagenomees, name='metagenome'),
    path('<str:run_id>/', views.metagenome_detail, name='metagenome_detail'),
]
