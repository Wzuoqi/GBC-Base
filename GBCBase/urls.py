"""
URL configuration for GBCBase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="homepage"),

    # record
    path('record/', include('record.urls')),

    # microbe
    path('microbe/', include('microbe.urls')),

    # metagenome
    path('metagenome/', include('metagenome.urls')),

    # amplicon
    path('amplicon/', include('amplicon.urls')),

    # genome
    path('genome/', include('genome.urls')),

    # virus
    path('virus/', include('virus.urls')),

]
