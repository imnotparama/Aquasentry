from rest_framework import serializers
from .models import SatelliteImage, WaterSensor, HealthReport

class SatelliteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatelliteImage
        fields = '__all__'

class WaterSensorSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = WaterSensor
        fields = '__all__'

    def get_status(self, obj):
        # WHO Standards: pH 6.5-8.5, Turbidity < 5 NTU
        if obj.ph < 6.5 or obj.ph > 8.5 or obj.turbidity > 5.0:
            return "CRITICAL"
        return "SAFE"

class HealthReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthReport
        fields = '__all__'
