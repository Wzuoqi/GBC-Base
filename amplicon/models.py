from django.db import models

# Create your models here.

class Amplicon(models.Model):
    id = models.AutoField(primary_key=True)
    run = models.CharField(max_length=100, unique=True, db_index=True, help_text="Run ID, e.g., SRR15928122")
    assay_type = models.CharField(max_length=100, null=True, blank=True, help_text="Sequencing assay type, e.g., AMPLICON")
    bioproject = models.CharField(max_length=100, db_index=True, null=True, blank=True, help_text="Bioproject ID, e.g., PRJNA764039")

    # Environmental and Geographic Information
    habitat = models.CharField(max_length=200, null=True, blank=True, help_text="Habitat type, e.g., Mangrove")
    latitude = models.CharField(max_length=100, null=True, blank=True, help_text="Latitude, e.g., 16.3862 S")
    longitude = models.CharField(max_length=100, null=True, blank=True, help_text="Longitude, e.g., 145.5638 E")
    geo_location = models.CharField(max_length=500, null=True, blank=True, help_text="Geographic location, e.g., Australia: GBR")
    collection_date = models.CharField(max_length=100, null=True, blank=True, help_text="Collection date")

    # Host Information
    host = models.CharField(max_length=500, db_index=True, null=True, blank=True, help_text="Host, e.g., coral")
    sample_isolated = models.CharField(max_length=500, null=True, blank=True, help_text="Sample isolated from, e.g., coral")

    # Sequencing Information
    bases = models.BigIntegerField(null=True, blank=True, help_text="Number of bases")
    biosample = models.CharField(max_length=100, db_index=True, null=True, blank=True, help_text="Biosample ID, e.g., SAMN21467046")
    layout = models.CharField(max_length=50, null=True, blank=True, help_text="Sequencing layout, e.g., PAIRED")
    instrument = models.CharField(max_length=200, null=True, blank=True, help_text="Sequencing instrument, e.g., Illumina MiSeq")
    library_source = models.CharField(max_length=100, null=True, blank=True, help_text="Library source, e.g., GENOMIC")

    # Amplicon Specific Information
    amplicon_type = models.CharField(max_length=50, null=True, blank=True, help_text="Amplicon type, e.g., 16S")
    reference = models.URLField(max_length=500, null=True, blank=True, help_text="Reference link, e.g., https://www.ncbi.nlm.nih.gov/sra/SRR15928122")

    def __str__(self):
        return f"{self.run} - {self.host} ({self.geo_location})"

    class Meta:
        ordering = ['run', 'geo_location', 'host', 'collection_date']
        indexes = [
            models.Index(fields=['run', 'geo_location', 'host', 'collection_date']),
            models.Index(fields=['bioproject']),
            models.Index(fields=['biosample']),
            models.Index(fields=['amplicon_type']),
        ]
