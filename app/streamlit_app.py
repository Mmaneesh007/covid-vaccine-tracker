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
from src.news_feed import display_news_feed
from src.feedback import display_feedback_form

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

# Custom CSS for PREMIUM aesthetics
st.markdown("""
<style>
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Global Styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main Title with Liquid Gradient */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: liquidGradient 8s ease infinite, fadeIn 1s ease;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
        letter-spacing: -1px;
    }
    
    @keyframes liquidGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Glassmorphism Cards */
    .stMetric, div[data-testid="stMetricValue"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideUp 0.6s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.5);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Premium Metric Values */
    div[data-testid="stMetricValue"] {
        color: #fff;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.5);
    }
    
    /* Chart Containers with Glow */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3),
                    0 0 40px rgba(102, 126, 234, 0.2);
        transition: all 0.4s ease;
        animation: fadeIn 0.8s ease;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4),
                    0 0 60px rgba(102, 126, 234, 0.4);
        transform: scale(1.01);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(48, 43, 99, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Buttons with Premium Glow */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Tabs with Neon Effect */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
    }
    
    /* Headers with Glow */
    h1, h2, h3 {
        color: #fff;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        animation: fadeIn 0.6s ease;
    }
    
    /* Text Colors */
    p, span, div {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Expander with Premium Style */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Input Fields */
    input, textarea, select {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Premium Loading Indicator */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Divider with Gradient */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        margin: 2rem 0;
    }
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

    # React to user input
    if prompt := st.chat_input(t('chatbot_placeholder')):
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
        
        # Create choropleth map
        fig = px.choropleth(
            latest_by_country,
            locations='location',
            locationmode='country names',
            color='pct_vaccinated',
            hover_name='location',
            hover_data={
                'pct_vaccinated': ':.2f',
                'total_vaccinations': ':,.0f',
                'people_vaccinated': ':,.0f'
            },
            color_continuous_scale='Viridis',
            title=t('pct_vax_chart'),
            labels={'pct_vaccinated': 'Vaccinated (%)'}
        )
        
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            height=600
        )
        
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
            
            st.info(t('pdf_info'))
            
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
    
    page = st.radio(t('nav_go_to'), [t('nav_dashboard'), t('nav_chatbot')])
    
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
    
    # Data info
    try:
        df = load_vaccination_data()
        st.markdown(f"### {t('data_info')}")
        st.metric(t('last_updated'), df['date'].max().strftime("%Y-%m-%d"))
        st.metric(t('countries_count'), df['location'].nunique())
        st.metric(t('total_records'), f"{len(df):,}")
    except Exception as e:
        st.error("Error loading data info")
    
    # News Feed Widget
    display_news_feed(source='Google News', limit=25)
    
    # Feedback Form Widget
    display_feedback_form()

# Main execution
if page == t('nav_dashboard'):
    show_dashboard()
else:
    show_chatbot()
