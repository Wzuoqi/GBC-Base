from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Virus)
class virusAdmin(admin.ModelAdmin):
    list_display = ('virus_id','type','quality','taxonomy')
