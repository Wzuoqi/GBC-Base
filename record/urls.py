from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'record'

urlpatterns = [
    path('', views.recordes, name='record'),
    path('<str:id>/', views.record_detail, name='record_detail'),
]
