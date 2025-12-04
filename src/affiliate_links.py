# src/affiliate_links.py
"""
Affiliate Marketing Module
Manages affiliate links and product recommendations for monetization.
"""

AFFILIATE_PRODUCTS = {
    "travel_insurance": [
        {
            "name": "SafetyWing Nomad Insurance",
            "description": "Comprehensive travel medical insurance for digital nomads and travelers. Covers COVID-19, trip interruption, and emergency medical expenses worldwide.",
            "benefits": [
                "✅ COVID-19 Coverage included",
                "✅ Monthly subscriptions from $45.08",
                "✅ Covers 180+ countries",
                "✅ No medical exam required"
            ],
            "affiliate_link": "https://safetywing.com/?referenceID=covidtracker&lan=en",  # Replace with actual affiliate link
            "cta": "Get a Quote",
            "icon": "🛡️"
        },
        {
            "name": "World Nomads Travel Insurance",
            "description": "Flexible travel insurance designed for adventurous travelers. Coverage for trip cancellation, medical emergencies, and lost luggage.",
            "benefits": [
                "✅ Trip cancellation protection",
                "✅ 24/7 emergency assistance",
                "✅ Adventure sports coverage",
                "✅ COVID-19 medical expenses"
            ],
            "affiliate_link": "https://www.worldnomads.com/",  # Replace with actual affiliate link
            "cta": "Learn More",
            "icon": "🌍"
        }
    ],
    
    "health_products": [
        {
            "name": "N95/KN95 Protective Masks",
            "description": "FDA-approved high-filtration masks for maximum protection during travel and crowded spaces.",
            "benefits": [
                "✅ 95%+ filtration efficiency",
                "✅ Comfortable fit for all-day wear",
                "✅ Multiple sizes available",
                "✅ Ideal for flights and public transport"
            ],
            "affiliate_link": "https://www.amazon.in/s?k=n95+mask&tag=covidvaccinetracker-21",  # Replace with your Amazon Associates tag
            "cta": "Shop on Amazon",
            "icon": "😷"
        },
        {
            "name": "Hand Sanitizer (Travel Size)",
            "description": "70%+ alcohol-based sanitizer in TSA-approved sizes. Perfect for on-the-go protection.",
            "benefits": [
                "✅ Kills 99.9% of germs",
                "✅ TSA-compliant sizes",
                "✅ Moisturizing formula",
                "✅ Portable and convenient"
            ],
            "affiliate_link": "https://www.amazon.in/s?k=hand+sanitizer+travel+size&tag=covidvaccinetracker-21",
            "cta": "Shop on Amazon",
            "icon": "🧴"
        },
        {
            "name": "Immune Support Vitamins",
            "description": "Vitamin C, D3, and Zinc supplements to boost your immune system naturally.",
            "benefits": [
                "✅ Supports immune function",
                "✅ Vitamin D3 + Vitamin C + Zinc",
                "✅ Trusted brands available",
                "✅ Essential for travelers"
            ],
            "affiliate_link": "https://www.amazon.in/s?k=vitamin+c+d+zinc&tag=covidvaccinetracker-21",
            "cta": "Shop on Amazon",
            "icon": "💊"
        },
        {
            "name": "Travel First Aid Kit",
            "description": "Complete medical kit with bandages, pain relievers, and emergency supplies for travelers.",
            "benefits": [
                "✅ 100+ piece medical kit",
                "✅ Compact and lightweight",
                "✅ Perfect for international travel",
                "✅ Includes COVID essentials"
            ],
            "affiliate_link": "https://www.amazon.in/s?k=travel+first+aid+kit&tag=covidvaccinetracker-21",
            "cta": "Shop on Amazon",
            "icon": "🩹"
        }
    ],
    
    "vpn_services": [
        {
            "name": "NordVPN",
            "description": "Premium VPN service to protect your data while traveling. Access content from anywhere securely.",
            "benefits": [
                "✅ Military-grade encryption",
                "✅ 5,500+ servers in 60 countries",
                "✅ No-logs policy",
                "✅ 30-day money-back guarantee"
            ],
            "affiliate_link": "https://nordvpn.com/",  # Replace with actual affiliate link when approved
            "cta": "Get NordVPN",
            "icon": "🔒"
        },
        {
            "name": "ExpressVPN",
            "description": "Fast and reliable VPN for secure browsing abroad. Unblock websites and protect your privacy.",
            "benefits": [
                "✅ Lightning-fast speeds",
                "✅ 160 locations in 94 countries",
                "✅ 24/7 customer support",
                "✅ Easy-to-use apps"
            ],
            "affiliate_link": "https://www.expressvpn.com/",  # Replace with actual affiliate link when approved
            "cta": "Try ExpressVPN",
            "icon": "⚡"
        }
    ]
}


def get_affiliate_disclosure():
    """Return FTC-compliant affiliate disclosure statement."""
    return """
    **Affiliate Disclosure:** This page contains affiliate links. If you click through and make a purchase, 
    we may earn a small commission at no additional cost to you. This helps us maintain and improve this free 
    service. We only recommend products we believe will benefit our users. Thank you for your support! 🙏
    """


def track_affiliate_click(product_name, category):
    """
    Track affiliate link clicks in Google Analytics.
    This function can be called when users click affiliate links.
    """
    # This will be integrated with GA4 custom events
    return {
        "event": "affiliate_click",
        "product_name": product_name,
        "category": category
    }


def get_products_by_category(category):
    """Get all products for a specific category."""
    return AFFILIATE_PRODUCTS.get(category, [])


def get_all_categories():
    """Get list of all available affiliate categories."""
    return list(AFFILIATE_PRODUCTS.keys())
