from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(SoilFactor)
class soilfactorAdmin(admin.ModelAdmin):
    list_display = ('id','latitude','longitude','average_organic_carbon','average_total_carbon')
