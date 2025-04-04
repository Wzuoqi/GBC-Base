from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'genome'

urlpatterns = [
    path('', views.genomes, name='genomes'),
    path('<str:bin_id>/', views.genome_detail, name='genome_detail'),
]
