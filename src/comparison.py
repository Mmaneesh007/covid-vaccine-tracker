import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.etl import load_data
from src.clean import clean_vax
from src.storage import save_df_to_db, DB_PATH
from src.utils import format_metric
import os

@st.cache_data(ttl=3600)
def get_data():
    if os.path.exists(DB_PATH):
        try:
            from sqlalchemy import create_engine
            engine = create_engine(f"sqlite:///{DB_PATH}")
            df = pd.read_sql("SELECT * FROM countries_vaccinations", engine, parse_dates=["date"])
            return df
        except:
            pass
    
    df = load_data()
    df_clean = clean_vax(df)
    save_df_to_db(df_clean)
    return df_clean

def render_comparison():
    st.markdown("## ⚔️ Country Face-Off")
    st.markdown("Compare vaccination performance head-to-head.")

    df = get_data()
    countries = sorted([c for c in df['location'].unique() if pd.notna(c)])

    col1, col2 = st.columns(2)
    
    with col1:
        country_a = st.selectbox("Select Country A", countries, index=countries.index("India") if "India" in countries else 0)
    
    with col2:
        # Try to pick a different default for B
        default_b = "United States" if "United States" in countries else countries[1]
        country_b = st.selectbox("Select Country B", countries, index=countries.index(default_b) if default_b in countries else 1)

    if country_a and country_b:
        # Get latest data for both
        latest_date = df['date'].max()
        
        # We need the latest row for each country (might not be same date, so take max date per country)
        df_a = df[df['location'] == country_a].sort_values('date').iloc[-1]
        df_b = df[df['location'] == country_b].sort_values('date').iloc[-1]
        
        # Metrics to compare
        metrics = [
            ("Total Doses", 'total_vaccinations', "M", 1e6),
            ("Fully Vaccinated", 'people_fully_vaccinated', "M", 1e6),
            ("Population Covered", 'pct_vaccinated', "%", 1),
            ("Daily Speed (7d avg)", 'daily_vaccinations_7d', "K", 1e3)
        ]
        
        st.divider()
        
        # Battle Cards
        for label, col, suffix, divisor in metrics:
            val_a = df_a[col] if pd.notna(df_a[col]) else 0
            val_b = df_b[col] if pd.notna(df_b[col]) else 0
            
            # Determine winner
            if val_a > val_b:
                winner = "A"
                color_a = "green"
                color_b = "red"
            elif val_b > val_a:
                winner = "B"
                color_a = "red"
                color_b = "green"
            else:
                winner = "Tie"
                color_a = "gray"
                color_b = "gray"
                
            c1, c2, c3 = st.columns([2, 1, 2])
            
            with c1:
                st.markdown(f"<h3 style='text-align: center; color: {color_a}'>{val_a/divisor:.1f}{suffix}</h3>", unsafe_allow_html=True)
            
            with c2:
                st.markdown(f"<p style='text-align: center; font-weight: bold; padding-top: 10px'>{label}</p>", unsafe_allow_html=True)
                
            with c3:
                st.markdown(f"<h3 style='text-align: center; color: {color_b}'>{val_b/divisor:.1f}{suffix}</h3>", unsafe_allow_html=True)
            
            st.divider()

        # Visual Comparison
        st.subheader("📈 Head-to-Head Trend")
        
        hist_a = df[df['location'] == country_a]
        hist_b = df[df['location'] == country_b]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_a['date'], y=hist_a['pct_vaccinated'], name=country_a, line=dict(width=3)))
        fig.add_trace(go.Scatter(x=hist_b['date'], y=hist_b['pct_vaccinated'], name=country_b, line=dict(width=3)))
        
        fig.update_layout(
            title="Vaccination Coverage (%) Over Time",
            xaxis_title="Date",
            yaxis_title="% Vaccinated",
            template="plotly_white",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render_comparison()
