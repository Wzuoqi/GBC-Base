from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('DB', 'Database Content'),
        ('BUG', 'Bug Report'),
        ('FEATURE', 'Feature Request'),
        ('RECORD', 'Record Submission'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback_type = models.CharField(
        max_length=10,
        choices=FEEDBACK_TYPES,
        default='OTHER'
    )
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.subject} - {self.name} ({self.created_at.strftime('%Y-%m-%d')})"