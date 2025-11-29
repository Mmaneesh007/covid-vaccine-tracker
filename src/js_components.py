import streamlit.components.v1 as components
import json

def text_to_speech_button(text, lang='en'):
    """
    Renders a button that speaks the given text using the Web Speech API.
    """
    # Map our lang codes to BCP 47 language tags
    lang_map = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'bn': 'bn-IN',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'fr': 'fr-FR'
    }
    voice_lang = lang_map.get(lang, 'en-US')
    
    # Escape single quotes in text to prevent JS errors
    safe_text = text.replace("'", "\\'")
    
    html_code = f"""
    <div style="display: inline-block;">
        <button onclick="speakText()" style="
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 5px 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 5px;
        ">
            <span>🔊</span> Listen
        </button>
    </div>

    <script>
    function speakText() {{
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const msg = new SpeechSynthesisUtterance('{safe_text}');
        msg.lang = '{voice_lang}';
        
        // Try to find a matching voice
        const voices = window.speechSynthesis.getVoices();
        const voice = voices.find(v => v.lang.includes('{voice_lang}'));
        if (voice) {{
            msg.voice = voice;
        }}

        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(html_code, height=40)

def geolocation_button():
    """
    Renders a button that gets the user's location and reloads the page with query params.
    """
    html_code = """
    <div id="geo-container-v3" style="margin-bottom: 10px;">
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
            📍 Auto-Detect My Location
        </button>
        <p id="status" style="font-size: 12px; color: #666; margin-top: 5px;">v3.1 - Ready (Cache Cleared)</p>
    </div>

    <script>
    function getLocation() {
        const status = document.getElementById("status");
        const btn = document.getElementById("geo-btn");
        
        if (!navigator.geolocation) {
            status.innerHTML = "Geolocation is not supported by your browser";
            return;
        }

        status.innerHTML = "Locating... (Please allow permission)";
        btn.disabled = true;
        btn.style.opacity = "0.7";

        navigator.geolocation.getCurrentPosition(success, error);
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const status = document.getElementById("status");
        
        status.innerHTML = "Found coordinates! Identifying country...";
        console.log("Lat:", latitude, "Long:", longitude);

        // Try Primary API (BigDataCloud)
        fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
            .then(response => {
                if (!response.ok) throw new Error("Primary API failed");
                return response.json();
            })
            .then(data => {
                if (!data.countryName) throw new Error("No country in Primary data");
                redirect(data.countryName);
            })
            .catch(err1 => {
                console.warn("Primary API failed, trying fallback...", err1);
                status.innerHTML = "Primary failed. Trying fallback...";
                
                // Try Fallback API (Nominatim)
                fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`)
                    .then(response => {
                        if (!response.ok) throw new Error("Fallback API failed");
                        return response.json();
                    })
                    .then(data => {
                        if (!data.address || !data.address.country) throw new Error("No country in Fallback data");
                        redirect(data.address.country);
                    })
                    .catch(err2 => {
                        status.innerHTML = "Error: Could not determine country. " + err2.message;
                        const btn = document.getElementById("geo-btn");
                        btn.disabled = false;
                        btn.style.opacity = "1";
                    });
            });
    }

    function redirect(country) {
        const status = document.getElementById("status");
        status.innerHTML = "Success! Redirecting to " + country + "...";
        const currentUrl = new URL(window.parent.location.href);
        currentUrl.searchParams.set('country', country);
        window.parent.location.href = currentUrl.toString();
    }

    function error(err) {
        const status = document.getElementById("status");
        status.innerHTML = "Location Access Denied or Error: " + err.message;
        const btn = document.getElementById("geo-btn");
        btn.disabled = false;
        btn.style.opacity = "1";
    }
    </script>
    """
    components.html(html_code, height=125)
