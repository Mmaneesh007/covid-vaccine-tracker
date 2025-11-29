import streamlit.components.v1 as components

def show_my_location_button():
    """
    Renders a button that opens Google Maps with the user's current location.
    Simple, clean implementation with no Streamlit communication needed.
    """
    html_code = """
    <div style="margin-bottom: 10px;">
        <button id="location-btn" onclick="showMyLocation()" style="
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            width: 100%;
            font-weight: 500;
        ">
            📍 Show My Location
        </button>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 5px; text-align: center;"></p>
    </div>

    <script>
    function showMyLocation() {
        const status = document.getElementById("status");
        const btn = document.getElementById("location-btn");
        
        if (!navigator.geolocation) {
            status.innerHTML = "Location not supported";
            status.style.color = "#f44336";
            return;
        }

        status.innerHTML = "Getting location...";
        status.style.color = "#2196F3";
        btn.disabled = true;
        btn.style.opacity = "0.7";

        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                status.innerHTML = "Opening Google Maps...";
                
                // Open Google Maps in new tab
                window.open(`https://www.google.com/maps?q=${lat},${lon}`, '_blank');
                
                // Reset button
                setTimeout(() => {
                    status.innerHTML = "";
                    btn.disabled = false;
                    btn.style.opacity = "1";
                }, 1500);
            },
            function(error) {
                let msg = "Error getting location";
                if (error.code === error.PERMISSION_DENIED) {
                    msg = "Permission denied";
                } else if (error.code === error.POSITION_UNAVAILABLE) {
                    msg = "Location unavailable";
                } else if (error.code === error.TIMEOUT) {
                    msg = "Request timed out";
                }
                status.innerHTML = msg;
                status.style.color = "#f44336";
                btn.disabled = false;
                btn.style.opacity = "1";
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    }
    </script>
    """
    
    components.html(html_code, height=80)
