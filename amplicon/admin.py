from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Amplicon)
class ampliconAdmin(admin.ModelAdmin):
    list_display = ('id','run','habitat','host')
