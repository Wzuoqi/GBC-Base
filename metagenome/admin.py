from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Metagenome)
class metagenomeAdmin(admin.ModelAdmin):
    list_display = ('run_id','habitat','geo_location')
