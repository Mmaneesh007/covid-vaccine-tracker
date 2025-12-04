# app/streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.etl import load_data
from src.clean import clean_vax
from src.storage import save_df_to_db, get_country_timeseries, DB_PATH
from src.forecast import forecast_country_with_history
from src.utils import format_metric
from src.pdf_generator import create_symptom_assessment_pdf
from src.chatbot import get_chatbot_response
from src.translations import t, SUPPORTED_LANGUAGES
from src.js_components import text_to_speech_button
from src.location_maps import show_my_location_button
from src.news_dashboard import render_news_dashboard
from src.feedback import display_feedback_form
from src.particles import show_particle_background
from src.simulation import render_simulator
from src.voice_input import get_voice_input
from src.comparison import render_comparison
from src.globe import render_3d_globe
from src.insights import generate_country_insight, generate_global_insight
from src.pwa_injector import inject_pwa_components

# Page configuration
st.set_page_config(
    page_title="COVID-19 Vaccine Tracker",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize language in session state if not present
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Inject PWA Components (manifest, service worker, meta tags)
inject_pwa_components()

# Render Particle Background
show_particle_background()

# Custom CSS - Google Antigravity Inspired (Light Theme) with Elegant Animations
st.markdown("""
<style>
    /* Import Google Sans Display for that premium Google feel */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Google+Sans+Display:wght@400;500&display=swap');
    
    /* Global Styling - Clean & Minimal */
    * {
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Transparent Background to show Particles */
    .stApp {
        background: transparent !important;
    }
    
    /* Elegant Title - Gradient Text with Entrance Animation */
    .main-title {
        font-family: 'Google Sans Display', sans-serif;
        font-size: 4rem;
        font-weight: 500;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        animation: elegantFadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes elegantFadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0);
        }
    }
    
    /* Staggered Card Entrance Animations */
    .stMetric {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
    }
    
    /* Stagger effect for multiple cards */
    .stMetric:nth-child(1) { animation-delay: 0.1s; }
    .stMetric:nth-child(2) { animation-delay: 0.2s; }
    .stMetric:nth-child(3) { animation-delay: 0.3s; }
    .stMetric:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes slideInScale {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .stMetric:hover {
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-4px) scale(1.02);
    }
    
    /* Animated Metric Values with Counter Effect */
    div[data-testid="stMetricValue"] {
        color: #1a1a1a;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        animation: pulseGlow 3s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.9; }
    }
    
    div[data-testid="stMetricLabel"] {
        color: #5f6368;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Animated Chart Containers */
    .stPlotlyChart {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.06);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.4s ease;
        animation: fadeInUp 0.8s ease backwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Light Sidebar with Slide In */
    section[data-testid="stSidebar"] {
        background: #f8f9fa;
        border-right: 1px solid rgba(0, 0, 0, 0.08);
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Animated Buttons with Ripple Effect */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 0.625rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.875rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px) scale(1.02);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Clean Tabs with Smooth Transitions */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        animation: fadeIn 0.6s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #5f6368;
        border-radius: 0;
        padding: 0.75rem 1rem;
        border-bottom: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #667eea;
        border-bottom-color: #667eea;
    }
    
    /* Typography - Animated Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a;
        font-weight: 500;
        letter-spacing: -0.3px;
        animation: fadeInUp 0.6s ease backwards;
    }
    
    h1 { font-size: 2.5rem; animation-delay: 0.1s; }
    h2 { font-size: 2rem; animation-delay: 0.15s; }
    h3 { font-size: 1.5rem; animation-delay: 0.2s; }
    
    /* Text with Subtle Fade In */
    p, span, div, label {
        color: #3c4043;
        line-height: 1.6;
    }
    
    /* Animated Expanders */
    .streamlit-expanderHeader {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        color: #1a1a1a;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    .streamlit-expanderHeader:hover {
        background: #f8f9fa;
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        transform: translateY(-1px);
    }
    
    /* Smooth Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f3f4;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animated Input Fields */
    input, textarea, select {
        background: #ffffff !important;
        border: 1px solid #dadce0 !important;
        border-radius: 12px !important;
        color: #1a1a1a !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #667eea !important;
        background: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        transform: scale(1.01);
    }
    
    /* Animated Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        margin: 2rem 0;
        animation: fadeIn 0.8s ease;
    }
    
    /* Spinning Loading Indicator */
    .stSpinner > div {
        border-top-color: #667eea !important;
        animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Animated Chat Messages */
    .stChatMessage {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        animation: slideInScale 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Select Box with Animation */
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #dadce0 !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #667eea !important;
    }
    
    /* Animated Multiselect Tags */
    div[data-baseweb="tag"] {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
        color: #667eea !important;
        animation: popIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transition: all 0.2s ease;
    }
    
    @keyframes popIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    div[data-baseweb="tag"]:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        transform: scale(1.05);
    }
    
    /* Info/Warning/Error Boxes with Entrance */
    .stAlert {
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        animation: slideInScale 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Columns with Stagger Effect */
    [data-testid="column"] {
        animation: fadeInUp 0.6s ease backwards;
    }
    
    [data-testid="column"]:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="column"]:nth-child(2) { animation-delay: 0.2s; }
    [data-testid="column"]:nth-child(3) { animation-delay: 0.3s; }
    [data-testid="column"]:nth-child(4) { animation-delay: 0.4s; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_vaccination_data():
    """Load and clean vaccination data, with caching"""
    if os.path.exists(DB_PATH):
        # Try to load from database first
        try:
            from sqlalchemy import create_engine
            engine = create_engine(f"sqlite:///{DB_PATH}")
            df = pd.read_sql("SELECT * FROM countries_vaccinations", engine, parse_dates=["date"])
            return df
        except:
            pass
    
    # Fallback to loading from source
    df = load_data()
    df_clean = clean_vax(df)
    save_df_to_db(df_clean)
    return df_clean

def refresh_data():
    """Force refresh data from source"""
    st.cache_data.clear()
    df = load_data()
    df_clean = clean_vax(df)
    save_df_to_db(df_clean)
    return df_clean

def show_chatbot():
    """Display the AI Health Assistant interface"""
    st.markdown(f'<p class="main-title">{t("chatbot_title")}</p>', unsafe_allow_html=True)
    st.markdown(f"### {t('chatbot_subtitle')}")
    
    st.info(f"""
    **{t('chatbot_help_title')}**
    {t('chatbot_help_desc')}
    """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": t('chatbot_welcome')}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Add Listen button for assistant messages
            if message["role"] == "assistant":
                text_to_speech_button(message["content"], lang=st.session_state.language)

    # Voice Input
    voice_text = get_voice_input(language=st.session_state.language)
    
    # React to user input (Text OR Voice)
    prompt = st.chat_input(t('chatbot_placeholder'))
    
    # If voice input is detected, use it as prompt
    if voice_text:
        prompt = voice_text

    if prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner(t('chatbot_thinking')):
                # Pass current language to chatbot
                response = get_chatbot_response(prompt, lang=st.session_state.language)
                st.markdown(response)
                
                # Add Text-to-Speech Button
                text_to_speech_button(response, lang=st.session_state.language)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def show_dashboard():
    """Display the main dashboard"""
    # Header
    st.markdown(f'<p class="main-title">{t("dashboard_title")}</p>', unsafe_allow_html=True)
    st.markdown(f"### {t('dashboard_subtitle')}")

    try:
        df = load_vaccination_data()
        
        # Global Overview
        st.header(t('global_overview'))
        
        # Get latest stats
        latest_date = df['date'].max()
        latest_stats = df[df['date'] == latest_date].copy()
        
        # Calculate global totals
        total_vaccinations = latest_stats['total_vaccinations'].sum()
        total_people_vaccinated = latest_stats['people_vaccinated'].sum()
        total_fully_vaccinated = latest_stats['people_fully_vaccinated'].sum()
        total_population = latest_stats['population'].sum()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                t('total_doses'),
                f"{total_vaccinations / 1e9:.2f}B" if pd.notna(total_vaccinations) else "N/A"
            )
        
        with col2:
            st.metric(
                t('people_vaccinated'),
                f"{total_people_vaccinated / 1e9:.2f}B" if pd.notna(total_people_vaccinated) else "N/A"
            )
        
        with col3:
            st.metric(
                t('fully_vaccinated'),
                f"{total_fully_vaccinated / 1e9:.2f}B" if pd.notna(total_fully_vaccinated) else "N/A"
            )
        
        with col4:
            pct_vaccinated = (total_people_vaccinated / total_population * 100) if pd.notna(total_population) and total_population > 0 else 0
            st.metric(
                t('global_coverage'),
                f"{pct_vaccinated:.1f}%" if pct_vaccinated > 0 else "N/A"
            )
        
        # AI-Generated Global Insight
        try:
            global_insight = generate_global_insight(df)
            st.info(f"🧠 **AI Insights:** {global_insight}")
        except Exception as e:
            pass  # Silently skip if insights fail
        
        st.divider()
        
        # Country Selection
        st.header(t('country_analysis'))
        
        # Filter out aggregated regions (they usually contain spaces or special chars)
        countries = sorted([c for c in df['location'].unique() if pd.notna(c)])
        
        # Default countries for comparison
        default_countries = ['India', 'United States', 'China', 'United Kingdom', 'Brazil']
        
        # If geolocation found a country, add it to defaults
        if 'detected_country' in st.session_state:
            detected = st.session_state['detected_country']
            if detected in countries and detected not in default_countries:
                default_countries.insert(0, detected)
            elif detected in default_countries:
                # Move to front
                default_countries.remove(detected)
                default_countries.insert(0, detected)

        default_selection = [c for c in default_countries if c in countries]
        
        selected_countries = st.multiselect(
            t('select_countries'),
            options=countries,
            default=default_selection[:3] if default_selection else countries[:3]
        )
        
        # AI Insights for first selected country
        if selected_countries:
            try:
                primary_country = selected_countries[0]
                country_insight = generate_country_insight(df, primary_country)
                st.info(f"🧠 **AI Insights:** {country_insight}")
            except Exception as e:
                pass  # Silently skip if insights fail
        
        if selected_countries:
            # Filter data for selected countries
            country_data = df[df['location'].isin(selected_countries)].copy()
            
            # Time Series Visualizations
            st.subheader(t('vaccination_trends'))
            
            tab1, tab2, tab3 = st.tabs([t('tab_daily'), t('tab_cumulative'), t('tab_coverage')])
            
            with tab1:
                # Daily vaccinations with 7-day average
                fig = px.line(
                    country_data,
                    x='date',
                    y='daily_vaccinations_7d',
                    color='location',
                    title=t('daily_vax_chart'),
                    labels={'daily_vaccinations_7d': t('daily_vaccinations'), 'date': 'Date', 'location': 'Country'},
                    template='plotly_white'
                )
                fig.update_layout(
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Cumulative vaccinations
                fig = px.line(
                    country_data,
                    x='date',
                    y='total_vaccinations',
                    color='location',
                    title=t('cumulative_vax_chart'),
                    labels={'total_vaccinations': t('total_doses'), 'date': 'Date', 'location': 'Country'},
                    template='plotly_white'
                )
                fig.update_layout(
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Percentage vaccinated
                fig = px.line(
                    country_data,
                    x='date',
                    y='pct_vaccinated',
                    color='location',
                    title=t('pct_vax_chart'),
                    labels={'pct_vaccinated': t('population_coverage'), 'date': 'Date', 'location': 'Country'},
                    template='plotly_white'
                )
                fig.update_layout(
                    hovermode='x unified',
                    yaxis=dict(range=[0, 100]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()

            # Impact Analysis Section
            st.header(t('impact_analysis'))
            st.markdown(t('impact_description'))

            impact_country = st.selectbox(
                t('select_impact_country'),
                options=selected_countries,
                key="impact_country"
            )

            if impact_country:
                country_impact_data = country_data[country_data['location'] == impact_country].copy()
                
                # Check if required columns exist
                # Ensure column exists
                if 'new_deaths_smoothed_per_million' not in country_impact_data.columns:
                    country_impact_data['new_deaths_smoothed_per_million'] = pd.NA
                
                # Check if data is missing (all NaNs) and try to calculate
                if country_impact_data['new_deaths_smoothed_per_million'].isna().all():
                    if 'new_deaths_smoothed' in country_impact_data.columns and 'population' in country_impact_data.columns:
                        # Calculate: (new_deaths_smoothed / population) * 1,000,000
                        country_impact_data['new_deaths_smoothed_per_million'] = (
                            country_impact_data['new_deaths_smoothed'] / country_impact_data['population'] * 1_000_000
                        )
                        st.info(t('calc_deaths'))
                
                # Final check for valid data and filter to usable rows
                required_cols = ['pct_vaccinated', 'new_deaths_smoothed_per_million']
                
                # Filter to only rows where BOTH columns have non-null values
                valid_data = country_impact_data.dropna(subset=required_cols)
                
                if len(valid_data) == 0:
                    st.warning(t('no_overlap').format(country=impact_country))
                else:
                    # Create dual-axis chart
                    fig = go.Figure()

                    # Axis 1: Vaccination Rate (Left)
                    fig.add_trace(go.Scatter(
                        x=valid_data['date'],
                        y=valid_data['pct_vaccinated'],
                        name=t('pct_vax_chart'),
                        mode='lines',
                        line=dict(color='#667eea', width=3),
                        yaxis='y1'
                    ))

                    # Axis 2: New Deaths (Right)
                    fig.add_trace(go.Scatter(
                        x=valid_data['date'],
                        y=valid_data['new_deaths_smoothed_per_million'],
                        name='Daily Deaths (per million)',
                        mode='lines',
                        line=dict(color='#e3342f', width=2),
                        yaxis='y2',
                        opacity=0.8
                    ))

                    # Layout for dual axis
                    fig.update_layout(
                        title=f'{impact_country}: Vaccination Effect on Mortality',
                        xaxis=dict(title='Date'),
                        yaxis=dict(
                            title=dict(text=t('pct_vax_chart'), font=dict(color='#667eea')),
                            tickfont=dict(color='#667eea'),
                            range=[0, 100]
                        ),
                        yaxis2=dict(
                            title=dict(text='Daily Deaths (per million)', font=dict(color='#e3342f')),
                            tickfont=dict(color='#e3342f'),
                            overlaying='y',
                            side='right'
                        ),
                        hovermode='x unified',
                        template='plotly_white',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )

                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info(t('insight_impact'))

            st.divider()
            
            # Forecasting Section
            st.header(t('forecast_title'))
            
            forecast_country = st.selectbox(
                t('select_forecast_country'),
                options=selected_countries
            )
            
            if st.button(t('generate_forecast')):
                with st.spinner(f"Generating forecast for {forecast_country}..."):
                    try:
                        # Get country data
                        country_ts = country_data[country_data['location'] == forecast_country].copy()
                        
                        if len(country_ts) > 30:  # Need sufficient history for Prophet
                            # Generate forecast
                            historical, future = forecast_country_with_history(
                                country_ts, 
                                column="daily_vaccinations",
                                periods=30
                            )
                            
                            # Create forecast visualization
                            fig = go.Figure()
                            
                            # Historical actual values
                            fig.add_trace(go.Scatter(
                                x=historical['ds'],
                                y=historical['actual'],
                                mode='lines',
                                name='Actual',
                                line=dict(color='#667eea', width=2)
                            ))
                            
                            # Historical predictions
                            fig.add_trace(go.Scatter(
                                x=historical['ds'],
                                y=historical['yhat'],
                                mode='lines',
                                name='Model Fit',
                                line=dict(color='#764ba2', width=1, dash='dot'),
                                opacity=0.5
                            ))
                            
                            # Future predictions
                            fig.add_trace(go.Scatter(
                                x=future['ds'],
                                y=future['yhat'],
                                mode='lines',
                                name='Forecast',
                                line=dict(color='#f093fb', width=2)
                            ))
                            
                            # Confidence interval
                            fig.add_trace(go.Scatter(
                                x=pd.concat([future['ds'], future['ds'][::-1]]),
                                y=pd.concat([future['yhat_upper'], future['yhat_lower'][::-1]]),
                                fill='toself',
                                fillcolor='rgba(240, 147, 251, 0.2)',
                                line=dict(color='rgba(255,255,255,0)'),
                                name='Confidence Interval',
                                showlegend=True
                            ))
                            
                            fig.update_layout(
                                title=f'30-Day Vaccination Forecast for {forecast_country}',
                                xaxis_title='Date',
                                yaxis_title='Daily Vaccinations',
                                template='plotly_white',
                                hovermode='x unified'
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Show forecast summary
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric(t('forecast_period'), t('forecast_days'))
                            with col2:
                                avg_forecast = future['yhat'].mean()
                                st.metric(t('avg_daily_forecast'), f"{avg_forecast:,.0f}")
                            with col3:
                                total_forecast = future['yhat'].sum()
                                st.metric(t('total_expected'), f"{total_forecast / 1e6:.2f}M {t('forecast_doses')}")
                            
                        else:
                            st.warning(t('insufficient_data').format(country=forecast_country))
                    
                    except Exception as e:
                        st.error(f"Error generating forecast: {str(e)}")
        
        else:
            st.info(t('select_one_country'))
        
        st.divider()
        
        # Global Map
        st.header(t('global_map'))
        
        # Get latest data for each country
        latest_by_country = df[df['date'] == latest_date].copy()
        
        # Create 3D Globe
        fig = render_3d_globe(latest_by_country)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top performers table
        st.subheader(t('top_performers'))
        
        # Ensure numeric types for sorting and formatting
        numeric_cols = ['pct_vaccinated', 'pct_fully_vaccinated', 'total_vaccinations', 'daily_vaccinations_7d']
        for col in numeric_cols:
            latest_by_country[col] = pd.to_numeric(latest_by_country[col], errors='coerce')

        if not latest_by_country.empty:
            top_countries = latest_by_country.nlargest(10, 'pct_vaccinated')[
                ['location', 'pct_vaccinated', 'pct_fully_vaccinated', 'total_vaccinations', 'daily_vaccinations_7d']
            ].copy()
            
            top_countries.columns = ['Country', 'Vaccinated (%)', 'Fully Vaccinated (%)', 
                                      'Total Doses', '7-Day Avg Daily']
            
            top_countries['Total Doses'] = top_countries['Total Doses'].apply(
                lambda x: format_metric(x, 1e6, "M")
            )
            top_countries['7-Day Avg Daily'] = top_countries['7-Day Avg Daily'].apply(
                lambda x: format_metric(x, 1e3, "K", 1)
            )
            top_countries['Vaccinated (%)'] = top_countries['Vaccinated (%)'].apply(
                lambda x: format_metric(x, 1, "%")
            )
            top_countries['Fully Vaccinated (%)'] = top_countries['Fully Vaccinated (%)'].apply(
                lambda x: format_metric(x, 1, "%")
            )
            
            st.dataframe(top_countries, use_container_width=True, hide_index=True)
        else:
            st.info(t('no_data_latest'))

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.exception(e)


    # COVID-19 Symptom Checker
    st.divider()
    st.header(t('symptom_checker_title'))

    # Medical Disclaimer
    st.warning(f"""
    ⚠️ **{t('medical_disclaimer_title')}**  
    {t('medical_disclaimer_text')}
    """)

    st.markdown(t('symptom_intro'))

    # Symptom Checker Form
    with st.form("symptom_checker"):
        st.subheader(t('check_symptoms'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('primary_symptoms')}**")
            fever = st.checkbox(t('sym_fever'))
            cough = st.checkbox(t('sym_cough'))
            breathing = st.checkbox(t('sym_breathing'))
            taste_smell = st.checkbox(t('sym_taste_smell'))
        
        with col2:
            st.markdown(f"**{t('other_symptoms')}**")
            fatigue = st.checkbox(t('sym_fatigue'))
            body_aches = st.checkbox(t('sym_body_aches'))
            sore_throat = st.checkbox(t('sym_sore_throat'))
            headache = st.checkbox(t('sym_headache'))
            congestion = st.checkbox(t('sym_congestion'))
            nausea = st.checkbox(t('sym_nausea'))
            diarrhea = st.checkbox(t('sym_diarrhea'))
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            exposure = st.radio(
                t('q_exposure'),
                [t('ans_no'), t('ans_yes_14'), t('ans_unsure')]
            )
        
        with col2:
            vaccinated = st.radio(
                t('q_vaccination'),
                [t('vax_unvaccinated'), t('vax_partially'), t('vax_fully'), t('vax_boosted')]
            )
        
        submitted = st.form_submit_button(t('assess_risk'), use_container_width=True)
        
        if submitted:
            # Calculate symptom score
            primary_symptoms = sum([fever, cough, breathing, taste_smell])
            other_symptoms = sum([fatigue, body_aches, sore_throat, headache, congestion, nausea, diarrhea])
            total_symptoms = primary_symptoms + other_symptoms
            
            # Risk assessment logic
            high_risk = False
            moderate_risk = False
            
            # High risk criteria
            if breathing or (taste_smell and fever):
                high_risk = True
            elif primary_symptoms >= 2 and exposure == t('ans_yes_14'):
                high_risk = True
            elif total_symptoms >= 4:
                high_risk = True
            # Moderate risk criteria
            elif primary_symptoms >= 1 or total_symptoms >= 2:
                moderate_risk = True
            elif exposure == t('ans_yes_14'):
                moderate_risk = True
            
            # Store results in session state
            st.session_state['assessment_complete'] = True
            st.session_state['symptoms_data'] = {
                'fever': fever,
                'cough': cough,
                'breathing': breathing,
                'taste_smell': taste_smell,
                'fatigue': fatigue,
                'body_aches': body_aches,
                'sore_throat': sore_throat,
                'headache': headache,
                'congestion': congestion,
                'nausea': nausea,
                'diarrhea': diarrhea
            }
            st.session_state['risk_high'] = high_risk
            st.session_state['risk_moderate'] = moderate_risk
            st.session_state['exposure'] = exposure
            st.session_state['vaccination_status'] = vaccinated

    # Display results OUTSIDE the form
    if st.session_state.get('assessment_complete', False):
        st.divider()
        
        # Retrieve stored values
        high_risk = st.session_state['risk_high']
        moderate_risk = st.session_state['risk_moderate']
        exposure = st.session_state['exposure']
        vaccinated = st.session_state['vaccination_status']
        symptoms_data = st.session_state['symptoms_data']
        
        # Display results
        if high_risk:
            st.error(f"""
            ### {t('high_risk_title')}
            {t('high_risk_text')}
            """)
            
        elif moderate_risk:
            st.warning(f"""
            ### {t('moderate_risk_title')}
            {t('moderate_risk_text')}
            """)
            
        else:
            st.success(f"""
            ### {t('low_risk_title')}
            {t('low_risk_text')}
            """)
        
        # Generate PDF Report Button (OUTSIDE FORM)
        st.divider()
        st.subheader(t('download_pdf'))
        
        # Determine risk level string
        if high_risk:
            risk_level_str = "HIGH"
        elif moderate_risk:
            risk_level_str = "MODERATE"
        else:
            risk_level_str = "LOW"
        
        try:
            # Generate PDF
            pdf_bytes = create_symptom_assessment_pdf(
                symptoms_data=symptoms_data,
                risk_level=risk_level_str,
                exposure=exposure,
                vaccination_status=vaccinated
            )
            
            # Generate filename with timestamp
            from datetime import datetime
            filename = f"COVID19_Assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Download button (NOW OUTSIDE THE FORM)
            st.download_button(
                label=t('download_pdf'),
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                help=t('pdf_help')
            )
            
            # Social Share Card
            from src.social_share import generate_health_check_card
            try:
                share_img = generate_health_check_card(risk_level_str)
                st.download_button(
                    label="📸 Share My Status",
                    data=share_img,
                    file_name=f"Health_Status_{datetime.now().strftime('%Y%m%d')}.png",
                    mime="image/png",
                    use_container_width=True,
                    help="Download and share your health status on social media!"
                )
            except Exception as e:
                pass  # Silently fail if image generation doesn't work
            
            st.info(t('pdf_info'))
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
        
        st.divider()
        
        # Testing locations and resources
        st.subheader(t('find_testing'))
        
        testing_col1, testing_col2 = st.columns(2)
        
        with testing_col1:
            st.markdown("""
            **India:**
            - [ICMR Testing Centers](https://www.icmr.gov.in/)
            - [MyGov India COVID Testing](https://www.mygov.in/covid-19)
            - Call: **1075** (COVID-19 Helpline)
            
            **United States:**
            - [COVID.gov Testing Locator](https://www.covid.gov/tests)
            - [HHS Testing Sites](https://www.hhs.gov/coronavirus/community-based-testing-sites/)
            - Call: **211** for local resources
            """)
        
        with testing_col2:
            st.markdown("""
            **United Kingdom:**
            - [NHS COVID-19 Testing](https://www.nhs.uk/conditions/coronavirus-covid-19/testing/)
            - Call: **119** (COVID-19 Helpline)
            
            **Global Resources:**
            - [WHO COVID-19 Resources](https://www.who.int/emergencies/diseases/novel-coronavirus-2019)
            - Contact your local health department
            - Visit your nearest hospital emergency dept for urgent care
            """)
        
        st.info(t('testing_tip'))

    # News Feed Dashboard
    st.divider()
    render_news_dashboard(limit=6)

    # Footer
    st.divider()
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>{t('data_source')}: <a href='https://ourworldindata.org/' target='_blank'>Our World in Data</a></p>
        <p>{t('built_with')}</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.header(t('nav_title'))
    
    # Language Selector
    lang_code = st.selectbox(
        "Language / भाषा / ভাষা / மொழி / భాష / Langue",
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: SUPPORTED_LANGUAGES[x],
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.language)
    )
    
    # Update session state if language changed
    if lang_code != st.session_state.language:
        st.session_state.language = lang_code
        st.rerun()
        
    st.divider()

    # Location Feature - Opens Google Maps
    show_my_location_button()
    
    st.divider()
    
    # Check for country query param from Geolocation
    # st.query_params is the new way in recent Streamlit versions
    query_params = st.query_params
    if "country" in query_params:
        detected_country = query_params["country"]
        st.success(f"📍 Detected: {detected_country}")
        # We'll use this to set the default in the dashboard if valid
        st.session_state['detected_country'] = detected_country
        # Clear param to avoid sticky state
        # st.query_params.clear() # Optional: keep it for now so user sees it
    
    st.divider()
    
    page = st.radio(t('nav_go_to'), [t('nav_dashboard'), t('nav_chatbot'), t('nav_simulator'), t('nav_comparison'), "🏥 Resources", "✨ Share & Viral", "🔌 Developers"])
    
    st.divider()
    
    st.header(t('nav_settings'))
    
    # Data refresh button
    if st.button(t('refresh_data')):
        with st.spinner("Downloading and processing latest data..."):
            df = refresh_data()
            st.success(t('refresh_success'))
    
    st.divider()
    
    # About section
    st.markdown(f"### {t('nav_about')}")
    st.info(t('about_text'))
    
    st.divider()
    
    # Support the Project
    st.markdown("### ☕ Support the Project")
    st.markdown("If you find this app useful, consider buying me a coffee!")
    st.markdown("[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-orange.svg?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/Manish_Sau)")
    
    
    # UPI Payment Option
    st.markdown("**OR Pay via UPI (India)**")
    
    # Create UPI payment link
    upi_id = "manish7044436272@okaxis"
    name = "Manish Sau"
    upi_link = f"upi://pay?pa={upi_id}&pn={name}&cu=INR"
    
    # Use components.html with proper iframe to handle UPI link
    upi_button_html = f"""
    <div style="margin: 10px 0;">
        <a href="{upi_link}" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
                transition: transform 0.2s;
            ">
                💳 Pay via UPI
            </button>
        </a>
        <div style="font-size: 12px; color: #666; margin-top: 8px; text-align: center;">
            Click to pay with GPay, PhonePe, Paytm, etc.<br>
            UPI ID: {upi_id}
        </div>
    </div>
    """
    
    from streamlit import components
    components.v1.html(upi_button_html, height=120)
    
    st.divider()
    
    # Data info
    try:
        df = load_vaccination_data()
        st.markdown(f"### {t('data_info')}")
        st.metric(t('last_updated'), df['date'].max().strftime("%Y-%m-%d"))
        st.metric(t('countries_count'), df['location'].nunique())
        st.metric(t('total_records'), f"{len(df):,}")
    except Exception as e:
        st.error("Error loading data info")
    
    # News Feed Widget (Moved to Dashboard)
    # render_news_dashboard(limit=6)
    
    # Feedback Form Widget
    display_feedback_form()

def show_api_docs():
    """Display API documentation and usage examples"""
    st.markdown('<p class="main-title">🔌 API Documentation</p>', unsafe_allow_html=True)
    st.markdown("### Access vaccination data programmatically via REST API")
    
    st.info("""
    **Experimental Feature**: The COVID-19 Vaccine Tracker provides a FastAPI-based REST API
    for programmatic access to all vaccination data, forecasts, and AI chatbot features.
    """)
    
    # Quick Start
    st.header("⚡ Quick Start")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Installation")
        st.code("""pip install requests""", language="bash")
    
    with col2:
        st.subheader("Base URL")
        st.code("http://localhost:8000/api/v1", language="text")
    
    st.warning("**Note**: The API runs independently from this Streamlit app on port 8000.")
    
    # Endpoints
    st.header("📡 Available Endpoints")
    
   # Create tabs for different endpoint categories
    tab1, tab2, tab3, tab4 = st.tabs(["Countries", "Forecasting", "Chatbot", "All Endpoints"])
    
    with tab1:
        st.subheader("Get Countries")
        st.code("GET /api/v1/countries", language="http")
        st.markdown("**Description**: Returns a list of all available countries.")
        
        with st.expander("📄 Example Response"):
            st.code("""{
  "countries": ["India", "United States", "Brazil", ...],
  "total_count": 237
}""", language="json")
        
        st.divider()
        
        st.subheader("Get Country Stats")
        st.code("GET /api/v1/countries/{country_name}", language="http")
        st.markdown("**Description**: Get latest vaccination statistics for a specific country.")
        
        with st.expander("💻 Python Example"):
            st.code("""import requests

response = requests.get("http://localhost:8000/api/v1/countries/India")
data = response.json()
print(f"Total Vaccinations: {data['total_vaccinations']:,}")""", language="python")
    
    with tab2:
        st.subheader("Generate Forecast")
        st.code("GET /api/v1/forecast/{country_name}?days=30", language="http")
        st.markdown("**Description**: Generate machine learning forecast using Facebook Prophet.")
        
        with st.expander("💻 Python Example"):
            st.code("""import requests

response = requests.get("http://localhost:8000/api/v1/forecast/USA?days=30")
forecast = response.json()['forecast']

for day in forecast:
    print(f"{day['ds']}: {day['yhat']:.0f} doses")""", language="python")
    
    with tab3:
        st.subheader("Chat with AI")
        st.code("POST /api/v1/chat", language="http")
        st.markdown("**Description**: Send a message to the AI Health Assistant.")
        
        with st.expander("💻 Python Example"):
            st.code("""import requests

payload = {
    "message": "Is the vaccine safe?",
    "language": "en"
}
response = requests.post("http://localhost:8000/api/v1/chat", json=payload)
print(response.json()['message'])""", language="python")
    
    with tab4:
        endpoints_table = """
| Method | Endpoint | Description |
|:-------|:---------|:------------|
| `GET` | `/countries` | List all countries |
| `GET` | `/countries/{name}` | Get country stats |
| `GET` | `/countries/{name}/timeseries` | Get historical data |
| `GET` | `/forecast/{name}` | Generate forecast |
| `POST` | `/chat` | Chat with AI assistant |
| `GET` | `/chat/languages` | Supported languages |
"""
        st.markdown(endpoints_table)
        
        st.info("**Interactive Docs**: Run the API and visit `http://localhost:8000/docs` for full Swagger UI.")
    
    # Code Examples
    st.header("💡 Common Use Cases")
    
    use_cases = {
        "📱 Mobile App Dashboard": "Fetch country stats and display in native UI",
        "🤖 Slack Bot": "Integrate chatbot responses into workspace commands",
        "📊 Automated Reports": "Schedule weekly vaccination analysis reports",
        "🏥 Hospital Kiosk": "Voice-enabled information system",
        "🔬 Data Science": "Correlate vaccination with economic indicators"
    }
    
    for title, desc in use_cases.items():
        st.markdown(f"**{title}**: {desc}")
    
    st.markdown("[View detailed use cases →](https://github.com/Mmaneesh007/covid-vaccine-tracker/blob/main/examples/USE_CASES.md)")
    
    # CLI Tool
    st.header("🔧 Command-Line Tool")
    st.markdown("For quick testing, use the included CLI tool:")
    
    st.code("""# List countries
python examples/api_cli.py list-countries

# Get stats
python examples/api_cli.py stats --country "India"

# Forecast
python examples/api_cli.py forecast --country "USA" --days 30

# Chat
python examples/api_cli.py chat --message "What are side effects?"
""", language="bash")
    
    # Running the API
    st.header("🚀 Running the API Locally")
    
    st.markdown("**Step 1**: Install dependencies")
    st.code("pip install -r app/experimental/requirements-api.txt", language="bash")
    
    st.markdown("**Step 2**: Start the API server")
    st.code(".\\app\\experimental\\start_api.ps1", language="powershell")
    
    st.markdown("**Step 3**: Access the docs")
    st.markdown("Visit [http://localhost:8000/docs](http://localhost:8000/docs)")
    
    st.success("""
    ✅ **Safe to Test**: The API runs on a separate port and does not affect this Streamlit application.
    You can run both simultaneously!
    """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>For more examples, check the <a href='https://github.com/Mmaneesh007/covid-vaccine-tracker/tree/main/examples' target='_blank'>examples/ folder</a> on GitHub.</p>
    </div>
    """, unsafe_allow_html=True)

from src.locator import render_center_locator
from src.reminder import render_vaccine_reminder
from src.share_page import render_share_page

# ... (existing imports)

# Main execution
if page == t('nav_dashboard'):
    show_dashboard()
elif page == t('nav_chatbot'):
    show_chatbot()
elif page == t('nav_simulator'):
    render_simulator()
elif page == t('nav_comparison'):
    render_comparison()
elif page == "🏥 Resources":  # New Page
    st.markdown(f'<p class="main-title">🏥 Resources & Tools</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📍 Center Locator", "📅 Dose Reminder"])
    
    with tab1:
        render_center_locator()
    
    with tab2:
        render_vaccine_reminder()
        
elif page == "✨ Share & Viral":
    render_share_page()
        
elif page == "🔌 Developers":
    show_api_docs()
