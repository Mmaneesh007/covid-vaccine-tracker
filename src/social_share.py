"""
Social Share Card Generator - Using Pre-designed Templates
Loads professional template images based on risk level.
"""
from PIL import Image
import io
import os

def generate_health_check_card(risk_level="LOW"):
    """
    Load and return the appropriate pre-designed share card.
    
    Args:
        risk_level: "LOW", "MODERATE", or "HIGH"
    
    Returns:
        bytes: PNG/JPG image data
    """
    # Map risk levels to image files
    image_map = {
        'LOW': 'low_risk.png',
        'MODERATE': 'moderate_risk.jpg',
        'HIGH': 'high_risk.png'
    }
    
    # Get the appropriate image filename
    filename = image_map.get(risk_level, 'low_risk.png')
    
    # Construct path to image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    image_path = os.path.join(project_root, 'assets', 'share_cards', filename)
    
    # Load and return image
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if needed (for consistency)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG', quality=95)
            img_bytes.seek(0)
            return img_bytes.getvalue()
    except FileNotFoundError:
        # Fallback: create a simple error image
        img = Image.new('RGB', (1080, 1080), (200, 200, 200))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()


def generate_vaccine_warrior_card():
    """Generate vaccine warrior card (uses low risk template for now)"""
    return generate_health_check_card("LOW")
