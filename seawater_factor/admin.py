from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(SeawaterFactor)
class seawaterfactorAdmin(admin.ModelAdmin):
    list_display = ('id','latitude','longitude','ph','ocean_temperature')
