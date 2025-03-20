from django.db import models

class Metagenome(models.Model):
    """
    Model representing metagenomic sequencing data and associated metadata.
    """
    # Sequencing identifiers
    run_id = models.CharField(max_length=100, unique=True, db_index=True,
                             help_text="Run identifier, e.g., SRR25010643")
    bioproject = models.CharField(max_length=100, db_index=True, null=True, blank=True,
                                 help_text="BioProject identifier, e.g., PRJNA985394")

    # Sequencing information
    strategy = models.CharField(max_length=50, null=True, blank=True,
                               help_text="Sequencing strategy, e.g., WGS")
    library_source = models.CharField(max_length=50, null=True, blank=True,
                                     help_text="Library source, e.g., METAGENOMIC")
    bases = models.BigIntegerField(null=True, blank=True,
                                  help_text="Number of bases sequenced")
    instrument = models.CharField(max_length=200, null=True, blank=True,
                                 help_text="Sequencing instrument, e.g., Illumina NovaSeq 6000")
    layout = models.CharField(max_length=50, null=True, blank=True,
                             help_text="Sequencing layout, e.g., PAIRED")

    # Environmental and geographic information
    habitat = models.CharField(max_length=200, db_index=True, null=True, blank=True,
                              help_text="Habitat type, e.g., Seagrass")
    collection_date = models.CharField(max_length=100, null=True, blank=True,
                                      help_text="Collection date, e.g., 2021/6/1")
    sample_isolated = models.CharField(max_length=200, null=True, blank=True,
                                      help_text="Sample isolation source, e.g., sediment")
    host = models.CharField(max_length=200, db_index=True, null=True, blank=True,
                           help_text="Host organism, e.g., Zostera marina")
    latitude = models.CharField(max_length=50, null=True, blank=True,
                               help_text="Latitude, e.g., 37.21N")
    longitude = models.CharField(max_length=50, null=True, blank=True,
                                help_text="Longitude, e.g., 122.62E")
    geo_location = models.CharField(max_length=500, null=True, blank=True,
                                   help_text="Geographic location, e.g., China:Shandong")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['run_id']),
            models.Index(fields=['bioproject']),
            models.Index(fields=['habitat']),
            models.Index(fields=['host']),
            models.Index(fields=['geo_location']),
        ]
        ordering = ['run_id']

    def __str__(self):
        """String representation of the Metagenome model."""
        return f"{self.run_id} - {self.habitat} ({self.geo_location})"

    def get_coordinates(self):
        """Returns formatted coordinates if available."""
        if self.latitude and self.longitude:
            return f"{self.latitude}, {self.longitude}"
        return "Unknown"

    @property
    def sequencing_size_gb(self):
        """Returns the sequencing size in gigabases."""
        if self.bases:
            return round(self.bases / 1_000_000_000, 2)
        return None

    @property
    def location_country(self):
        """Extracts the country from geo_location."""
        if self.geo_location and ':' in self.geo_location:
            return self.geo_location.split(':')[0]
        return self.geo_location

    @property
    def location_region(self):
        """Extracts the region from geo_location."""
        if self.geo_location and ':' in self.geo_location:
            parts = self.geo_location.split(':')
            if len(parts) > 1:
                return parts[1]
        return None
