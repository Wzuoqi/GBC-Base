from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Microbe)
class microbeAdmin(admin.ModelAdmin):
    list_display = ('taxonomy','functions','habitats','sources')
