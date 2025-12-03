"""
Social Share Card Generator
Generates dynamic, personalized images for social sharing.
"""
from PIL import Image, ImageDraw, ImageFont
import io
import os
import platform

def get_font(size=40, bold=False):
    """
    Load a font that works on the current system.
    """
    system = platform.system()
    
    # Preferred fonts by OS
    font_names = []
    if system == "Windows":
        font_names = ["arialbd.ttf" if bold else "arial.ttf", "seguiemj.ttf"]
    elif system == "Darwin":  # macOS
        font_names = ["Helvetica-Bold.ttf" if bold else "Helvetica.ttf", "Arial.ttf"]
    else:  # Linux
        font_names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", "FreeSans.ttf"]
        
    # Try to load preferred fonts
    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue
            
    # Fallback to default
    return ImageFont.load_default()

def generate_health_check_card(risk_level="LOW"):
    """
    Load and return the appropriate pre-designed share card.
    """
    # Map risk levels to image files
    image_map = {
        'LOW': 'low_risk.png',
        'MODERATE': 'moderate_risk.jpg',
        'HIGH': 'high_risk.png'
    }
    
    filename = image_map.get(risk_level, 'low_risk.png')
    
    # Construct path to image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    image_path = os.path.join(project_root, 'assets', 'share_cards', filename)
    
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            return img_bytes.getvalue()
    except FileNotFoundError:
        return _create_fallback_image(f"Risk: {risk_level}")

def create_vaccination_certificate(name, date, dose="Fully Vaccinated"):
    """
    Generate a personalized vaccination certificate card.
    """
    # Create a clean, professional background
    width, height = 1080, 1080
    # Gradient background (simulated with solid color for now, or load template)
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Draw Header Background
    draw.rectangle([(0, 0), (width, 300)], fill='#667eea')
    
    # Fonts
    title_font = get_font(80, bold=True)
    subtitle_font = get_font(50)
    name_font = get_font(100, bold=True)
    detail_font = get_font(40)
    
    # Header Text
    draw.text((width/2, 100), "COVID-19", font=title_font, fill='white', anchor="mm")
    draw.text((width/2, 200), "Vaccination Status", font=subtitle_font, fill='white', anchor="mm")
    
    # Badge/Icon (Simple Circle for now)
    draw.ellipse([(width/2 - 80, 350), (width/2 + 80, 510)], fill='#e2e8f0')
    draw.text((width/2, 430), "💉", font=get_font(80), fill='black', anchor="mm")
    
    # User Name
    draw.text((width/2, 600), name, font=name_font, fill='#2d3748', anchor="mm")
    
    # Status
    draw.text((width/2, 720), dose, font=get_font(60, bold=True), fill='#38a169', anchor="mm")
    
    # Date
    draw.text((width/2, 820), f"Date: {date}", font=detail_font, fill='#718096', anchor="mm")
    
    # Footer
    draw.text((width/2, 950), "Verified by VaxTracker App", font=get_font(30), fill='#a0aec0', anchor="mm")
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

def create_country_status_card(country_name, vax_percentage, total_doses):
    """
    Generate a shareable card for country statistics.
    """
    width, height = 1080, 1080
    img = Image.new('RGB', (width, height), color='#1a202c')
    draw = ImageDraw.Draw(img)
    
    # Fonts
    title_font = get_font(90, bold=True)
    stat_font = get_font(180, bold=True)
    label_font = get_font(50)
    
    # Country Name
    draw.text((width/2, 150), country_name, font=title_font, fill='#667eea', anchor="mm")
    draw.text((width/2, 250), "Vaccination Progress", font=label_font, fill='white', anchor="mm")
    
    # Percentage
    draw.text((width/2, 450), f"{vax_percentage}%", font=stat_font, fill='#48bb78', anchor="mm")
    draw.text((width/2, 580), "Population Vaccinated", font=get_font(40), fill='#a0aec0', anchor="mm")
    
    # Total Doses
    draw.text((width/2, 750), total_doses, font=get_font(100, bold=True), fill='white', anchor="mm")
    draw.text((width/2, 850), "Total Doses Administered", font=get_font(40), fill='#a0aec0', anchor="mm")
    
    # Footer
    draw.text((width/2, 1000), "Tracked via VaxTracker", font=get_font(30), fill='#718096', anchor="mm")
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

def _create_fallback_image(text):
    img = Image.new('RGB', (800, 400), (200, 200, 200))
    draw = ImageDraw.Draw(img)
    draw.text((400, 200), text, fill='black', anchor="mm")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()
