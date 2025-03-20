from django.db import models

class SeawaterFactor(models.Model):
    """
    Model representing oceanographic measurements and environmental parameters of seawater.
    """
    id = models.AutoField(primary_key=True)

    # Geographic coordinates
    latitude = models.FloatField(db_index=True, help_text="Latitude coordinate, e.g., 28.743")
    longitude = models.FloatField(db_index=True, help_text="Longitude coordinate, e.g., -80.837")

    # Chemical parameters
    salinity = models.FloatField(null=True, blank=True, help_text="Salinity measurement in PSU")
    silicate = models.FloatField(null=True, blank=True, help_text="Silicate concentration in μmol/L")
    phosphate = models.FloatField(null=True, blank=True, help_text="Phosphate concentration in μmol/L")
    nitrate = models.FloatField(null=True, blank=True, help_text="Nitrate concentration in μmol/L")
    iron = models.FloatField(null=True, blank=True, help_text="Iron concentration in μmol/L")

    # Physical parameters
    ph = models.FloatField(null=True, blank=True, help_text="pH value")
    dissolved_oxygen = models.FloatField(null=True, blank=True, help_text="Dissolved molecular oxygen in μmol/kg")
    ocean_temperature = models.FloatField(null=True, blank=True, help_text="Ocean temperature in °C")

    # Current information
    seawater_direction = models.FloatField(null=True, blank=True, help_text="Sea water direction in degrees")
    seawater_speed = models.FloatField(null=True, blank=True, help_text="Seawater speed in m/s")

    # Biological parameters
    primary_productivity = models.FloatField(null=True, blank=True, help_text="Primary productivity in mg C/m³/day")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['ocean_temperature']),
            models.Index(fields=['salinity']),
            models.Index(fields=['ph']),
        ]
        ordering = ['latitude', 'longitude']
        # Ensure we don't have duplicate measurements for the same location
        unique_together = ['latitude', 'longitude']

    def __str__(self):
        """String representation of the SeawaterFactor model."""
        return f"Location ({self.latitude}, {self.longitude}) - Temp: {self.ocean_temperature}°C"

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
    def is_tropical(self):
        """Returns whether the location is in tropical waters (between 23.5°N and 23.5°S)."""
        return -23.5 <= self.latitude <= 23.5

    @property
    def water_quality_index(self):
        """
        Calculate a simple water quality index based on available parameters.
        Higher values indicate better water quality (simplified example).
        """
        # This is a simplified example - a real index would be more complex
        factors = []

        # pH factor (optimal range 7.8-8.3)
        if self.ph is not None:
            if 7.8 <= self.ph <= 8.3:
                factors.append(1.0)
            else:
                distance = min(abs(self.ph - 7.8), abs(self.ph - 8.3))
                factors.append(max(0, 1.0 - distance/0.5))

        # Oxygen factor (higher is better, up to saturation)
        if self.dissolved_oxygen is not None:
            # Assuming 200 μmol/kg is a good baseline
            factors.append(min(1.0, self.dissolved_oxygen/200))

        # Nutrient balance factor (lower phosphate is generally better for open ocean)
        if self.phosphate is not None:
            factors.append(max(0, 1.0 - self.phosphate/0.1))

        if not factors:
            return None

        return sum(factors) / len(factors) * 100  # Scale to 0-100
