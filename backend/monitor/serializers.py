from rest_framework import serializers
from .models import SatelliteImage, WaterSensor, HealthReport

class SatelliteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatelliteImage
        fields = '__all__'

class WaterSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSensor
        fields = '__all__'

class HealthReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthReport
        fields = '__all__'
