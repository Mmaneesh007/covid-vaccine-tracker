"""
Premium Social Share Card Generator - Diagonal Design
Creates viral Instagram-style cards with tilted layouts and curved elements.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
from datetime import datetime
import math

def generate_premium_diagonal_card(risk_level="LOW"):
    """Generate Instagram-worthy diagonal card design"""
    width, height = 1080, 1080
    
    # Risk-specific config
    configs = {
        'LOW': {
            'bg_top': (16, 185, 129),
            'bg_bottom': (5, 150, 105),
            'accent': (5, 150, 105),
            'emoji': '✅',
            'status': 'LOW RISK',
            'subtitle': 'STAYING SAFE',
            'badge': 'HEALTH CONSCIOUS'
        },
        'MODERATE': {
            'bg_top': (59, 130, 246),
            'bg_bottom': (37, 99, 235),
            'accent': (37, 99, 235),
            'emoji': '🔵',
            'status': 'MODERATE RISK',
            'subtitle': 'STAY CAUTIOUS',
            'badge': 'MONITOR SYMPTOMS'
        },
        'HIGH': {
            'bg_top': (251, 146, 60),
            'bg_bottom': (234, 88, 12),
            'accent': (234, 88, 12),
            'emoji': '⚠️',
            'status': 'HIGH RISK',
            'subtitle': 'ACTION NEEDED',
            'badge': 'CONSULT DOCTOR'
        }
    }
    
    config = configs.get(risk_level, configs['LOW'])
    
    # Create gradient background
    bg = Image.new('RGB', (width, height))
    draw_bg = ImageDraw.Draw(bg)
    
    for y in range(height):
        ratio = y / height
        r = int(config['bg_top'][0] * (1 - ratio) + config['bg_bottom'][0] * ratio)
        g = int(config['bg_top'][1] * (1 - ratio) + config['bg_bottom'][1] * ratio)
        b = int(config['bg_top'][2] * (1 - ratio) + config['bg_bottom'][2] * ratio)
        draw_bg.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Add decorative dots
    import random
    random.seed(42)
    for _ in range(60):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.choice([3, 4, 5, 6, 8, 10, 12])
        draw_bg.ellipse([(x-radius, y-radius), (x+radius, y+radius)], 
                       fill=(255, 255, 255))
    
    # Brand text (top left)
    try:
        brand_font = ImageFont.truetype("arialbd.ttf", 24)
        status_font = ImageFont.truetype("arialbd.ttf", 110)
        subtitle_font = ImageFont.truetype("arialbd.ttf", 38)
        badge_font = ImageFont.truetype("arialbd.ttf", 26)
        body_font = ImageFont.truetype("arial.ttf", 24)
        cta_font = ImageFont.truetype("arialbd.ttf", 34)
    except:
        brand_font = status_font = subtitle_font = badge_font = body_font = cta_font = ImageFont.load_default()
    
    draw_bg.text((40, 40), "COVID-19 VACCINE TRACKER", 
                fill=(255, 255, 255), font=brand_font)
    
    # Create white card (larger canvas for rotation)
    card_size = 1200
    card = Image.new('RGBA', (card_size, card_size), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    
    # Draw rounded white rectangle
    card_width, card_height = 750, 550
    card_x = (card_size - card_width) // 2
    card_y = (card_size - card_height) // 2
    
    # Rounded rectangle
    radius = 25
    card_draw.rounded_rectangle(
        [(card_x, card_y), (card_x + card_width, card_y + card_height)],
        radius=radius,
        fill=(255, 255, 255, 255)
    )
    
    # Add content ON the white card
    content_x = card_x + 60
    content_y = card_y + 70
    
    # Status with emoji
    status_text = f"{config['emoji']} {config['status']}"
    card_draw.text((content_x, content_y), status_text,
                  fill=(31, 41, 55), font=status_font)
    
    # Subtitle
    card_draw.text((content_x, content_y + 130), config['subtitle'],
                  fill=(75, 85, 99), font=subtitle_font)
    
    # Badge pill
    badge_y = content_y + 200
    badge_text = config['badge']
    badge_bbox = card_draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_padding = 20
    
    card_draw.rounded_rectangle(
        [(content_x, badge_y), 
         (content_x + badge_width + badge_padding * 2, badge_y + 40)],
        radius=20,
        fill=config['accent']
    )
    card_draw.text((content_x + badge_padding, badge_y + 8), badge_text,
                  fill=(255, 255, 255), font=badge_font)
    
    # Date
    date_text = f"Health Check: {datetime.now().strftime('%B %d, %Y')}"
    card_draw.text((content_x, badge_y + 70), date_text,
                  fill=(156, 163, 175), font=body_font)
    
    # Divider
    divider_y = card_y + card_height - 120
    card_draw.line([(card_x + 40, divider_y), (card_x + card_width - 40, divider_y)],
                  fill=(229, 231, 235), width=2)
    
    # CTA
    cta_text = "Check Yours Now →"
    card_draw.text((content_x, divider_y + 15), cta_text,
                  fill=config['accent'], font=cta_font)
    
    # URL
    url_text = "covid-vaccine-tracker.streamlit.app"
    card_draw.text((content_x, divider_y + 60), url_text,
                  fill=(156, 163, 175), font=body_font)
    
    # Rotate card
    rotated_card = card.rotate(8, expand=True, resample=Image.BICUBIC)
    
    # Create shadow
    shadow = rotated_card.filter(ImageFilter.GaussianBlur(20))
    
    # Paste onto background
    card_pos_x = -60  # Offset left
    card_pos_y = 180  # Offset down
    
    bg.paste(shadow, (card_pos_x + 10, card_pos_y + 10), shadow)
    bg.paste(rotated_card, (card_pos_x, card_pos_y), rotated_card)
    
    # Draw thick curved arc (bottom right)
    draw_final = ImageDraw.Draw(bg)
    
    # Large circular arc
    circle_center_x = width + 100
    circle_center_y = height - 100
    circle_radius = 280
    
    draw_final.arc(
        [(circle_center_x - circle_radius, circle_center_y - circle_radius),
         (circle_center_x + circle_radius, circle_center_y + circle_radius)],
        start=140, end=250,
        fill=(255, 255, 255), width=15
    )
    
    # Inner concentric arc for style
    inner_radius = 240
    draw_final.arc(
        [(circle_center_x - inner_radius, circle_center_y - inner_radius),
         (circle_center_x + inner_radius, circle_center_y + inner_radius)],
        start=140, end=250,
        fill=(200, 200, 200), width=3
    )
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    bg.save(img_bytes, format='PNG', quality=95)
    img_bytes.seek(0)
    return img_bytes.getvalue()


def generate_health_check_card(risk_level="LOW"):
    """Generate premium diagonal health check card"""
    return generate_premium_diagonal_card(risk_level)


def generate_vaccine_warrior_card():
    """Generate vaccine warrior card"""
    return generate_premium_diagonal_card("LOW")
