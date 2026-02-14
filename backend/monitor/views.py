from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SatelliteImage, WaterSensor, HealthReport
from .serializers import SatelliteImageSerializer, WaterSensorSerializer, HealthReportSerializer
from .utils import analyze_water_image
import os

class SatelliteImageViewSet(viewsets.ModelViewSet):
    queryset = SatelliteImage.objects.all().order_by('-captured_at')
    serializer_class = SatelliteImageSerializer
    parser_classes = (MultiPartParser, FormParser)

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

class HealthReportViewSet(viewsets.ModelViewSet):
    queryset = HealthReport.objects.all().order_by('-submitted_at')
    serializer_class = HealthReportSerializer
