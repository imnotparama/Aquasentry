import requests
import os
from django.conf import settings
from .models import SatelliteImage
from .utils import analyze_water_image
from django.core.files.base import ContentFile
import time

class SentinelService:
    # ------------------------------------------------------------------
    # TODO: REPLACE THESE PLACEHOLDERS WITH YOUR ACTUAL SENTINEL HUB KEYS
    # Register at: https://www.sentinel-hub.com/
    # ------------------------------------------------------------------
    CLIENT_ID = os.environ.get('SENTINEL_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')
    CLIENT_SECRET = os.environ.get('SENTINEL_CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')
    
    TOKEN_URL = "https://services.sentinel-hub.com/oauth/token"
    PROCESS_URL = "https://services.sentinel-hub.com/api/v1/process"

    @classmethod
    def get_token(cls):
        if cls.CLIENT_ID == 'YOUR_CLIENT_ID_HERE':
            print("WARNING: Sentinel Hub Client ID not set. Using mock data path.")
            return None
            
        data = {
            "grant_type": "client_credentials",
            "client_id": cls.CLIENT_ID,
            "client_secret": cls.CLIENT_SECRET
        }
        try:
            response = requests.post(cls.TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()['access_token']
        except Exception as e:
            print(f"Failed to get Sentinel token: {e}")
            return None

    @classmethod
    def fetch_satellite_image(cls, bbox, location_name="Target Area"):
        """
        Fetches an image from Sentinel-2 for the given Bounding Box (bbox).
        bbox format: [min_lon, min_lat, max_lon, max_lat]
        """
        token = cls.get_token()
        
        # MOCK FALLBACK if no token (so the app doesn't crash during demo)
        if not token:
            print("Simulating Sentinel Fetch...")
            # Generate a synthetic image (Simulating a water body)
            import numpy as np
            from PIL import Image
            import io
            
            # Create a random noise image with some "water blue" and "algae green"
            width, height = 512, 512
            # Base blue water
            data = np.zeros((height, width, 3), dtype=np.uint8)
            data[:, :] = [0, 100, 200] # Blue (RGB somewhat)
            
            # Add some "Algae" (Green) blobs
            for _ in range(10):
                cx, cy = np.random.randint(0, width), np.random.randint(0, height)
                radius = np.random.randint(20, 100)
                y, x = np.ogrid[-cy:height-cy, -cx:width-cx]
                mask = x*x + y*y <= radius*radius
                data[mask] = [34, 139, 34] # Forest Green

            # Add some "Turbidity" (Brown) blobs
            for _ in range(5):
                cx, cy = np.random.randint(0, width), np.random.randint(0, height)
                radius = np.random.randint(20, 80)
                y, x = np.ogrid[-cy:height-cy, -cx:width-cx]
                mask = x*x + y*y <= radius*radius
                data[mask] = [139, 69, 19] # Saddle Brown

            img = Image.fromarray(data, 'RGB')
            
            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            
            # Save to Django Model
            file_name = f"simulated_sentinel_{location_name.replace(' ', '_')}_{int(time.time())}.png"
            image_content = ContentFile(buffer.getvalue(), name=file_name)
            
            instance = SatelliteImage(location_name=f"[SIM] {location_name}")
            instance.image.save(file_name, image_content)
            instance.save()
            
            # Run analysis
            analysis = analyze_water_image(instance.image.path)
            instance.chlorophyll_index = analysis['chlorophyll_index']
            instance.turbidity_index = analysis['turbidity_index']
            instance.risk_score = analysis['risk_score']
            instance.save()
            
            return instance

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "image/png"
        }

        # Evalscript to get True Color (RGB)
        evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: ["B04", "B03", "B02"],
            output: { bands: 3 }
          };
        }

        function evaluatePixel(sample) {
          return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
        }
        """

        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox,
                    "properties": { "crs": "http://www.opengis.net/def/crs/EPSG/0/4326" }
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": "2024-01-01T00:00:00Z",
                            "to": "2024-02-14T23:59:59Z"  # Adjust dynamically in production
                        },
                        "mosaickingOrder": "leastCC" # Least cloud cover
                    }
                }]
            },
            "output": {
                "width": 512,
                "height": 512,
                "responses": [{ "identifier": "default", "format": { "type": "image/png" } }]
            },
            "evalscript": evalscript
        }

        try:
            response = requests.post(cls.PROCESS_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            # Save the image to Django Model
            file_name = f"sentinel_{location_name.replace(' ', '_')}.png"
            image_content = ContentFile(response.content, name=file_name)
            
            instance = SatelliteImage(location_name=location_name)
            instance.image.save(file_name, image_content)
            instance.save()
            
            # Run our OpenCV analysis on this new image
            analysis = analyze_water_image(instance.image.path)
            instance.chlorophyll_index = analysis['chlorophyll_index']
            instance.turbidity_index = analysis['turbidity_index']
            instance.risk_score = analysis['risk_score']
            instance.save()
            
            return instance

        except Exception as e:
            print(f"Error fetching from Sentinel: {e}")
            return None
