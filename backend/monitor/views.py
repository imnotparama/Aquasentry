from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SatelliteImage, WaterSensor, HealthReport
from .serializers import SatelliteImageSerializer, WaterSensorSerializer, HealthReportSerializer
from .utils import analyze_water_image
from .sentinel_service import SentinelService
import os

class SatelliteImageViewSet(viewsets.ModelViewSet):
    queryset = SatelliteImage.objects.all().order_by('-captured_at')
    serializer_class = SatelliteImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'])
    def fetch_live(self, request):
        location_name = request.data.get('location_name', 'Unknown Region')
        # Expecting bbox as a list of floats: [min_lon, min_lat, max_lon, max_lat]
        # For simplicity, we can also accept a center lat/lon and create a bbox
        lat = float(request.data.get('lat', 0))
        lon = float(request.data.get('lon', 0))
        
        if lat and lon:
            # Create a small bbox around the point (~5km)
            delta = 0.05
            bbox = [lon - delta, lat - delta, lon + delta, lat + delta]
            
            instance = SentinelService.fetch_satellite_image(bbox, location_name)
            
            if instance:
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to fetch from Sentinel Hub (Check API Keys)"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response({"error": "Latitude and Longitude required"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        # Intercept creation to perform OpenCV analysis
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            instance = file_serializer.save()
            
            # Perform Analysis
            image_path = instance.image.path
            analysis_results = analyze_water_image(image_path)
            
            # Update instance with results
            instance.chlorophyll_index = analysis_results['chlorophyll_index']
            instance.turbidity_index = analysis_results['turbidity_index']
            instance.risk_score = analysis_results['risk_score']
            instance.save()
            
            # Return updated data
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WaterSensorViewSet(viewsets.ModelViewSet):
    queryset = WaterSensor.objects.all().order_by('-timestamp')
    serializer_class = WaterSensorSerializer

from .email_service import send_alert_email

class HealthReportViewSet(viewsets.ModelViewSet):
    queryset = HealthReport.objects.all().order_by('-submitted_at')
    serializer_class = HealthReportSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # Trigger email alert if severity is high
        send_alert_email(instance)

from rest_framework.decorators import api_view
from django.db.models import Avg

@api_view(['GET'])
def dashboard_stats(request):
    """
    Aggregates data from all layers to provide a system overview.
    """
    # 1. Satellite Risk
    recent_sat = SatelliteImage.objects.order_by('-captured_at').first()
    sat_risk = recent_sat.risk_score if recent_sat else 0
    
    # 2. Sensor Risk (Check last 10 readings for any critical status)
    recent_sensors = WaterSensor.objects.order_by('-timestamp')[:10]
    sensor_issues = 0
    if recent_sensors:
        for s in recent_sensors:
            if s.ph < 6.5 or s.ph > 8.5 or s.turbidity > 5.0:
                sensor_issues += 1
    
    # 3. Health Risk (Check reports from last 24h - simplified to last 10 for demo)
    recent_reports = HealthReport.objects.order_by('-submitted_at')[:10]
    health_issues = 0
    if recent_reports:
        for h in recent_reports:
            if h.severity > 5:
                health_issues += 1

    # Determine Overall Status
    overall_status = "LOW"
    status_color = "text-green-400"
    status_message = "Systems Nominal"

    if sat_risk > 70 or sensor_issues > 2 or health_issues > 2:
        overall_status = "CRITICAL"
        status_color = "text-red-500"
        status_message = "Immediate Action Required"
    elif sat_risk > 40 or sensor_issues > 0 or health_issues > 0:
        overall_status = "MODERATE"
        status_color = "text-yellow-400"
        status_message = "Elevated Risk Detected"

    return Response({
        "overallRisk": overall_status,
        "statusMessage": status_message,
        "statusColor": status_color,
        "satelliteAlerts": 1 if sat_risk > 50 else 0,
        "sensorAnomalies": sensor_issues,
        "healthReports": HealthReport.objects.count()
    })
