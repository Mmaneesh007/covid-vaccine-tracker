import streamlit as st
from streamlit_mic_recorder import speech_to_text

def get_voice_input(key="voice_input", language='en'):
    """
    Renders a microphone button and returns the transcribed text.
    """
    # Map our language codes to Google Speech API codes
    lang_map = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'bn': 'bn-IN',
        'ta': 'ta-IN',
        'te': 'te-IN'
    }
    
    speech_lang = lang_map.get(language, 'en-US')
    
    st.markdown("###### 🎙️ Voice Input")
    text = speech_to_text(
        language=speech_lang,
        start_prompt="Click to Speak",
        stop_prompt="Stop Recording",
        just_once=True,
        key=key
    )
    
    return text
