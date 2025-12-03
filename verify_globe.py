import pandas as pd
from src.globe import render_3d_globe
import plotly.graph_objects as go

def test_globe_generation():
    print("Testing 3D Globe Generation...")
    
    # Create mock data
    df = pd.DataFrame({
        'location': ['India', 'USA', 'Brazil'],
        'pct_vaccinated': [75.5, 80.2, 85.1]
    })
    
    try:
        fig = render_3d_globe(df)
        print("Figure generated successfully.")
        
        # Verify it's a 3D globe (orthographic projection)
        layout = fig.to_dict()['layout']
        projection = layout['geo']['projection']['type']
        print(f"Projection type: {projection}")
        
        if projection == 'orthographic':
            print("SUCCESS: 3D Globe projection verified.")
        else:
            print(f"FAILURE: Expected 'orthographic', got '{projection}'")
            
    except Exception as e:
        print(f"ERROR: Failed to generate globe. {str(e)}")

if __name__ == "__main__":
    test_globe_generation()
