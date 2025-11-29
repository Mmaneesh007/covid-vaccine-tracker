import streamlit.components.v1 as components
import streamlit as st

def geolocation_button_v4():
    """
    Renders a button that gets the user's location and returns the country to Python.
    Version 4.1 - Uses Streamlit component communication instead of direct navigation.
    """
    html_code = """
    <div id="geo-container-v4" style="margin-bottom: 10px; padding: 10px; border: 1px dashed #ccc; border-radius: 5px;">
        <button id="geo-btn" onclick="getLocation()" style="
            background-color: #008CBA;
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
            📍 Auto-Detect My Location (v4)
        </button>
        <p id="status" style="font-size: 12px; color: #333; margin-top: 5px; font-weight: bold;">v4.1 - System Ready</p>
    </div>

    <script>
    function getLocation() {
        const status = document.getElementById("status");
        const btn = document.getElementById("geo-btn");
        
        if (!navigator.geolocation) {
            status.innerHTML = "v4 Error: Geolocation not supported";
            return;
        }

        status.innerHTML = "v4: Requesting location access...";
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
        
        status.innerHTML = "v4: Coordinates found! Looking up country...";
        console.log("Lat:", latitude, "Long:", longitude);

        // Try Primary API (BigDataCloud)
        fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
            .then(response => {
                if (!response.ok) throw new Error("Primary API failed");
                return response.json();
            })
            .then(data => {
                if (!data.countryName) throw new Error("No country in Primary data");
                sendCountryToPython(data.countryName);
            })
            .catch(err1 => {
                console.warn("Primary API failed, trying fallback...", err1);
                status.innerHTML = "v4: Primary failed. Trying fallback...";
                
                // Try Fallback API (Nominatim)
                fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`)
                    .then(response => {
                        if (!response.ok) throw new Error("Fallback API failed");
                        return response.json();
                    })
                    .then(data => {
                        if (!data.address || !data.address.country) throw new Error("No country in Fallback data");
                        sendCountryToPython(data.address.country);
                    })
                    .catch(err2 => {
                        status.innerHTML = "v4 ERROR: " + err2.message;
                        const btn = document.getElementById("geo-btn");
                        btn.disabled = false;
                        btn.style.opacity = "1";
                    });
            });
    }

    function sendCountryToPython(country) {
        const status = document.getElementById("status");
        status.innerHTML = "v4 Success! Found: " + country;
        // Send country back to Streamlit Python
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:setComponentValue",
            value: country
        }, "*");
    }

    function error(err) {
        const status = document.getElementById("status");
        let msg = "Unknown Error";
        switch(err.code) {
            case err.PERMISSION_DENIED:
                msg = "User denied the request for Geolocation.";
                break;
            case err.POSITION_UNAVAILABLE:
                msg = "Location information is unavailable.";
                break;
            case err.TIMEOUT:
                msg = "The request to get user location timed out.";
                break;
            case err.UNKNOWN_ERROR:
                msg = "An unknown error occurred.";
                break;
        }
        status.innerHTML = "v4 Error: " + msg;
        const btn = document.getElementById("geo-btn");
        btn.disabled = false;
        btn.style.opacity = "1";
    }
    </script>
    """
    
    # Render the component and get the returned value
    detected_country = components.html(html_code, height=150)
    
    # If country was detected, update query params and reload
    if detected_country:
        st.query_params["country"] = detected_country
        st.rerun()
