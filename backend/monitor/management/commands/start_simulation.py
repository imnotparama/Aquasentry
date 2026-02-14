import time
import random
from django.core.management.base import BaseCommand
from monitor.models import WaterSensor

class Command(BaseCommand):
    help = 'Simulates real-time IoT sensor data stream'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting IoT Sensor Simulation... Press Ctrl+C to stop.'))
        
        sensor_ids = ['SENSOR-001', 'SENSOR-002', 'SENSOR-003']
        
        try:
            while True:
                for sensor_id in sensor_ids:
                    # Generate random realistic values
                    ph = round(random.uniform(6.5, 8.5), 2)
                    turbidity = round(random.uniform(0.5, 5.0), 2)
                    temp = round(random.uniform(20.0, 30.0), 1)
                    do = round(random.uniform(6.0, 9.0), 2)
                    cond = round(random.uniform(300, 600), 0)
                    
                    WaterSensor.objects.create(
                        sensor_id=sensor_id,
                        ph=ph,
                        turbidity=turbidity,
                        temperature=temp,
                        dissolved_oxygen=do,
                        conductivity=cond
                    )
                    
                    self.stdout.write(f"Data packet sent from {sensor_id}: pH={ph}, Turbidity={turbidity}")
                
                # Keep database size manageable (optional cleanup)
                if WaterSensor.objects.count() > 1000:
                    oldest_ids = WaterSensor.objects.order_by('timestamp').values_list('id', flat=True)[:100]
                    WaterSensor.objects.filter(id__in=oldest_ids).delete()
                    
                time.sleep(5) # Update every 5 seconds
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Simulation stopped.'))
