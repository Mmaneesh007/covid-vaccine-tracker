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

# Page configuration
st.set_page_config(
    page_title="COVID-19 Vaccine Tracker",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stPlotlyChart {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
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

# Header
st.markdown('<p class="main-title">💉 COVID-19 Vaccine Tracker</p>', unsafe_allow_html=True)
st.markdown("### Real-time global vaccination monitoring and forecasting")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Data refresh button
    if st.button("🔄 Refresh Data", help="Download latest vaccination data"):
        with st.spinner("Downloading and processing latest data..."):
            df = refresh_data()
            st.success("Data updated successfully!")
    
    st.divider()
    
    # About section
    st.markdown("### About")
    st.info("""
    This dashboard tracks global COVID-19 vaccination progress using data from 
    [Our World in Data](https://ourworldindata.org/).
    
    **Features:**
    - 📊 Interactive visualizations
    - 🌍 Global vaccination map
    - 📈 30-day forecasts
    - 🔄 Daily data updates
    """)
    
    st.divider()
    
    # Data info
    try:
        df = load_vaccination_data()
        st.markdown("### 📅 Data Info")
        st.metric("Last Updated", df['date'].max().strftime("%Y-%m-%d"))
        st.metric("Countries", df['location'].nunique())
        st.metric("Total Records", f"{len(df):,}")
    except Exception as e:
        st.error("Error loading data info")

# Main content
try:
    df = load_vaccination_data()
    
    # Global Overview
    st.header("🌍 Global Overview")
    
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
            "Total Doses",
            f"{total_vaccinations / 1e9:.2f}B" if pd.notna(total_vaccinations) else "N/A"
        )
    
    with col2:
        st.metric(
            "People Vaccinated",
            f"{total_people_vaccinated / 1e9:.2f}B" if pd.notna(total_people_vaccinated) else "N/A"
        )
    
    with col3:
        st.metric(
            "Fully Vaccinated",
            f"{total_fully_vaccinated / 1e9:.2f}B" if pd.notna(total_fully_vaccinated) else "N/A"
        )
    
    with col4:
        pct_vaccinated = (total_people_vaccinated / total_population * 100) if pd.notna(total_population) and total_population > 0 else 0
        st.metric(
            "Global Coverage",
            f"{pct_vaccinated:.1f}%" if pct_vaccinated > 0 else "N/A"
        )
    
    st.divider()
    
    # Country Selection
    st.header("📊 Country Analysis")
    
    # Filter out aggregated regions (they usually contain spaces or special chars)
    countries = sorted([c for c in df['location'].unique() if pd.notna(c)])
    
    # Default countries for comparison
    default_countries = ['India', 'United States', 'China', 'United Kingdom', 'Brazil']
    default_selection = [c for c in default_countries if c in countries]
    
    selected_countries = st.multiselect(
        "Select countries to compare:",
        options=countries,
        default=default_selection[:3] if default_selection else countries[:3],
        help="Choose up to 5 countries for comparison"
    )
    
    if selected_countries:
        # Filter data for selected countries
        country_data = df[df['location'].isin(selected_countries)].copy()
        
        # Time Series Visualizations
        st.subheader("📈 Vaccination Trends")
        
        tab1, tab2, tab3 = st.tabs(["Daily Vaccinations", "Cumulative Progress", "Population Coverage"])
        
        with tab1:
            # Daily vaccinations with 7-day average
            fig = px.line(
                country_data,
                x='date',
                y='daily_vaccinations_7d',
                color='location',
                title='Daily Vaccinations (7-day average)',
                labels={'daily_vaccinations_7d': 'Daily Vaccinations', 'date': 'Date', 'location': 'Country'},
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
                title='Cumulative Vaccination Doses',
                labels={'total_vaccinations': 'Total Vaccinations', 'date': 'Date', 'location': 'Country'},
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
                title='Percentage of Population Vaccinated',
                labels={'pct_vaccinated': 'Population Vaccinated (%)', 'date': 'Date', 'location': 'Country'},
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
        st.header("📉 Impact Analysis: Vaccines vs. Deaths")
        st.markdown("Visualizing the correlation between rising vaccination rates and falling death rates.")

        impact_country = st.selectbox(
            "Select country for impact analysis:",
            options=selected_countries,
            key="impact_country",
            help="Compare vaccination progress with mortality trends"
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
                    st.info("Calculated deaths per million from raw data.")
            
            # Final check for valid data and filter to usable rows
            required_cols = ['pct_vaccinated', 'new_deaths_smoothed_per_million']
            
            # Filter to only rows where BOTH columns have non-null values
            valid_data = country_impact_data.dropna(subset=required_cols)
            
            if len(valid_data) == 0:
                st.warning(f"No overlapping data available for {impact_country}. The vaccination data and death data may not cover the same time period.")
            else:
                # Create dual-axis chart
                fig = go.Figure()

                # Axis 1: Vaccination Rate (Left)
                fig.add_trace(go.Scatter(
                    x=valid_data['date'],
                    y=valid_data['pct_vaccinated'],
                    name='Vaccination Rate (%)',
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
                        title=dict(text='Vaccinated Population (%)', font=dict(color='#667eea')),
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
                
                st.info(f"💡 **Insight:** Observe how the red line (deaths) tends to flatten or decline as the blue line (vaccinations) rises.")

        st.divider()
        
        # Forecasting Section
        st.header("🔮 Vaccination Forecast")
        
        forecast_country = st.selectbox(
            "Select a country for 30-day forecast:",
            options=selected_countries,
            help="Generate Prophet-based predictions"
        )
        
        if st.button("Generate Forecast"):
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
                            st.metric("Forecast Period", "30 days")
                        with col2:
                            avg_forecast = future['yhat'].mean()
                            st.metric("Avg. Daily Forecast", f"{avg_forecast:,.0f}")
                        with col3:
                            total_forecast = future['yhat'].sum()
                            st.metric("Total Expected", f"{total_forecast / 1e6:.2f}M doses")
                        
                    else:
                        st.warning(f"Insufficient data for {forecast_country}. Need at least 30 days of history.")
                
                except Exception as e:
                    st.error(f"Error generating forecast: {str(e)}")
    
    else:
        st.info("👆 Please select at least one country to view visualizations")
    
    st.divider()
    
    # Global Map
    st.header("🗺️ Global Vaccination Map")
    
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
        title='Vaccination Coverage by Country (%)',
        labels={'pct_vaccinated': 'Vaccinated (%)'}
    )
    
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top performers table
    st.subheader("🏆 Top Performing Countries")
    
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
        st.info("No data available for the latest date.")

except Exception as e:
    st.error(f"Error loading dashboard: {str(e)}")
    st.exception(e)


# COVID-19 Symptom Checker
st.divider()
st.header("🩺 COVID-19 Symptom Self-Assessment")

# Medical Disclaimer
st.warning("""
⚠️ **MEDICAL DISCLAIMER**  
This is NOT a diagnostic tool and does not replace professional medical advice, diagnosis, or treatment. 
If you have symptoms, please consult a healthcare provider and get tested for COVID-19.
""")

st.markdown("""
This assessment is based on symptoms recognized by the **WHO** and **CDC**. 
It helps you understand if you should get tested, but it cannot confirm or rule out COVID-19.
""")

# Symptom Checker Form
with st.form("symptom_checker"):
    st.subheader("📋 Check Your Symptoms")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Primary Symptoms:**")
        fever = st.checkbox("🌡️ Fever (>100.4°F / 38°C)")
        cough = st.checkbox("🤧 New continuous cough")
        breathing = st.checkbox("😮‍💨 Difficulty breathing / shortness of breath")
        taste_smell = st.checkbox("👃 Loss of taste or smell")
    
    with col2:
        st.markdown("**Other Symptoms:**")
        fatigue = st.checkbox("😴 Unusual tiredness / fatigue")
        body_aches = st.checkbox("💪 Muscle or body aches")
        sore_throat = st.checkbox("🗣️ Sore throat")
        headache = st.checkbox("🤕 Headache")
        congestion = st.checkbox("🤧 Nasal congestion or runny nose")
        nausea = st.checkbox("🤢 Nausea or vomiting")
        diarrhea = st.checkbox("🚽 Diarrhea")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        exposure = st.radio(
            "Have you been in close contact with someone who tested positive for COVID-19?",
            ["No", "Yes, within last 14 days", "Unsure"]
        )
    
    with col2:
        vaccinated = st.radio(
            "Vaccination Status:",
            ["Unvaccinated", "Partially Vaccinated", "Fully Vaccinated", "Boosted"]
        )
    
    submitted = st.form_submit_button("🔍 Assess Risk", use_container_width=True)
    
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
        elif primary_symptoms >= 2 and exposure == "Yes, within last 14 days":
            high_risk = True
        elif total_symptoms >= 4:
            high_risk = True
        # Moderate risk criteria
        elif primary_symptoms >= 1 or total_symptoms >= 2:
            moderate_risk = True
        elif exposure == "Yes, within last 14 days":
            moderate_risk = True
        
        st.divider()
        
        # Display results
        if high_risk:
            st.error("""
            ### 🚨 HIGH RISK ASSESSMENT
            
            Based on your symptoms, you may have COVID-19. Please take the following steps:
            
            **Immediate Actions:**
            1. ✅ **Get tested immediately** - Find testing locations below
            2. 🏠 **Self-isolate** - Stay away from others, including household members
            3. 😷 **Wear a mask** if you must be around others
            4. 📞 **Contact your healthcare provider** if symptoms worsen
            
            **Seek Emergency Care if you experience:**
            - Trouble breathing
            - Persistent chest pain or pressure
            - New confusion
            - Inability to wake or stay awake
            - Pale, gray, or blue-colored skin, lips, or nail beds
            """)
            
        elif moderate_risk:
            st.warning("""
            ### ⚠️ MODERATE RISK ASSESSMENT
            
            You have some symptoms that could indicate COVID-19.
            
            **Recommended Actions:**
            1. ✅ **Get tested** - Schedule a COVID-19 test
            2. 🏠 **Stay home** - Avoid contact with others until you get tested
            3. 😷 **Wear a mask** around others
            4. 👁️ **Monitor symptoms** - Watch for worsening symptoms
            5. 📞 **Contact your healthcare provider** if symptoms worsen
            """)
            
        else:
            st.success("""
            ### ✅ LOW RISK ASSESSMENT
            
            Based on your responses, you currently have a low risk for COVID-19.
            
            **Continue Preventive Measures:**
            - 💉 Stay up-to-date with vaccinations
            - 😷 Wear masks in crowded indoor spaces
            - 👐 Wash hands frequently
            - 📏 Maintain social distance when possible
            - 👁️ Monitor for new symptoms
            
            **Note:** This assessment is based on current symptoms only. Get tested if you develop new symptoms or have known exposure.
            """)
        
        # Generate PDF Report Button
        st.divider()
        st.subheader("📄 Download Your Assessment Report")
        
        # Prepare symptoms data for PDF
        symptoms_data = {
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
            
            # Download button
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                help="Download a detailed PDF report of your symptom assessment to share with your healthcare provider"
            )
            
            st.info("💡 **This report can be shared with your healthcare provider for better consultation.**")
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
        
        st.divider()
        
        # Testing locations and resources
        st.subheader("🔬 Find COVID-19 Testing Locations")
        
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
        
        st.info("💡 **Tip:** Many pharmacies and clinics offer rapid testing. Check with your local pharmacy for availability.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Data source: <a href='https://ourworldindata.org/' target='_blank'>Our World in Data</a></p>
    <p>Built with ❤️ using Streamlit • Prophet • Plotly</p>
</div>
""", unsafe_allow_html=True)

