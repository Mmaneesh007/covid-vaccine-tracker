import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.integrate import odeint

def SIR_model(y, t, N, beta, gamma):
    """
    The SIR model differential equations.
    S: Susceptible
    I: Infected
    R: Recovered
    N: Total population
    beta: Contact rate
    gamma: Mean recovery rate
    """
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def render_simulator():
    """
    Renders the Pandemic Simulator UI in Streamlit
    """
    st.markdown("## 🧪 Pandemic Simulator: See How Viruses Spread")
    
    # Beginner-friendly introduction
    st.info("""
    **🎓 What is this?**  
    This simulator shows how a disease spreads through a population. You can see how different actions (like social distancing, masks, or vaccines) help "flatten the curve."
    
    **💡 How to use:**
    1. Choose a scenario below (or customize your own)
    2. Watch the graph update in real-time
    3. Notice how the **Red Line** (infected people) changes!
    """)
    
    # Add scenario presets
    st.subheader("🎯 Try These Scenarios")
    scenario = st.selectbox(
        "Quick Scenarios:",
        [
            "Custom (adjust yourself)",
            "😷 Strong Prevention (Masks + Distance)",
            "🤝 Normal Life (No precautions)",
            "💉 High Vaccination (70% immune)",
            "🚨 Highly Contagious Virus"
        ]
    )
    
    # Preset values based on scenario
    if scenario == "😷 Strong Prevention (Masks + Distance)":
        beta_default, gamma_default, R0_default = 0.15, 0.2, 0
        st.success("✅ With masks and distancing, the virus spreads slowly!")
    elif scenario == "🤝 Normal Life (No precautions)":
        beta_default, gamma_default, R0_default = 0.5, 0.1, 0
        st.warning("⚠️ Without precautions, the virus spreads quickly.")
    elif scenario == "💉 High Vaccination (70% immune)":
        beta_default, gamma_default, R0_default = 0.3, 0.15, 700000
        st.success("✅ Vaccination creates 'herd immunity' and protects everyone!")
    elif scenario == "🚨 Highly Contagious Virus":
        beta_default, gamma_default, R0_default = 0.8, 0.1, 0
        st.error("🚨 Very contagious! The curve spikes fast.")
    else:
        beta_default, gamma_default, R0_default = 0.2, 0.1, 0

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ Adjust Settings")
        
        with st.expander("📌 Population Settings", expanded=False):
            N = st.number_input(
                "City Population", 
                min_value=10000, 
                max_value=10_000_000, 
                value=1_000_000, 
                step=10000,
                format="%d",
                help="Total number of people in the city"
            )
            
            I0 = st.number_input(
                "Starting Infections", 
                min_value=1, 
                max_value=1000, 
                value=1,
                help="How many people are infected on Day 1?"
            )
            
            R0 = st.number_input(
                "Already Immune/Vaccinated", 
                min_value=0, 
                max_value=int(N*0.9), 
                value=R0_default,
                help="People who already can't get sick (from vaccines or past infection)"
            )
        
        st.divider()
        
        st.markdown("#### 🔧 Disease Behavior")
        
        # Simplified explanation for transmission
        st.markdown("**How Contagious is it?**")
        st.caption("Higher = Spreads faster (like flu vs. common cold)")
        beta = st.slider(
            "Contagiousness", 
            min_value=0.0, 
            max_value=1.0, 
            value=beta_default, 
            step=0.05,
            format="%.2f",
            label_visibility="collapsed"
        )
        
        # Simplified explanation for recovery
        st.markdown("**How Fast Do People Recover?**")
        st.caption("Higher = Get well faster (shorter illness)")
        gamma = st.slider(
            "Recovery Speed", 
            min_value=0.05, 
            max_value=0.5, 
            value=gamma_default, 
            step=0.05,
            format="%.2f",
            label_visibility="collapsed"
        )
        
        days = st.slider(
            "⏳ Simulate for How Many Days?", 
            min_value=30, 
            max_value=365, 
            value=160
        )
        
        # Calculate R_naught with explanation
        r_naught = beta / gamma
        st.divider()
        st.markdown("#### 📈 Prediction")
        if r_naught > 1:
            st.error(f"**⚠️ Outbreak Alert!**  \nEach sick person infects **{r_naught:.1f}** others on average.  \n→ The virus will **spread** through the population.")
        else:
            st.success(f"**✅ Under Control!**  \nEach sick person infects only **{r_naught:.1f}** others.  \n→ The virus will **die out** naturally.")

    with col2:
        # Run Simulation
        t = np.linspace(0, days, days)
        y0 = S0, I0, R0_val = N - I0 - R0, I0, R0
        
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(SIR_model, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T
        
        # Create DataFrame for plotting
        df_sim = pd.DataFrame({
            'Day': t,
            'Healthy (Can Get Sick)': S,
            'Currently Sick': I,
            'Recovered/Immune': R
        })
        
        # Plot with user-friendly labels
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sim['Day'], y=df_sim['Healthy (Can Get Sick)'], 
            mode='lines', name='😊 Healthy (Can Get Sick)',
            line=dict(color='#3498db', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_sim['Day'], y=df_sim['Currently Sick'], 
            mode='lines', name='🤒 Currently Sick',
            line=dict(color='#e74c3c', width=3),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_sim['Day'], y=df_sim['Recovered/Immune'], 
            mode='lines', name='✅ Recovered/Immune',
            line=dict(color='#2ecc71', width=2)
        ))
        
        fig.update_layout(
            title="🦠 How the Disease Spreads Over Time",
            xaxis_title="Days Since Outbreak Started",
            yaxis_title="Number of People",
            template="plotly_white",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key Stats with explanations
        peak_infected = max(I)
        peak_day = list(I).index(peak_infected)
        total_infected = N - S[-1]
        
        st.markdown("### 📊 What Happens?")
        k1, k2, k3 = st.columns(3)
        k1.metric("Worst Day", f"Day {peak_day}", help="When hospitals are most crowded")
        k2.metric("Max Sick at Once", f"{int(peak_infected):,}", help="Peak number of sick people")
        k3.metric("Total Affected", f"{int(total_infected):,}", help="Everyone who gets sick (total)")
        
        # Add interpretation
        pct_affected = (total_infected / N) * 100
        if pct_affected > 70:
            st.error(f"🚨 **{pct_affected:.0f}% of the population gets infected!** This is a major outbreak.")
        elif pct_affected > 30:
            st.warning(f"⚠️ **{pct_affected:.0f}% of the population gets infected.** Moderate spread.")
        else:
            st.success(f"✅ **Only {pct_affected:.0f}% get infected.** The outbreak is contained!")

if __name__ == "__main__":
    # Test standalone
    st.set_page_config(layout="wide")
    render_simulator()
