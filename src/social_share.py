"""
Social Share Card Generator - Premium Edition
Creates viral-worthy shareable images for social media platforms.
"""
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

def generate_premium_share_card(
    main_status="✅ STAYING SAFE",
    badge_text="HEALTH CONSCIOUS",
    stats_line="Checked: Dec 3, 2025",
    url_text="Track Yours →",
    color_scheme="green"
):
    """
    Generate a premium Instagram-style share card.
    
    Args:
        main_status: Large bold status text
        badge_text: Achievement badge text
        stats_line: Date or stats info
        url_text: Call to action
        color_scheme: Color theme ('green', 'blue', 'orange')
    
    Returns:
        bytes: PNG image data
    """
    # Image dimensions (Instagram square)
    width, height = 1080, 1080
    
    # Color schemes with modern palettes
    schemes = {
        'green': {
            'bg_top': (16, 185, 129),      # Emerald
            'bg_bottom': (5, 150, 105),    # Darker emerald
            'card_bg': (255, 255, 255),
            'accent': (16, 185, 129),
            'text_dark': (17, 24, 39),
            'text_light': (107, 114, 128),
            'badge_bg': (209, 250, 229),
            'badge_text': (4, 120, 87)
        },
        'orange': {
            'bg_top': (251, 146, 60),
            'bg_bottom': (234, 88, 12),
            'card_bg': (255, 255, 255),
            'accent': (251, 146, 60),
            'text_dark': (17, 24, 39),
            'text_light': (107, 114, 128),
            'badge_bg': (254, 243, 199),
            'badge_text': (180, 83, 9)
        },
        'blue': {
            'bg_top': (59, 130, 246),
            'bg_bottom': (37, 99, 235),
            'card_bg': (255, 255, 255),
            'accent': (59, 130, 246),
            'text_dark': (17, 24, 39),
            'text_light': (107, 114, 128),
            'badge_bg': (219, 234, 254),
            'badge_text': (30, 64, 175)
        }
    }
    
    colors = schemes.get(color_scheme, schemes['green'])
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Draw smooth gradient
    for y in range(height):
        ratio = y / height
        r = int(colors['bg_top'][0] * (1 - ratio) + colors['bg_bottom'][0] * ratio)
        g = int(colors['bg_top'][1] * (1 - ratio) + colors['bg_bottom'][1] * ratio)
        b = int(colors['bg_top'][2] * (1 - ratio) + colors['bg_bottom'][2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Draw white card with shadow effect
    card_margin = 80
    card_top = 200
    card_bottom = height - 200
    
    # Shadow layers (multiple for depth)
    for i in range(5):
        offset = 5 - i
        shadow_alpha = 20 + (i * 10)
        shadow_color = (0, 0, 0, shadow_alpha)
        # Note: We can't do alpha in RGB mode, so we'll just use gray
        shadow_gray = 200 - (i * 15)
        draw.rectangle(
            [(card_margin + offset, card_top + offset), 
             (width - card_margin + offset, card_bottom + offset)],
            fill=(shadow_gray, shadow_gray, shadow_gray)
        )
    
    # Main white card
    draw.rectangle(
        [(card_margin, card_top), (width - card_margin, card_bottom)],
        fill=colors['card_bg']
    )
    
    # Load fonts with better sizing
    try:
        logo_font = ImageFont.truetype("arialbd.ttf", 36)
        status_font = ImageFont.truetype("arialbd.ttf", 76)
        badge_font = ImageFont.truetype("arialbd.ttf", 40)
        stats_font = ImageFont.truetype("arial.ttf", 32)
        url_font = ImageFont.truetype("arialbd.ttf", 44)
    except:
        # Fallback
        logo_font = ImageFont.load_default()
        status_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
    
    # TOP: Logo/Brand
    logo_text = "COVID-19 VACCINE TRACKER"
    logo_bbox = draw.textbbox((0, 0), logo_text, font=logo_font)
    logo_width = logo_bbox[2] - logo_bbox[0]
    draw.text(
        ((width - logo_width) / 2, 100),
        logo_text,
        fill=(255, 255, 255),
        font=logo_font
    )
    
    # CENTER CARD: Main Status
    status_y = card_top + 120
    
    # Status text (multi-line support)
    status_lines = main_status.split('\n')
    for i, line in enumerate(status_lines):
        line_bbox = draw.textbbox((0, 0), line, font=status_font)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text(
            ((width - line_width) / 2, status_y + (i * 90)),
            line,
            fill=colors['text_dark'],
            font=status_font
        )
    
    # Achievement Badge (rounded rect)
    badge_y = status_y + (len(status_lines) * 90) + 60
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_padding = 30
    badge_rect_width = badge_width + (badge_padding * 2)
    badge_rect_height = 70
    badge_x = (width - badge_rect_width) / 2
    
    # Draw rounded rectangle for badge
    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_rect_width, badge_y + badge_rect_height)],
        radius=35,
        fill=colors['badge_bg']
    )
    
    # Badge text
    draw.text(
        ((width - badge_width) / 2, badge_y + 15),
        badge_text,
        fill=colors['badge_text'],
        font=badge_font
    )
    
    # Stats line
    stats_y = badge_y + 130
    stats_bbox = draw.textbbox((0, 0), stats_line, font=stats_font)
    stats_width = stats_bbox[2] - stats_bbox[0]
    draw.text(
        ((width - stats_width) / 2, stats_y),
        stats_line,
        fill=colors['text_light'],
        font=stats_font
    )
    
    # Divider line
    divider_y = card_bottom - 140
    divider_margin = 150
    draw.rectangle(
        [(divider_margin, divider_y), (width - divider_margin, divider_y + 2)],
        fill=colors['text_light']
    )
    
    # Bottom: CTA
    cta_y = divider_y + 30
    url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    draw.text(
        ((width - url_width) / 2, cta_y),
        url_text,
        fill=colors['accent'],
        font=url_font
    )
    
    # Website URL (smaller)
    website_y = cta_y + 60
    website_text = "covid-vaccine-tracker.streamlit.app"
    website_bbox = draw.textbbox((0, 0), website_text, font=stats_font)
    website_width = website_bbox[2] - website_bbox[0]
    draw.text(
        ((width - website_width) / 2, website_y),
        website_text,
        fill=colors['text_light'],
        font=stats_font
    )
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()


def generate_health_check_card(risk_level="LOW"):
    """Generate a premium health check status card"""
    today = datetime.now().strftime("%B %d, %Y")
    
    risk_configs = {
        'HIGH': {
            'status': "⚠️ HIGH RISK\nSTAY ALERT",
            'badge': "ACTION REQUIRED",
            'color': 'orange'
        },
        'MODERATE': {
            'status': "🔵 MODERATE RISK\nSTAY CAUTIOUS",
            'badge': "MONITOR SYMPTOMS",
            'color': 'blue'
        },
        'LOW': {
            'status': "✅ LOW RISK\nSTAYING SAFE",
            'badge': "HEALTH CONSCIOUS",
            'color': 'green'
        }
    }
    
    config = risk_configs.get(risk_level, risk_configs['LOW'])
    
    return generate_premium_share_card(
        main_status=config['status'],
        badge_text=config['badge'],
        stats_line=f"Health Check: {today}",
        url_text="Check Yours Now  →",
        color_scheme=config['color']
    )


def generate_vaccine_warrior_card():
    """Generate a 'Vaccine Warrior' share card"""
    today = datetime.now().strftime("%B %d, %Y")
    
    return generate_premium_share_card(
        main_status="💪 VACCINE\nWARRIOR",
        badge_text="GETTING VACCINATED",
        stats_line=f"Reminder Set: {today}",
        url_text="Join the Movement  →",
        color_scheme="green"
    )
