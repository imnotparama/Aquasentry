from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SatelliteImageViewSet, WaterSensorViewSet, HealthReportViewSet, dashboard_stats

router = DefaultRouter()
router.register(r'satellite', SatelliteImageViewSet)
router.register(r'sensors', WaterSensorViewSet)
router.register(r'health-reports', HealthReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard-stats/', dashboard_stats, name='dashboard-stats'),
]
