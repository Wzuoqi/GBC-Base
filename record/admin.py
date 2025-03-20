from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Record)
class recordAdmin(admin.ModelAdmin):
    list_display = ('id','taxonomy','habitat')
