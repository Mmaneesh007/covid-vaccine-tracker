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
    <div style="margin-bottom: 10px;">
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
        <p id="status" style="font-size: 12px; color: #666; margin-top: 5px;"></p>
    </div>

    <script>
    function getLocation() {
        const status = document.getElementById("status");
        const btn = document.getElementById("geo-btn");
        
        if (!navigator.geolocation) {
            status.innerHTML = "Geolocation is not supported by your browser";
            return;
        }

        status.innerHTML = "Locating...";
        btn.disabled = true;
        btn.style.opacity = "0.7";

        navigator.geolocation.getCurrentPosition(success, error);
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const status = document.getElementById("status");
        
        status.innerHTML = "Found you! Finding country...";

        // Use OpenStreetMap (Nominatim) for reverse geocoding (Free, No Key)
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`)
            .then(response => response.json())
            .then(data => {
                const country = data.address.country;
                status.innerHTML = "Redirecting to " + country + "...";
                
                // Reload page with country query param
                // We use window.parent.location because Streamlit runs in an iframe
                const currentUrl = new URL(window.parent.location.href);
                currentUrl.searchParams.set('country', country);
                window.parent.location.href = currentUrl.toString();
            })
            .catch(e => {
                status.innerHTML = "Error finding country.";
                console.error(e);
                btn.disabled = false;
                btn.style.opacity = "1";
            });
    }

    function error() {
        const status = document.getElementById("status");
        status.innerHTML = "Unable to retrieve your location";
        const btn = document.getElementById("geo-btn");
        btn.disabled = false;
        btn.style.opacity = "1";
    }
    </script>
    """
    components.html(html_code, height=100)
