from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'microbe'

urlpatterns = [
    path('', views.microbes, name='microbes'),
    path('<int:id>/', views.microbe_detail, name='microbe_detail'),
]
