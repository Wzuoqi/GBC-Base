from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Gene)
class geneAdmin(admin.ModelAdmin):
    list_display = ('gene_id','preferred_name','description','source')
