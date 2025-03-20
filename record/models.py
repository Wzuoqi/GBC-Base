from django.db import models

class Record(models.Model):
    """
    Model representing taxonomic records and their associated functional information.
    """
    id = models.AutoField(primary_key=True)
    # Taxonomic information
    taxonomy = models.TextField(db_index=True,
                               help_text="Full taxonomic lineage, e.g., d__Bacteria; p__Proteobacteria; c__Gammaproteobacteria")

    # Functional information
    function = models.CharField(max_length=200, db_index=True,
                               help_text="Functional process, e.g., methanotrophy, nitrification")
    function_type = models.CharField(max_length=50, db_index=True,
                                    help_text="Function type/category, e.g., C, N")

    # Environmental context
    habitat = models.CharField(max_length=200, db_index=True,
                              help_text="Habitat type, e.g., mangrove")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['taxonomy']),
            models.Index(fields=['function']),
            models.Index(fields=['function_type']),
            models.Index(fields=['habitat']),
            # Compound indexes for common queries
            models.Index(fields=['function_type', 'habitat']),
            models.Index(fields=['function', 'habitat']),
        ]
        ordering = ['taxonomy', 'function']
        # Ensure we don't have duplicate records
        unique_together = ['taxonomy', 'function', 'habitat']

    def __str__(self):
        """String representation of the Record model."""
        return f"{self.get_short_taxonomy()} - {self.function} ({self.habitat})"

    def get_short_taxonomy(self):
        """Returns a shortened version of the taxonomy for display."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')

        # Try to get the most specific classification
        for level in reversed(parts):
            if level and level != "s__":
                # Extract the name after the prefix (e.g., g__Nitrosopumilus_5141 -> Nitrosopumilus_5141)
                if "__" in level and level.split("__")[1]:
                    return level.split("__")[1]

        # If no specific classification found, return the domain
        if parts and parts[0]:
            return parts[0].split("__")[1] if "__" in parts[0] else parts[0]

        return "Unknown"

    def get_domain(self):
        """Extract and return the domain from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if parts and parts[0]:
            return parts[0].replace('d__', '')

        return "Unknown"

    def get_phylum(self):
        """Extract and return the phylum from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if len(parts) >= 2 and parts[1]:
            return parts[1].replace('p__', '')

        return "Unknown"

    def get_class(self):
        """Extract and return the class from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if len(parts) >= 3 and parts[2]:
            return parts[2].replace('c__', '')

        return "Unknown"

    def get_order(self):
        """Extract and return the order from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if len(parts) >= 4 and parts[3]:
            return parts[3].replace('o__', '')

        return "Unknown"

    def get_family(self):
        """Extract and return the family from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if len(parts) >= 5 and parts[4]:
            return parts[4].replace('f__', '')

        return "Unknown"

    def get_genus(self):
        """Extract and return the genus from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if len(parts) >= 6 and parts[5]:
            return parts[5].replace('g__', '')

        return "Unknown"

    def get_species(self):
        """Extract and return the species from taxonomy."""
        if not self.taxonomy:
            return "Unknown"

        parts = self.taxonomy.split('; ')
        if len(parts) >= 7 and parts[6]:
            return parts[6].replace('s__', '')

        return "Unknown"
