from django.contrib import admin
from .models import *

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'feedback_type', 'subject', 'created_at')
    list_filter = ('feedback_type', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
