from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from subprocess import Popen, PIPE
import os
from django.conf import settings



def home(request):
    return render(request, "home.html")