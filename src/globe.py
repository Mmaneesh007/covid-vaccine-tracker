import plotly.graph_objects as go
import pandas as pd

def render_3d_globe(df):
    """
    Render a 3D interactive globe showing vaccination coverage.
    
    Args:
        df (pd.DataFrame): DataFrame containing vaccination data. 
                           Must have 'location', 'pct_vaccinated', etc.
    
    Returns:
        plotly.graph_objects.Figure: The 3D globe figure.
    """
    # Create the 3D Globe
    fig = go.Figure(data=go.Choropleth(
        locations=df['location'],
        locationmode='country names',
        z=df['pct_vaccinated'],
        text=df['location'],
        colorscale='Viridis',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Vaccinated (%)',
        hovertemplate=(
            "<b>%{text}</b><br>" +
            "Vaccinated: %{z:.1f}%<br>" +
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title_text='Global Vaccination Coverage (3D View)',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='orthographic',
            showocean=True,
            oceancolor='rgb(230, 240, 255)',
            showlakes=True,
            lakecolor='rgb(230, 240, 255)',
            showcountries=True,
            countrycolor='rgb(200, 200, 200)',
            bgcolor='rgba(0,0,0,0)'  # Transparent background
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
