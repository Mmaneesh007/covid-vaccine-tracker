"""
Social Share Card Generator
Creates beautiful shareable images for social media platforms.
"""
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

def generate_share_card(
    title="Vaccine Tracker",
    subtitle="COVID-19 Safety",
    status_text="I'm staying safe!",
    color_theme="green"
):
    """
    Generate a social media share card image.
    
    Args:
        title: Main title text
        subtitle: Subtitle text
        status_text: The main status message
        color_theme: Color theme ('green', 'blue', 'orange')
    
    Returns:
        bytes: PNG image data
    """
    # Image dimensions (optimized for Instagram/WhatsApp)
    width, height = 1080, 1080
    
    # Color themes
    themes = {
        'green': {
            'bg_start': (102, 126, 234),  # #667eea
            'bg_end': (118, 75, 162),     # #764ba2
            'text': (255, 255, 255),
            'emoji': '✅'
        },
        'blue': {
            'bg_start': (66, 165, 245),
            'bg_end': (25, 118, 210),
            'text': (255, 255, 255),
            'emoji': '💙'
        },
        'orange': {
            'bg_start': (255, 167, 38),
            'bg_end': (251, 140, 0),
            'text': (255, 255, 255),
            'emoji': '🔥'
        }
    }
    
    theme = themes.get(color_theme, themes['green'])
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), theme['bg_start'])
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    for y in range(height):
        ratio = y / height
        r = int(theme['bg_start'][0] * (1 - ratio) + theme['bg_end'][0] * ratio)
        g = int(theme['bg_start'][1] * (1 - ratio) + theme['bg_end'][1] * ratio)
        b = int(theme['bg_start'][2] * (1 - ratio) + theme['bg_end'][2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Try to load custom font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 80)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
        status_font = ImageFont.truetype("arialbd.ttf", 90)
        credit_font = ImageFont.truetype("arial.ttf", 30)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        status_font = ImageFont.load_default()
        credit_font = ImageFont.load_default()
    
    # Draw title (top)
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        ((width - title_width) / 2, 150),
        title,
        fill=theme['text'],
        font=title_font
    )
    
    # Draw subtitle
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(
        ((width - subtitle_width) / 2, 260),
        subtitle,
        fill=theme['text'],
        font=subtitle_font
    )
    
    # Draw emoji (large)
    emoji_text = theme['emoji']
    emoji_bbox = draw.textbbox((0, 0), emoji_text, font=status_font)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    draw.text(
        ((width - emoji_width) / 2, 400),
        emoji_text,
        font=status_font
    )
    
    # Draw status text (center)
    status_bbox = draw.textbbox((0, 0), status_text, font=status_font)
    status_width = status_bbox[2] - status_bbox[0]
    draw.text(
        ((width - status_width) / 2, 550),
        status_text,
        fill=theme['text'],
        font=status_font
    )
    
    # Draw website credit (bottom)
    credit_text = "Track yours at:"
    website_text = "COVID-19 Vaccine Tracker"
    
    credit_bbox = draw.textbbox((0, 0), credit_text, font=credit_font)
    credit_width = credit_bbox[2] - credit_bbox[0]
    draw.text(
        ((width - credit_width) / 2, 850),
        credit_text,
        fill=theme['text'],
        font=credit_font
    )
    
    website_bbox = draw.textbbox((0, 0), website_text, font=subtitle_font)
    website_width = website_bbox[2] - website_bbox[0]
    draw.text(
        ((width - website_width) / 2, 900),
        website_text,
        fill=theme['text'],
        font=subtitle_font
    )
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()


def generate_vaccine_warrior_card():
    """Generate a 'Vaccine Warrior' share card"""
    return generate_share_card(
        title="COVID-19 Vaccine Tracker",
        subtitle="Vaccine Warrior 💪",
        status_text="I'm Getting Vaccinated!",
        color_theme="green"
    )


def generate_health_check_card(risk_level="LOW"):
    """Generate a health check status card"""
    themes = {
        'HIGH': ('orange', '⚠️ High Risk'),
        'MODERATE': ('blue', '🔵 Moderate Risk'),
        'LOW': ('green', '✅ Low Risk')
    }
    
    theme, emoji_status = themes.get(risk_level, themes['LOW'])
    
    return generate_share_card(
        title="COVID-19 Vaccine Tracker",
        subtitle="Health Assessment",
        status_text=f"Status: {emoji_status}",
        color_theme=theme
    )
