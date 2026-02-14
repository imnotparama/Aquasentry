import cv2
import numpy as np

def analyze_water_image(image_path):
    """
    Analyzes an image for chlorophyll (green) and turbidity (brown/yellow) content.
    Returns:
        dict: {
            'chlorophyll_index': float (0-100),
            'turbidity_index': float (0-100),
            'risk_score': float (0-100)
        }
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {'chlorophyll_index': 0, 'turbidity_index': 0, 'risk_score': 0}
        
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        total_pixels = img.shape[0] * img.shape[1]

        # 1. Chlorophyll (Green Algae) Detection
        # Green hue range in HSV: approx 35-85
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_pixels = cv2.countNonZero(green_mask)
        chlorophyll_index = (green_pixels / total_pixels) * 100

        # 2. Turbidity (Brown/Muddy) Detection
        # Brown/Yellow hue range: approx 10-30
        lower_brown = np.array([10, 40, 40])
        upper_brown = np.array([30, 255, 255])
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
        brown_pixels = cv2.countNonZero(brown_mask)
        turbidity_index = (brown_pixels / total_pixels) * 100

        # 3. Calculate Risk Score
        # Weighted sum: Turbidity is often more critical for pathogens, but Algae is toxic.
        # Let's say: 60% Turbidity + 40% Chlorophyll
        base_risk = (turbidity_index * 1.5) + (chlorophyll_index * 1.2)
        risk_score = min(max(base_risk, 0), 100) # Clamp between 0-100

        return {
            'chlorophyll_index': round(chlorophyll_index, 2),
            'turbidity_index': round(turbidity_index, 2),
            'risk_score': round(risk_score, 2)
        }

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {'chlorophyll_index': 0, 'turbidity_index': 0, 'risk_score': 0}
