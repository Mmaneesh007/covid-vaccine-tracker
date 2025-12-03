import streamlit as st
from src.social_share import create_vaccination_certificate, create_country_status_card
from src.translations import t
import datetime

def render_share_page():
    """
    Render the 'Share & Viral' page for generating social media cards.
    """
    st.markdown('<p class="main-title">✨ Share & Go Viral</p>', unsafe_allow_html=True)
    st.markdown("### Create beautiful cards to share your status on Instagram, WhatsApp, or Twitter.")
    
    tab1, tab2 = st.tabs(["🎓 Vaccination Certificate", "🌍 Country Status"])
    
    with tab1:
        st.subheader("Create Your Certificate")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            name = st.text_input("Your Name", "Manish")
            date = st.date_input("Vaccination Date", datetime.date.today())
            dose = st.selectbox("Status", ["Fully Vaccinated", "Partially Vaccinated", "Booster Shot"])
            
            if st.button("Generate Certificate"):
                with st.spinner("Designing your certificate..."):
                    image_bytes = create_vaccination_certificate(name, str(date), dose)
                    st.session_state['cert_image'] = image_bytes
                    
        with col2:
            if 'cert_image' in st.session_state:
                st.image(st.session_state['cert_image'], caption="Preview", use_column_width=True)
                
                st.download_button(
                    label="⬇️ Download Image",
                    data=st.session_state['cert_image'],
                    file_name=f"vaccine_certificate_{name}.png",
                    mime="image/png"
                )
            else:
                st.info("👈 Enter your details to generate a preview.")

    with tab2:
        st.subheader("Share Country Stats")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            country = st.selectbox("Select Country", ["India", "United States", "United Kingdom", "Brazil", "China"])
            # In a real app, we'd fetch live data here. For now, we'll let user customize or mock it.
            # Ideally, pass the dataframe here, but for simplicity let's allow manual input or mock.
            
            vax_rate = st.slider("Vaccination Percentage", 0, 100, 75)
            doses = st.text_input("Total Doses (e.g., 2.2B)", "2.2B")
            
            if st.button("Generate Status Card"):
                with st.spinner("Creating status card..."):
                    image_bytes = create_country_status_card(country, str(vax_rate), doses)
                    st.session_state['status_image'] = image_bytes
                    
        with col2:
            if 'status_image' in st.session_state:
                st.image(st.session_state['status_image'], caption="Preview", use_column_width=True)
                
                st.download_button(
                    label="⬇️ Download Image",
                    data=st.session_state['status_image'],
                    file_name=f"{country}_status.png",
                    mime="image/png"
                )
            else:
                st.info("👈 Select a country to generate a preview.")
