# src/affiliate_ui.py
"""
Affiliate UI Components
Renders affiliate product cards and resources section.
"""

import streamlit as st
from src.affiliate_links import (
    get_products_by_category,
    get_all_categories,
    get_affiliate_disclosure,
    AFFILIATE_PRODUCTS
)


def render_product_card(product):
    """Render a single affiliate product card with premium design."""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{product['icon']}</div>
        <h3 style="
            color: #1a1a1a;
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        ">{product['name']}</h3>
        <p style="
            color: #5f6368;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        ">{product['description']}</p>
        <div style="margin-bottom: 1rem;">
            {''.join([f'<div style="color: #667eea; font-size: 0.9rem; margin: 0.25rem 0;">{benefit}</div>' for benefit in product['benefits']])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call-to-action button
    # Call-to-action button using direct HTML link to avoid popup blockers
    st.markdown(f"""
    <a href="{product['affiliate_link']}" target="_blank" style="text-decoration: none;" onclick="
        if (typeof gtag !== 'undefined') {{
            gtag('event', 'affiliate_click', {{
                'product_name': '{product['name']}',
                'event_category': 'Affiliate',
                'event_label': 'Product Click'
            }});
        }}
    ">
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
            margin-top: 1rem;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08)';" 
          onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08)';">
            {product['cta']} →
        </div>
    </a>
    """, unsafe_allow_html=True)


def render_category_section(category_key, category_title, icon):
    """Render a complete category section with all products."""
    
    st.markdown(f"## {icon} {category_title}")
    st.markdown("---")
    
    products = get_products_by_category(category_key)
    
    # Render products in columns for better layout
    if len(products) <= 2:
        cols = st.columns(len(products))
        for idx, product in enumerate(products):
            with cols[idx]:
                render_product_card(product)
    else:
        # For more than 2 products, use 2-column layout
        for i in range(0, len(products), 2):
            cols = st.columns(2)
            for idx, product in enumerate(products[i:i+2]):
                with cols[idx]:
                    render_product_card(product)
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_affiliate_resources_page():
    """Main function to render the complete affiliate resources page."""
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="
            font-size: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        ">🌍 Travel & Health Resources</h1>
        <p style="
            color: #5f6368;
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
        ">
            Essential products and services recommended for vaccinated travelers. 
            Stay safe, protected, and connected on your journeys.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Affiliate Disclosure
    st.info(get_affiliate_disclosure())
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different categories
    tab1, tab2, tab3 = st.tabs([
        "🛡️ Travel Insurance",
        "💊 Health Products",
        "🔒 VPN Services"
    ])
    
    with tab1:
        st.markdown("""
        ### Why Travel Insurance?
        
        Protect yourself from unexpected medical expenses, trip cancellations, and emergencies while traveling internationally. 
        Essential for post-pandemic travel peace of mind.
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        
        products = get_products_by_category("travel_insurance")
        for product in products:
            render_product_card(product)
    
    with tab2:
        st.markdown("""
        ### Essential Health Products
        
        Stay protected with high-quality masks, sanitizers, and immune-boosting supplements. 
        Perfect for travelers and health-conscious individuals.
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        
        products = get_products_by_category("health_products")
        
        # Render in 2-column grid
        for i in range(0, len(products), 2):
            cols = st.columns(2)
            for idx, product in enumerate(products[i:i+2]):
                with cols[idx]:
                    render_product_card(product)
    
    with tab3:
        st.markdown("""
        ### Secure Your Connection
        
        Protect your personal data and access content from anywhere with a premium VPN service. 
        Essential for safe browsing on public Wi-Fi while traveling.
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        
        products = get_products_by_category("vpn_services")
        for product in products:
            render_product_card(product)
    
    # Footer note
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #5f6368; font-size: 0.9rem; padding: 1rem 0;">
        💡 <strong>Have questions?</strong> Visit our AI Health Assistant in the chatbot section for personalized advice.
    </div>
    """, unsafe_allow_html=True)
