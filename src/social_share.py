"""
Premium Social Share Card Generator
Creates Instagram-worthy shareable images with curved layouts and decorative elements.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
from datetime import datetime
import math

def create_gradient_with_curves(width, height, color_top, color_bottom):
    """Create background with gradient and curved decorative elements"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Smooth gradient
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Add decorative dots pattern
    import random
    random.seed(42)  # Consistent pattern
    for _ in range(80):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(3, 10)
        opacity_color = (255, 255, 255)
        draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], 
                    fill=opacity_color)
    
    return img

def draw_rounded_rectangle(draw, xy, radius, fill):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)

def generate_premium_health_card(risk_level="LOW"):
    """Generate premium Instagram-style health status card"""
    width, height = 1080, 1080
    
    # Color schemes
    risk_colors = {
        'LOW': {
            'bg_top': (16, 185, 129),
            'bg_bottom': (5, 150, 105),
            'accent': (16, 185, 129),
            'badge_bg': (209, 250, 229),
            'badge_text': (4, 120, 87),
            'status_emoji': '✅',
            'status_text': 'LOW RISK\nSTAYING SAFE',
            'badge': 'HEALTH CONSCIOUS'
        },
        'MODERATE': {
            'bg_top': (59, 130, 246),
            'bg_bottom': (37, 99, 235),
            'accent': (59, 130, 246),
            'badge_bg': (219, 234, 254),
            'badge_text': (30, 64, 175),
            'status_emoji': '🔵',
            'status_text': 'MODERATE RISK\nSTAY CAUTIOUS',
            'badge': 'MONITOR SYMPTOMS'
        },
        'HIGH': {
            'bg_top': (251, 146, 60),
            'bg_bottom': (234, 88, 12),
            'accent': (251, 146, 60),
            'badge_bg': (254, 243, 199),
            'badge_text': (180, 83, 9),
            'status_emoji': '⚠️',
            'status_text': 'HIGH RISK\nACTION NEEDED',
            'badge': 'CONSULT DOCTOR'
        }
    }
    
    colors = risk_colors.get(risk_level, risk_colors['LOW'])
    
    # Create background with gradient and dots
    img = create_gradient_with_curves(width, height, colors['bg_top'], colors['bg_bottom'])
    
    # Create main white card with curves
    card_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    
    # Card dimensions with diagonal curve
    card_left = 100
    card_right = width - 100
    card_top = 250
    card_bottom = height - 150
    
    # Draw white card with rounded corners
    draw_rounded_rectangle(card_draw, 
                          (card_left, card_top, card_right, card_bottom),
                          radius=30,
                          fill=(255, 255, 255, 255))
    
    # Blur for shadow effect
    shadow = card_layer.filter(ImageFilter.GaussianBlur(15))
    img.paste(shadow, (0, 0), shadow)
    img.paste(card_layer, (0, 0), card_layer)
    
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 32)
        hero_font = ImageFont.truetype("arialbd.ttf", 80)
        subtitle_font = ImageFont.truetype("arialbd.ttf", 50)
        badge_font = ImageFont.truetype("arialbd.ttf", 36)
        body_font = ImageFont.truetype("arial.ttf", 28)
        cta_font = ImageFont.truetype("arialbd.ttf", 38)
    except:
        title_font = hero_font = subtitle_font = badge_font = body_font = cta_font = ImageFont.load_default()
    
    # Top branding (on gradient background)
    brand_text = "COVID-19 VACCINE TRACKER"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = brand_bbox[2] - brand_bbox[0]
    draw.text(((width - brand_width) / 2, 150), brand_text, 
             fill=(255, 255, 255), font=title_font)
    
    # Status emoji and text (on white card)
    emoji_y = card_top + 80
    emoji_text = colors['status_emoji']
    emoji_bbox = draw.textbbox((0, 0), emoji_text, font=hero_font)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    draw.text(((width - emoji_width) / 2, emoji_y), emoji_text, font=hero_font)
    
    # Status text
    status_lines = colors['status_text'].split('\n')
    status_y = emoji_y + 110
    for i, line in enumerate(status_lines):
        line_bbox = draw.textbbox((0, 0), line, font=subtitle_font)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text(((width - line_width) / 2, status_y + (i * 65)), 
                 line, fill=(31, 41, 55), font=subtitle_font)
    
    # Badge
    badge_y = status_y + (len(status_lines) * 65) + 50
    badge_text = colors['badge']
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_height = 60
    badge_padding = 40
    
    badge_rect_width = badge_width + (badge_padding * 2)
    badge_x = (width - badge_rect_width) / 2
    
    draw_rounded_rectangle(draw,
                          (badge_x, badge_y, badge_x + badge_rect_width, badge_y + badge_height),
                          radius=30,
                          fill=colors['badge_bg'])
    
    draw.text(((width - badge_width) / 2, badge_y + 12), 
             badge_text, fill=colors['badge_text'], font=badge_font)
    
    # Date
    date_text = f"Health Check: {datetime.now().strftime('%B %d, %Y')}"
    date_y = badge_y + 100
    date_bbox = draw.textbbox((0, 0), date_text, font=body_font)
    date_width = date_bbox[2] - date_bbox[0]
    draw.text(((width - date_width) / 2, date_y), 
             date_text, fill=(107, 114, 128), font=body_font)
    
    # Divider line
    divider_y = card_bottom - 120
    draw.line([(200, divider_y), (width - 200, divider_y)], 
             fill=(229, 231, 235), width=2)
    
    # CTA
    cta_text = "Check Yours Now  →"
    cta_y = divider_y + 25
    cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    draw.text(((width - cta_width) / 2, cta_y), 
             cta_text, fill=colors['accent'], font=cta_font)
    
    # URL
    url_text = "covid-vaccine-tracker.streamlit.app"
    url_y = cta_y + 55
    url_bbox = draw.textbbox((0, 0), url_text, font=body_font)
    url_width = url_bbox[2] - url_bbox[0]
    draw.text(((width - url_width) / 2, url_y), 
             url_text, fill=(156, 163, 175), font=body_font)
    
    # Decorative circle (bottom right)
    circle_radius = 150
    circle_x = width - 180
    circle_y = height - 180
    draw.ellipse([(circle_x - circle_radius, circle_y - circle_radius),
                  (circle_x + circle_radius, circle_y + circle_radius)],
                outline=(255, 255, 255), width=8)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG', quality=95)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def generate_health_check_card(risk_level="LOW"):
    """Generate premium health check card"""
    return generate_premium_health_card(risk_level)

def generate_vaccine_warrior_card():
    """Generate premium vaccine warrior card"""
    # For now, use the same base with different text
    return generate_premium_health_card("LOW")
