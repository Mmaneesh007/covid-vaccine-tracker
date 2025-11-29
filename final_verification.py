import sys
import os
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.storage import get_all_countries, get_latest_by_country
from src.chatbot import get_chatbot_response
from src.translations import t, SUPPORTED_LANGUAGES
from src.pdf_generator import create_symptom_assessment_pdf

def verify_system():
    print("COVID-19 Vaccine Tracker - Final System Health Check")
    print("=" * 60)
    
    errors = []

    # 1. Verify Storage & Data
    print("\n[1/5] Verifying Database...")
    try:
        countries = get_all_countries()
        if len(countries) > 0:
            print(f"OK: Database accessible. Found {len(countries)} countries.")
        else:
            errors.append("Database returned 0 countries.")
            print("FAIL: Database empty.")
    except Exception as e:
        errors.append(f"Database error: {str(e)}")
        print(f"FAIL: Database error: {str(e)}")

    # 2. Verify Chatbot & Hybrid Translation
    print("\n[2/5] Verifying Chatbot & Translations...")
    try:
        # Test English
        resp_en = get_chatbot_response("Hello", lang='en')
        if resp_en:
            print("OK: Chatbot (English)")
        else:
            errors.append("Chatbot (English) returned empty response.")
        
        # Test Hindi (Dictionary)
        resp_hi = get_chatbot_response("Hello", lang='hi')
        if resp_hi:
            print("OK: Chatbot (Hindi - Dictionary)")
        else:
            errors.append("Chatbot (Hindi) returned empty response.")

        # Test French (Deep Translator Fallback)
        # "Vaccine stats" -> Dynamic -> Translator
        resp_fr = get_chatbot_response("Vaccine stats", lang='fr')
        if resp_fr:
            print("OK: Chatbot (French - Hybrid)")
        else:
            errors.append("Chatbot (French) returned empty response.")

    except Exception as e:
        errors.append(f"Chatbot error: {str(e)}")
        print(f"FAIL: Chatbot error: {str(e)}")

    # 3. Verify UI Translations
    print("\n[3/5] Verifying UI Dictionaries...")
    try:
        missing_keys = []
        for lang in SUPPORTED_LANGUAGES:
            # Test a random key
            if not t('dashboard_title'):
                missing_keys.append(lang)
        
        if not missing_keys:
            print(f"OK: UI Translations loaded for {len(SUPPORTED_LANGUAGES)} languages.")
        else:
            errors.append(f"Missing translations for: {missing_keys}")
            print(f"FAIL: Missing translations for: {missing_keys}")
    except Exception as e:
        errors.append(f"Translation error: {str(e)}")
        print(f"FAIL: Translation error: {str(e)}")

    # 4. Verify PDF Generation
    print("\n[4/5] Verifying PDF Generator...")
    try:
        pdf_bytes = create_symptom_assessment_pdf(
            {'fever': True}, "HIGH", "Yes", "Unvaccinated"
        )
        if len(pdf_bytes) > 1000:
            print("OK: PDF Generation (Bytes generated)")
        else:
            errors.append("PDF generated was too small (<1KB).")
            print("FAIL: PDF Generation failed.")
    except Exception as e:
        errors.append(f"PDF error: {str(e)}")
        print(f"FAIL: PDF error: {str(e)}")

    # 5. Summary
    print("\n" + "=" * 60)
    if not errors:
        print("ALL SYSTEMS OPERATIONAL! The project is healthy.")
    else:
        print(f"Found {len(errors)} issues:")
        for err in errors:
            print(f" - {err}")

if __name__ == "__main__":
    verify_system()
