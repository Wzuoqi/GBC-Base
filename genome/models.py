from django.db import models

# Create your models here.

class Genome(models.Model):
    """
    Model representing metagenomic assembled genomes (MAGs/bins) and their taxonomic/quality information.
    """
    # Bin identifiers
    bin_id = models.CharField(max_length=100, unique=True, db_index=True,
                             help_text="Unique bin identifier, e.g., SRR28393034_bin.2")
    source = models.CharField(max_length=100, db_index=True,
                             help_text="Source identifier, e.g., SRR28393034")

    # Environmental information
    habitat = models.CharField(max_length=200, null=True, blank=True, db_index=True,
                              help_text="Habitat type, e.g., Mangrove")

    # Quality metrics
    marker_lineage = models.CharField(max_length=200, null=True, blank=True,
                                     help_text="Marker lineage used for quality assessment, e.g., p__Proteobacteria (UID3880)")
    completeness = models.FloatField(null=True, blank=True,
                                    help_text="Genome completeness percentage (0-100)")
    contamination = models.FloatField(null=True, blank=True,
                                     help_text="Genome contamination percentage (0-100)")
    strain_heterogeneity = models.FloatField(null=True, blank=True,
                                           help_text="Strain heterogeneity percentage (0-100)")

    # Taxonomic classification
    gtdb_classification = models.TextField(null=True, blank=True,
                                         help_text="GTDB taxonomy classification")

    # Reference genome information
    closest_genome_reference = models.CharField(max_length=200, null=True, blank=True,
                                              help_text="Closest reference genome identifier")
    closest_genome_ani = models.FloatField(null=True, blank=True,
                                         help_text="Average Nucleotide Identity to closest reference genome")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['bin_id']),
            models.Index(fields=['source']),
            models.Index(fields=['habitat']),
            models.Index(fields=['completeness']),
            models.Index(fields=['contamination']),
        ]
        ordering = ['source', 'bin_id']

    def __str__(self):
        """String representation of the Genome model."""
        return f"{self.bin_id} ({self.get_short_taxonomy()})"

    def get_short_taxonomy(self):
        """Returns a shortened version of the taxonomy for display."""
        if not self.gtdb_classification or self.gtdb_classification == "NA":
            return "Unclassified"

        # Try to extract genus and species if available
        parts = self.gtdb_classification.split(';')
        if len(parts) >= 6:  # Has at least genus level
            genus = parts[5].replace('g__', '')
            if len(parts) >= 7 and parts[6] != 's__':  # Has species level
                species = parts[6].replace('s__', '')
                return f"{genus} {species}"
            return genus

        # Fall back to the highest available classification
        for part in reversed(parts):
            if part and part != "NA" and "__" in part:
                return part.split('__')[1]

        return "Unclassified"

    @property
    def quality_category(self):
        """
        Returns the quality category of the genome based on completeness and contamination.

        High-quality: >90% completeness, <5% contamination
        Medium-quality: >50% completeness, <10% contamination
        Low-quality: <50% completeness or >10% contamination
        """
        if self.completeness is None or self.contamination is None:
            return "Unknown"

        if self.completeness > 90 and self.contamination < 5:
            return "High-quality"
        elif self.completeness > 50 and self.contamination < 10:
            return "Medium-quality"
        else:
            return "Low-quality"

    def get_domain(self):
        """Extract and return the domain from GTDB classification."""
        if not self.gtdb_classification or self.gtdb_classification == "NA":
            return "Unknown"

        parts = self.gtdb_classification.split(';')
        if parts and parts[0] and parts[0] != "NA":
            return parts[0].replace('d__', '')

        return "Unknown"

    def get_phylum(self):
        """Extract and return the phylum from GTDB classification."""
        if not self.gtdb_classification or self.gtdb_classification == "NA":
            return "Unknown"

        parts = self.gtdb_classification.split(';')
        if len(parts) >= 2 and parts[1] and parts[1] != "NA":
            return parts[1].replace('p__', '')

        return "Unknown"
