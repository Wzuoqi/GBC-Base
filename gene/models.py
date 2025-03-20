from django.db import models

class Gene(models.Model):
    """
    Model representing gene information from metagenomic data.
    """
    # Gene identifiers
    gene_id = models.CharField(max_length=1000, help_text="Gene identifier(s), can be multiple IDs separated by commas")
    preferred_name = models.CharField(max_length=100, null=True, blank=True, help_text="Preferred gene name if available")

    # Functional annotation
    cog_category = models.CharField(max_length=10, null=True, blank=True, help_text="COG functional category, e.g., F, T, S")
    description = models.TextField(null=True, blank=True, help_text="Functional description of the gene")
    cazy = models.CharField(max_length=100, null=True, blank=True, help_text="CAZy classification if available")

    # Source information
    source = models.CharField(max_length=100, db_index=True, help_text="Source identifier, e.g., SRR25010671")

    # Sequence data
    sequence = models.TextField(help_text="Amino acid sequence of the gene")

    # Metadata and relationships
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['gene_id']),
            models.Index(fields=['preferred_name']),
            models.Index(fields=['cog_category']),
            models.Index(fields=['source']),
        ]
        ordering = ['source', 'gene_id']

    def __str__(self):
        """String representation of the Gene model."""
        if self.preferred_name:
            return f"{self.preferred_name} ({self.gene_id.split(',')[0]})"
        return f"{self.gene_id.split(',')[0]}"

    def get_gene_ids_list(self):
        """Returns a list of individual gene IDs."""
        return [gene_id.strip() for gene_id in self.gene_id.split(',')]

    def get_short_sequence(self, length=50):
        """Returns a truncated sequence for display purposes."""
        if len(self.sequence) <= length:
            return self.sequence
        return f"{self.sequence[:length]}..."

    @property
    def gene_count(self):
        """Returns the number of gene IDs in this record."""
        return len(self.get_gene_ids_list())
