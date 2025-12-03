"""
Vaccine Center Locator Module
Helps users find vaccination centers using Google Maps and official government portals.
"""
import streamlit as st
import urllib.parse

def render_center_locator():
    """Render the vaccine center locator UI"""
    st.markdown("### 🏥 Find a Vaccination Center")
    st.markdown("Locate the nearest COVID-19 vaccination center using official resources.")
    
    # 1. Quick Search via Google Maps
    st.subheader("📍 Quick Search")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        location = st.text_input("Enter your City or Zip Code", placeholder="e.g., Mumbai, New York, 10001")
    
    with col2:
        st.write("") # Spacing
        st.write("")
        search_btn = st.button("🔍 Search Maps", use_container_width=True)
    
    if search_btn and location:
        # Create Google Maps query
        query = f"COVID-19 vaccination center in {location}"
        encoded_query = urllib.parse.quote(query)
        maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        
        st.success(f"Searching for centers in **{location}**...")
        st.markdown(f"👉 **[Click here to view results on Google Maps]({maps_url})**", unsafe_allow_html=True)
        
        # Embed map (optional, simple iframe if needed, but link is safer/cleaner)
        st.markdown(f"""
        <iframe
            width="100%"
            height="400"
            frameborder="0" style="border:0; border-radius: 12px;"
            src="https://www.google.com/maps/embed/v1/search?key=&q={encoded_query}&zoom=12"
            allowfullscreen>
        </iframe>
        <p style="font-size: 0.8rem; color: #666;">*Map preview requires API key. Use the link above if map doesn't load.</p>
        """, unsafe_allow_html=True)

    st.divider()

    # 2. Official Government Portals
    st.subheader("🌐 Official Booking Portals")
    
    portals = [
        {
            "country": "🇮🇳 India",
            "name": "CoWIN Portal",
            "url": "https://www.cowin.gov.in/",
            "desc": "Register and schedule appointments via Ministry of Health"
        },
        {
            "country": "🇺🇸 United States",
            "name": "Vaccines.gov",
            "url": "https://www.vaccines.gov/",
            "desc": "Find COVID-19 vaccine locations near you"
        },
        {
            "country": "🇬🇧 United Kingdom",
            "name": "NHS Booking",
            "url": "https://www.nhs.uk/conditions/coronavirus-covid-19/coronavirus-vaccination/book-coronavirus-vaccination/",
            "desc": "Book or manage your coronavirus vaccination"
        },
        {
            "country": "🇨🇦 Canada",
            "name": "Government of Canada",
            "url": "https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19/vaccines/how-vaccinated.html",
            "desc": "Provincial and territorial vaccination resources"
        },
        {
            "country": "🇦🇺 Australia",
            "name": "Health Direct",
            "url": "https://www.health.gov.au/initiatives-and-programs/covid-19-vaccines",
            "desc": "Vaccine eligibility checker and booking"
        }
    ]
    
    for portal in portals:
        with st.expander(f"{portal['country']} - {portal['name']}"):
            st.write(portal['desc'])
            st.markdown(f"👉 **[Go to Official Website]({portal['url']})**")

