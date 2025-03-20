from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Genome)
class genomeAdmin(admin.ModelAdmin):
    list_display = ('bin_id','source','habitat','gtdb_classification')
