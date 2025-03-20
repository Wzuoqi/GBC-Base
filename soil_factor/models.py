from django.db import models

class SoilFactor(models.Model):
    """
    Model representing soil composition measurements at different depths and locations.
    """
    id = models.AutoField(primary_key=True)

    # Geographic coordinates
    latitude = models.FloatField(db_index=True, help_text="Latitude coordinate, e.g., 28.743")
    longitude = models.FloatField(db_index=True, help_text="Longitude coordinate, e.g., -80.837")

    # Organic Carbon measurements
    average_organic_carbon = models.FloatField(null=True, blank=True, help_text="Average organic carbon content (%)")
    organic_carbon_upper_depth = models.IntegerField(null=True, blank=True, help_text="Upper depth for organic carbon measurement (cm)")
    organic_carbon_lower_depth = models.IntegerField(null=True, blank=True, help_text="Lower depth for organic carbon measurement (cm)")

    # Total Carbon measurements
    average_total_carbon = models.FloatField(null=True, blank=True, help_text="Average total carbon content (%)")
    total_carbon_upper_depth = models.IntegerField(null=True, blank=True, help_text="Upper depth for total carbon measurement (cm)")
    total_carbon_lower_depth = models.IntegerField(null=True, blank=True, help_text="Lower depth for total carbon measurement (cm)")

    # Organic Matter measurements
    average_organic_matter = models.FloatField(null=True, blank=True, help_text="Average organic matter content (%)")
    organic_matter_upper_depth = models.IntegerField(null=True, blank=True, help_text="Upper depth for organic matter measurement (cm)")
    organic_matter_lower_depth = models.IntegerField(null=True, blank=True, help_text="Lower depth for organic matter measurement (cm)")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['average_organic_carbon']),
            models.Index(fields=['average_total_carbon']),
            models.Index(fields=['average_organic_matter']),
        ]
        ordering = ['latitude', 'longitude']
        # Ensure we don't have duplicate measurements for the same location
        unique_together = ['latitude', 'longitude']

    def __str__(self):
        """String representation of the SoilFactor model."""
        return f"Soil at ({self.latitude}, {self.longitude}) - OC: {self.average_organic_carbon}%"

    def get_coordinates(self):
        """Returns formatted coordinates."""
        return f"{self.latitude}, {self.longitude}"

    @property
    def location_description(self):
        """Returns a description of the location based on hemisphere."""
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        return f"{abs(self.latitude)}° {lat_dir}, {abs(self.longitude)}° {lon_dir}"

    @property
    def organic_carbon_depth_range(self):
        """Returns the depth range for organic carbon measurements."""
        if self.organic_carbon_upper_depth is not None and self.organic_carbon_lower_depth is not None:
            return f"{self.organic_carbon_upper_depth}-{self.organic_carbon_lower_depth} cm"
        return "Unknown"

    @property
    def total_carbon_depth_range(self):
        """Returns the depth range for total carbon measurements."""
        if self.total_carbon_upper_depth is not None and self.total_carbon_lower_depth is not None:
            return f"{self.total_carbon_upper_depth}-{self.total_carbon_lower_depth} cm"
        return "Unknown"

    @property
    def organic_matter_depth_range(self):
        """Returns the depth range for organic matter measurements."""
        if self.organic_matter_upper_depth is not None and self.organic_matter_lower_depth is not None:
            return f"{self.organic_matter_upper_depth}-{self.organic_matter_lower_depth} cm"
        return "Unknown"

    @property
    def carbon_to_organic_matter_ratio(self):
        """
        Calculate the ratio of total carbon to organic matter.
        This can be useful for soil characterization.
        """
        if self.average_total_carbon and self.average_organic_matter and self.average_organic_matter > 0:
            return round(self.average_total_carbon / self.average_organic_matter, 2)
        return None

    @property
    def soil_carbon_category(self):
        """
        Categorize soil based on organic carbon content.

        Very Low: < 0.5%
        Low: 0.5-1.0%
        Medium: 1.0-2.0%
        High: 2.0-4.0%
        Very High: > 4.0%
        """
        if self.average_organic_carbon is None:
            return "Unknown"

        if self.average_organic_carbon < 0.5:
            return "Very Low"
        elif self.average_organic_carbon < 1.0:
            return "Low"
        elif self.average_organic_carbon < 2.0:
            return "Medium"
        elif self.average_organic_carbon < 4.0:
            return "High"
        else:
            return "Very High"
