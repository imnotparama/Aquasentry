from django.db import models

class SatelliteImage(models.Model):
    image = models.ImageField(upload_to='satellite_images/')
    captured_at = models.DateTimeField(auto_now_add=True)
    chlorophyll_index = models.FloatField(help_text="Detected chlorophyll percentage (0-100)")
    turbidity_index = models.FloatField(help_text="Detected turbidity percentage (0-100)")
    risk_score = models.FloatField(help_text="Calculated risk score (0-100)")
    location_name = models.CharField(max_length=255, default="Unknown Location")

    def __str__(self):
        return f"Satellite Scan - {self.location_name} ({self.captured_at})"

class WaterSensor(models.Model):
    sensor_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    ph = models.FloatField()
    turbidity = models.FloatField()
    temperature = models.FloatField()
    dissolved_oxygen = models.FloatField()
    conductivity = models.FloatField()
    
    def __str__(self):
        return f"Sensor {self.sensor_id} at {self.timestamp}"

class HealthReport(models.Model):
    SYMPTOM_TYPES = [
        ('GI', 'Gastrointestinal (Diarrhea, Vomiting)'),
        ('NEURO', 'Neurological (Dizziness, Seizures)'),
        ('DERM', 'Dermatological (Rashes, Itching)'),
        ('OTHER', 'Other'),
    ]
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    symptom_type = models.CharField(max_length=10, choices=SYMPTOM_TYPES)
    severity = models.IntegerField(default=1, help_text="1 (Mild) to 10 (Critical)")
    latitude = models.FloatField()
    longitude = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Health Report: {self.symptom_type} (Severity: {self.severity})"
