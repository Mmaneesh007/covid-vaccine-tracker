import plotly.graph_objects as go
import pandas as pd

def verify_plotly_fix():
    print("Verifying Plotly fix...")
    try:
        # Simulate data
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'pct_vaccinated': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'new_deaths_smoothed_per_million': [5, 4, 3, 2, 1, 0.5, 0.2, 0.1, 0.05, 0]
        })

        # Create dual-axis chart (same logic as app)
        fig = go.Figure()

        # Axis 1: Vaccination Rate (Left)
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['pct_vaccinated'],
            name='Vaccination Rate (%)',
            mode='lines',
            line=dict(color='#667eea', width=3),
            yaxis='y1'
        ))

        # Axis 2: New Deaths (Right)
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['new_deaths_smoothed_per_million'],
            name='Daily Deaths (per million)',
            mode='lines',
            line=dict(color='#e3342f', width=2),
            yaxis='y2',
            opacity=0.8
        ))

        # Layout for dual axis - THIS IS THE FIXED PART
        fig.update_layout(
            title='Test Chart',
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
        
        # Try to build the figure (this triggers validation)
        fig.to_dict()
        print("Successfully built figure with new layout structure!")
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_plotly_fix()
