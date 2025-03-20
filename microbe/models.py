from django.db import models
from django.contrib.postgres.fields import ArrayField

class Microbe(models.Model):
    """
    Model representing microbial organisms and their taxonomic, functional, and habitat information.
    """
    # Full taxonomy string
    taxonomy = models.TextField(
        unique=True,
        db_index=True,
        help_text="Complete GTDB taxonomy string"
    )

    # Individual taxonomic ranks
    domain = models.CharField(
        max_length=100,
        null=True,  # Allow null values
        db_index=True,
        help_text="Domain classification (d__)"
    )
    phylum = models.CharField(
        max_length=100,
        null=True,  # Allow null values
        db_index=True,
        help_text="Phylum classification (p__)"
    )
    class_name = models.CharField(
        max_length=100,
        null=True,  # Allow null values
        db_index=True,
        help_text="Class classification (c__)"
    )
    order = models.CharField(
        max_length=100,
        null=True,  # Allow null values
        db_index=True,
        help_text="Order classification (o__)"
    )
    family = models.CharField(
        max_length=100,
        null=True,  # Allow null values
        db_index=True,
        help_text="Family classification (f__)"
    )
    genus = models.CharField(
        max_length=100,
        null=True,  # Allow null values
        db_index=True,
        help_text="Genus classification (g__)"
    )
    species = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text="Species classification (s__), if available"
    )

    # Functional and environmental information
    functions = ArrayField(
        models.CharField(max_length=100),
        help_text="List of metabolic or functional capabilities"
    )
    habitats = ArrayField(
        models.CharField(max_length=100),
        help_text="List of habitats where the microbe is found"
    )
    sources = ArrayField(
        models.CharField(max_length=20),
        help_text="List of source identifiers (e.g., SRR numbers)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['taxonomy']),
            models.Index(fields=['domain']),
            models.Index(fields=['phylum']),
            models.Index(fields=['genus', 'species']),
        ]
        ordering = ['domain', 'phylum', 'genus', 'species']

    def __str__(self):
        """String representation of the Microbe model."""
        if self.species:
            return f"{self.genus} {self.species}"
        return self.genus

    def get_full_name(self):
        """Returns the full taxonomic name."""
        if self.species:
            return f"{self.genus} {self.species}"
        return self.genus

    def get_functions_list(self):
        """Returns the list of functions as a comma-separated string."""
        return ", ".join(self.functions)

    def get_habitats_list(self):
        """Returns the list of habitats as a comma-separated string."""
        return ", ".join(self.habitats)

    def get_sources_count(self):
        """Returns the number of sources this microbe was found in."""
        return len(self.sources)
