from django.db import models

# Create your models here.
class Virus(models.Model):
    """
    Virus data model for storing basic virus information
    """

    # Basic Information
    virus_id = models.CharField(max_length=100, primary_key=True, verbose_name="Virus ID")
    length = models.IntegerField(verbose_name="Length")
    multi = models.FloatField(verbose_name="Multiplicity")
    type = models.CharField(max_length=20, verbose_name="Type")
    quality = models.CharField(max_length=50, verbose_name="Quality")
    source = models.CharField(max_length=100, verbose_name="Source")
    taxonomy = models.CharField(max_length=100, blank=True, null=True, verbose_name="Taxonomy")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Time")

    class Meta:
        verbose_name = "Virus"
        verbose_name_plural = "Viruses"
        ordering = ['virus_id']

    def __str__(self):
        return self.virus_id

    def get_absolute_url(self):
        """Get the URL for the virus detail page"""
        from django.urls import reverse
        return reverse('virus:detail', args=[str(self.virus_id)])
