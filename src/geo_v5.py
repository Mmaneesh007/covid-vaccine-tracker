import streamlit.components.v1 as components
import streamlit as st

def geolocation_button_v5():
    """
    Renders a button that gets the user's location and displays the country.
    Version 5.0 - Simplified approach: display detected country, let user select it manually.
    """
    
    # Initialize session states
    if 'geo_detected_country' not in st.session_state:
        st.session_state['geo_detected_country'] = None
    if 'geo_refresh' not in st.session_state:
        st.session_state['geo_refresh'] = 0
    
    html_code = """
    <div id="geo-container-v5" style="margin-bottom: 10px; padding: 10px; background: #f0f8ff; border: 1px solid #4682b4; border-radius: 5px;">
        <button id="geo-btn" onclick="getLocation()" style="
            background-color: #4682b4;
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
        ">
            📍 Detect My Country
        </button>
        <p id="status" style="font-size: 13px; color: #1e3a8a; margin-top: 8px; font-weight: 500;">Click to detect your location</p>
    </div>

    <script>
    const Streamlit = window.parent.Streamlit;
    
    function getLocation() {
        const status = document.getElementById("status");
        const btn = document.getElementById("geo-btn");
        
        if (!navigator.geolocation) {
            status.innerHTML = "❌ Geolocation not supported by your browser";
            return;
        }

        status.innerHTML = "⏳ Requesting location permission...";
        btn.disabled = true;
        btn.style.opacity = "0.7";

        navigator.geolocation.getCurrentPosition(success, error, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const status = document.getElementById("status");
        
        status.innerHTML = "🔍 Finding your country...";
        console.log("Coordinates:", latitude, longitude);

        // Try BigDataCloud API
        fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
            .then(response => response.ok ? response.json() : Promise.reject("API failed"))
            .then(data => {
                if (data.countryName) {
                    showSuccess(data.countryName);
                } else {
                    tryFallback(latitude, longitude, status);
                }
            })
            .catch(() => tryFallback(latitude, longitude, status));
    }

    function tryFallback(lat, lon, status) {
        status.innerHTML = "🔄 Trying backup service...";
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
            .then(response => response.ok ? response.json() : Promise.reject("Fallback failed"))
            .then(data => {
                if (data.address && data.address.country) {
                    showSuccess(data.address.country);
                } else {
                    showError("Could not determine country from location");
                }
            })
            .catch(err => showError("Both services failed: " + err));
    }

    function showSuccess(country) {
        const status = document.getElementById("status");
        status.innerHTML = "✅ Detected: <strong>" + country + "</strong><br><small>Select it from the country list above</small>";
        
        // Send country to Streamlit
        if (Streamlit) {
            Streamlit.setComponentValue(country);
        }
        
        const btn = document.getElementById("geo-btn");
        btn.disabled = false;
        btn.style.opacity = "1";
    }

    function showError(msg) {
        const status = document.getElementById("status");
        status.innerHTML = "❌ Error: " + msg;
        const btn = document.getElementById("geo-btn");
        btn.disabled = false;
        btn.style.opacity = "1";
    }

    function error(err) {
        let msg = "Unknown error";
        if (err.code === err.PERMISSION_DENIED) {
            msg = "Location permission denied. Please allow location access.";
        } else if (err.code === err.POSITION_UNAVAILABLE) {
            msg = "Location information unavailable.";
        } else if (err.code === err.TIMEOUT) {
            msg = "Location request timed out.";
        }
        showError(msg);
    }
    
    // Notify Streamlit that component is ready
    if (Streamlit) {
        Streamlit.setFrameHeight(160);
    }
    </script>
    """
    
    # Render component
    detected_country = components.html(html_code, height=160)
    
    # If country was detected, store in session state and show success
    if detected_country and detected_country != st.session_state['geo_detected_country']:
        st.session_state['geo_detected_country'] = detected_country
        st.session_state['geo_refresh'] = st.session_state.get('geo_refresh', 0) + 1
        st.success(f"📍 **Detected:** {detected_country}  \nPlease select it from the 'Select countries to compare' dropdown below.", icon="🌍")
