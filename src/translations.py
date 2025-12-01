"""
Translation infrastructure for COVID-19 Vaccine Tracker
Provides UI and content translation without external APIs
"""

import streamlit as st

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी (Hindi)',
    'bn': 'বাংলা (Bengali)', 
    'ta': 'தமிழ் (Tamil)',
    'te': 'తెలుగు (Telugu)'
}

# UI Translation Dictionaries
UI_TRANSLATIONS = {
    'en': {
        # Page titles
        'page_title': 'COVID-19 Vaccine Tracker',
        'chatbot_title': '🤖 AI Health Assistant',
        'dashboard_title': '💉 COVID-19 Vaccine Tracker',
        'dashboard_subtitle': 'Real-time global vaccination monitoring and forecasting',
        
        # Navigation
        'nav_title': '📍 Navigation',
        'nav_dashboard': 'Dashboard',
        'nav_chatbot': 'AI Health Assistant',
        'nav_settings': '⚙️ Settings',
        'nav_about': 'About',
        'nav_go_to': 'Go to:',
        'nav_simulator': 'Pandemic Simulator',
        'nav_comparison': 'Country Face-Off',
        
        # Global Overview
        'global_overview': '🌍 Global Overview',
        'total_doses': 'Total Doses',
        'people_vaccinated': 'People Vaccinated',
        'fully_vaccinated': 'Fully Vaccinated',
        'global_coverage': 'Global Coverage',
        
        # Country Analysis
        'country_analysis': '📊 Country Analysis',
        'select_countries': 'Select countries to compare:',
        'vaccination_trends': '📈 Vaccination Trends',
        'daily_vaccinations': 'Daily Vaccinations',
        'cumulative_progress': 'Cumulative Progress',
        'population_coverage': 'Population Coverage',
        'tab_daily': 'Daily Vaccinations',
        'tab_cumulative': 'Cumulative Progress',
        'tab_coverage': 'Population Coverage',
        
        # Charts
        'daily_vax_chart': 'Daily Vaccinations (7-day average)',
        'cumulative_vax_chart': 'Cumulative Vaccination Doses',
        'pct_vax_chart': 'Percentage of Population Vaccinated',
        
        # Impact Analysis
        'impact_analysis': '📉 Impact Analysis: Vaccines vs. Deaths',
        'impact_description': 'Visualizing the correlation between rising vaccination rates and falling death rates.',
        'select_impact_country': 'Select country for impact analysis:',
        'insight_impact': '💡 **Insight:** Observe how the red line (deaths) tends to flatten or decline as the blue line (vaccinations) rises.',
        'calc_deaths': 'Calculated deaths per million from raw data.',
        'no_overlap': 'No overlapping data available for {country}. The vaccination data and death data may not cover the same time period.',
        
        # Forecast
        'forecast_title': '🔮 Vaccination Forecast',
        'select_forecast_country': 'Select a country for 30-day forecast:',
        'generate_forecast': 'Generate Forecast',
        'forecast_period': 'Forecast Period',
        'avg_daily_forecast': 'Avg. Daily Forecast',
        'total_expected': 'Total Expected',
        'forecast_days': '30 days',
        'forecast_doses': 'doses',
        'insufficient_data': 'Insufficient data for {country}. Need at least 30 days of history.',
        'select_one_country': '👆 Please select at least one country to view visualizations',
        
        # Map
        'global_map': '🗺️ Global Vaccination Map',
        'top_performers': '🏆 Top Performing Countries',
        'no_data_latest': 'No data available for the latest date.',
        
        # Chatbot
        'chatbot_subtitle': 'Your smart companion for COVID-19 information',
        'chatbot_help_title': 'How can I help?',
        'chatbot_help_desc': """
        I can answer questions about:
        - 💉 **Vaccines** (safety, side effects, boosters)
        - 🦠 **Variants** (Omicron, Delta)
        - 🩺 **Symptoms** & Testing
        - 😷 **Safety Guidelines** (masks, isolation)
        - 🤰 **Special Groups** (children, pregnancy)
        """,
        'chatbot_placeholder': 'Type your question here...',
        'chatbot_thinking': 'Thinking...',
        'chatbot_welcome': 'Hello! 👋 I am your COVID-19 Health Assistant. How can I help you today?',
        
        # Symptom Checker
        'symptom_checker_title': '🩺 COVID-19 Symptom Self-Assessment',
        'medical_disclaimer_title': '⚠️ MEDICAL DISCLAIMER',
        'medical_disclaimer_text': 'This is NOT a diagnostic tool and does not replace professional medical advice, diagnosis, or treatment. If you have symptoms, please consult a healthcare provider and get tested for COVID-19.',
        'symptom_intro': 'This assessment is based on symptoms recognized by the **WHO** and **CDC**. It helps you understand if you should get tested, but it cannot confirm or rule out COVID-19.',
        'check_symptoms': '📋 Check Your Symptoms',
        'primary_symptoms': 'Primary Symptoms:',
        'other_symptoms': 'Other Symptoms:',
        'assess_risk': '🔍 Assess Risk',
        
        # Symptoms
        'sym_fever': '🌡️ Fever (>100.4°F / 38°C)',
        'sym_cough': '🤧 New continuous cough',
        'sym_breathing': '😮‍💨 Difficulty breathing / shortness of breath',
        'sym_taste_smell': '👃 Loss of taste or smell',
        'sym_fatigue': '😴 Unusual tiredness / fatigue',
        'sym_body_aches': '💪 Muscle or body aches',
        'sym_sore_throat': '🗣️ Sore throat',
        'sym_headache': '🤕 Headache',
        'sym_congestion': '🤧 Nasal congestion or runny nose',
        'sym_nausea': '🤢 Nausea or vomiting',
        'sym_diarrhea': '🚽 Diarrhea',
        
        # Questions
        'q_exposure': 'Have you been in close contact with someone who tested positive for COVID-19?',
        'q_vaccination': 'Vaccination Status:',
        'ans_no': 'No',
        'ans_yes_14': 'Yes, within last 14 days',
        'ans_unsure': 'Unsure',
        'vax_unvaccinated': 'Unvaccinated',
        'vax_partially': 'Partially Vaccinated',
        'vax_fully': 'Fully Vaccinated',
        'vax_boosted': 'Boosted',
        
        # Risk Assessment
        'high_risk_title': '🚨 HIGH RISK ASSESSMENT',
        'high_risk_text': """
        Based on your symptoms, you may have COVID-19. Please take the following steps:
        
        **Immediate Actions:**
        1. ✅ **Get tested immediately**
        2. 🏠 **Self-isolate**
        3. 😷 **Wear a mask**
        4. 📞 **Contact your healthcare provider**
        """,
        'moderate_risk_title': '⚠️ MODERATE RISK ASSESSMENT',
        'moderate_risk_text': """
        You have some symptoms that could indicate COVID-19.
        
        **Recommended Actions:**
        1. ✅ **Get tested**
        2. 🏠 **Stay home**
        3. 😷 **Wear a mask**
        4. 👁️ **Monitor symptoms**
        """,
        'low_risk_title': '✅ LOW RISK ASSESSMENT',
        'low_risk_text': """
        Based on your responses, you currently have a low risk for COVID-19.
        
        **Continue Preventive Measures:**
        - 💉 Stay up-to-date with vaccinations
        - 😷 Wear masks in crowded indoor spaces
        - 👐 Wash hands frequently
        """,
        
        # Buttons & Misc
        'refresh_data': '🔄 Refresh Data',
        'refresh_success': 'Data updated successfully!',
        'download_pdf': '📥 Download PDF Report',
        'pdf_help': 'Download a detailed PDF report of your symptom assessment',
        'pdf_info': '💡 **This report can be shared with your healthcare provider for better consultation.**',
        'find_testing': '🔬 Find COVID-19 Testing Locations',
        'testing_tip': '💡 **Tip:** Many pharmacies and clinics offer rapid testing.',
        
        # Footer
        'data_source': 'Data source',
        'built_with': 'Built with ❤️ using Streamlit • Prophet • Plotly',
        'about_title': 'About',
        'about_text': """
        This dashboard tracks global COVID-19 vaccination progress using data from 
        [Our World in Data](https://ourworldindata.org/).
        
        **Features:**
        - 📊 Interactive visualizations
        - 🌍 Global vaccination map
        - 📈 30-day forecasts
        - 🔄 Daily data updates
        - 🤖 AI Health Assistant
        """,
        'data_info': '📅 Data Info',
        'last_updated': 'Last Updated',
        'countries_count': 'Countries',
        'total_records': 'Total Records',
    },
    
    'hi': {
        'page_title': 'COVID-19 टीकाकरण ट्रैकर',
        'chatbot_title': '🤖 AI स्वास्थ्य सहायक',
        'dashboard_title': '💉 COVID-19 टीकाकरण ट्रैकर',
        'dashboard_subtitle': 'वास्तविक समय में वैश्विक टीकाकरण निगरानी और पूर्वानुमान',
        'nav_title': '📍 नेविगेशन',
        'nav_dashboard': 'डैशबोर्ड',
        'nav_chatbot': 'AI स्वास्थ्य सहायक',
        'nav_settings': '⚙️ सेटिंग्स',
        'nav_about': 'हमारे बारे में',
        'nav_go_to': 'पर जाएं:',
        'nav_simulator': 'महामारी सिम्युलेटर',
        'nav_comparison': 'देश मुकाबला',
        'global_overview': '🌍 वैश्विक अवलोकन',
        'total_doses': 'कुल खुराक',
        'people_vaccinated': 'टीकाकृत लोग',
        'fully_vaccinated': 'पूर्ण टीकाकृत',
        'global_coverage': 'वैश्विक कवरेज',
        'country_analysis': '📊 देश विश्लेषण',
        'select_countries': 'तुलना के लिए देश चुनें:',
        'vaccination_trends': '📈 टीकाकरण रुझान',
        'daily_vaccinations': 'दैनिक टीकाकरण',
        'cumulative_progress': 'संचयी प्रगति',
        'population_coverage': 'जनसंख्या कवरेज',
        'tab_daily': 'दैनिक टीकाकरण',
        'tab_cumulative': 'संचयी प्रगति',
        'tab_coverage': 'जनसंख्या कवरेज',
        'daily_vax_chart': 'दैनिक टीकाकरण (7-दिन औसत)',
        'cumulative_vax_chart': 'संचयी टीकाकरण खुराक',
        'pct_vax_chart': 'टीकाकृत जनसंख्या का प्रतिशत',
        'impact_analysis': '📉 प्रभाव विश्लेषण: टीके बनाम मृत्यु',
        'impact_description': 'टीकाकरण दर में वृद्धि और मृत्यु दर में कमी के बीच संबंध।',
        'select_impact_country': 'प्रभाव विश्लेषण के लिए देश चुनें:',
        'insight_impact': '💡 **अंतर्दृष्टि:** देखें कि टीकाकरण (नीली रेखा) बढ़ने पर मृत्यु (लाल रेखा) कैसे कम होती है।',
        'calc_deaths': 'कच्चे डेटा से प्रति मिलियन मृत्यु की गणना की गई।',
        'no_overlap': '{country} के लिए कोई ओवरलैपिंग डेटा उपलब्ध नहीं है।',
        'forecast_title': '🔮 टीकाकरण पूर्वानुमान',
        'select_forecast_country': '30-दिन के पूर्वानुमान के लिए देश चुनें:',
        'generate_forecast': 'पूर्वानुमान बनाएं',
        'forecast_period': 'पूर्वानुमान अवधि',
        'avg_daily_forecast': 'औसत दैनिक पूर्वानुमान',
        'total_expected': 'कुल अपेक्षित',
        'forecast_days': '30 दिन',
        'forecast_doses': 'खुराक',
        'insufficient_data': '{country} के लिए अपर्याप्त डेटा। कम से कम 30 दिनों का इतिहास चाहिए।',
        'select_one_country': '👆 विज़ुअलाइज़ेशन देखने के लिए कृपया कम से कम एक देश चुनें',
        'global_map': '🗺️ वैश्विक टीकाकरण मानचित्र',
        'top_performers': '🏆 शीर्ष प्रदर्शन करने वाले देश',
        'no_data_latest': 'नवीनतम तिथि के लिए कोई डेटा उपलब्ध नहीं है।',
        'chatbot_subtitle': 'COVID-19 जानकारी के लिए आपका स्मार्ट साथी',
        'chatbot_help_title': 'मैं कैसे मदद कर सकता हूं?',
        'chatbot_help_desc': """
        मैं इनके बारे में सवालों के जवाब दे सकता हूं:
        - 💉 **टीके** (सुरक्षा, दुष्प्रभाव, बूस्टर)
        - 🦠 **वेरिएंट** (ओमिक्रोन, डेल्टा)
        - 🩺 **लक्षण** और परीक्षण
        - 😷 **सुरक्षा दिशानिर्देश** (मास्क, अलगाव)
        - 🤰 **विशेष समूह** (बच्चे, गर्भावस्था)
        """,
        'chatbot_placeholder': 'अपना प्रश्न यहां टाइप करें...',
        'chatbot_thinking': 'सोच रहा हूं...',
        'chatbot_welcome': 'नमस्ते! 👋 मैं आपका COVID-19 स्वास्थ्य सहायक हूं। आज मैं आपकी कैसे मदद कर सकता हूं?',
        'symptom_checker_title': '🩺 COVID-19 लक्षण स्व-मूल्यांकन',
        'medical_disclaimer_title': '⚠️ चिकित्सा अस्वीकरण',
        'medical_disclaimer_text': 'यह कोई निदान उपकरण नहीं है और पेशेवर चिकित्सा सलाह का विकल्प नहीं है। यदि आपको लक्षण हैं, तो कृपया डॉक्टर से सलाह लें।',
        'symptom_intro': 'यह मूल्यांकन WHO और CDC द्वारा मान्यता प्राप्त लक्षणों पर आधारित है।',
        'check_symptoms': '📋 अपने लक्षणों की जांच करें',
        'primary_symptoms': 'प्राथमिक लक्षण:',
        'other_symptoms': 'अन्य लक्षण:',
        'assess_risk': '🔍 जोखिम का आकलन करें',
        'sym_fever': '🌡️ बुखार (>100.4°F / 38°C)',
        'sym_cough': '🤧 नई लगातार खांसी',
        'sym_breathing': '😮‍💨 सांस लेने में कठिनाई',
        'sym_taste_smell': '👃 स्वाद या गंध की हानि',
        'sym_fatigue': '😴 असामान्य थकान',
        'sym_body_aches': '💪 मांसपेशियों या शरीर में दर्द',
        'sym_sore_throat': '🗣️ गले में खराश',
        'sym_headache': '🤕 सिरदर्द',
        'sym_congestion': '🤧 नाक बंद या बह रही है',
        'sym_nausea': '🤢 मतली या उल्टी',
        'sym_diarrhea': '🚽 दस्त',
        'q_exposure': 'क्या आप पिछले 14 दिनों में किसी COVID-19 पॉजिटिव व्यक्ति के संपर्क में आए हैं?',
        'q_vaccination': 'टीकाकरण स्थिति:',
        'ans_no': 'नहीं',
        'ans_yes_14': 'हां, पिछले 14 दिनों में',
        'ans_unsure': 'अनिश्चित',
        'vax_unvaccinated': 'टीकाकरण नहीं हुआ',
        'vax_partially': 'आंशिक रूप से टीकाकृत',
        'vax_fully': 'पूर्ण टीकाकृत',
        'vax_boosted': 'बूस्टर खुराक ली',
        'high_risk_title': '🚨 उच्च जोखिम मूल्यांकन',
        'high_risk_text': """
        आपके लक्षणों के आधार पर, आपको COVID-19 हो सकता है।
        
        **तत्काल कार्रवाई:**
        1. ✅ **तुरंत परीक्षण कराएं**
        2. 🏠 **स्व-पृथक (Self-isolate) करें**
        3. 😷 **मास्क पहनें**
        4. 📞 **डॉक्टर से संपर्क करें**
        """,
        'moderate_risk_title': '⚠️ मध्यम जोखिम मूल्यांकन',
        'moderate_risk_text': """
        आपमें कुछ लक्षण हैं जो COVID-19 का संकेत दे सकते हैं।
        
        **अनुशंसित कार्रवाई:**
        1. ✅ **परीक्षण कराएं**
        2. 🏠 **घर पर रहें**
        3. 😷 **मास्क पहनें**
        4. 👁️ **लक्षणों की निगरानी करें**
        """,
        'low_risk_title': '✅ कम जोखिम मूल्यांकन',
        'low_risk_text': """
        आपकी प्रतिक्रियाओं के आधार पर, वर्तमान में COVID-19 का जोखिम कम है।
        
        **निवारक उपाय जारी रखें:**
        - 💉 टीकाकरण अपडेट रखें
        - 😷 भीड़भाड़ वाली जगहों पर मास्क पहनें
        - 👐 बार-बार हाथ धोएं
        """,
        'refresh_data': '🔄 डेटा रीफ्रेश करें',
        'refresh_success': 'डेटा सफलतापूर्वक अपडेट किया गया!',
        'download_pdf': '📥 PDF रिपोर्ट डाउनलोड करें',
        'pdf_help': 'अपने लक्षण मूल्यांकन की विस्तृत PDF रिपोर्ट डाउनलोड करें',
        'pdf_info': '💡 **यह रिपोर्ट बेहतर परामर्श के लिए आपके डॉक्टर के साथ साझा की जा सकती है।**',
        'find_testing': '🔬 COVID-19 परीक्षण केंद्र खोजें',
        'testing_tip': '💡 **सुझाव:** कई फार्मेसी और क्लीनिक रैपिड टेस्टिंग की सुविधा देते हैं।',
        'data_source': 'डेटा स्रोत',
        'built_with': 'Streamlit • Prophet • Plotly के साथ ❤️ से बनाया गया',
        'about_title': 'हमारे बारे में',
        'about_text': """
        यह डैशबोर्ड [Our World in Data](https://ourworldindata.org/) के डेटा का उपयोग करके 
        वैश्विक COVID-19 टीकाकरण प्रगति को ट्रैक करता है।
        """,
        'data_info': '📅 डेटा जानकारी',
        'last_updated': 'अंतिम अपडेट',
        'countries_count': 'देश',
        'total_records': 'कुल रिकॉर्ड',
    },

    'bn': {
        'page_title': 'COVID-19 ভ্যাকসিন ট্র্যাকার',
        'chatbot_title': '🤖 AI স্বাস্থ্য সহায়ক',
        'dashboard_title': '💉 COVID-19 ভ্যাকসিন ট্র্যাকার',
        'dashboard_subtitle': 'রিয়েল-টাইম গ্লোবাল ভ্যাকসিনেশন মনিটরিং এবং পূর্বাভাস',
        'nav_title': '📍 নেভিগেশন',
        'nav_dashboard': 'ড্যাশবোর্ড',
        'nav_chatbot': 'AI স্বাস্থ্য সহায়ক',
        'nav_settings': '⚙️ সেটিংস',
        'nav_about': 'আমাদের সম্পর্কে',
        'nav_go_to': 'এখানে যান:',
        'nav_simulator': 'মহামারী সিমুলেটর',
        'nav_comparison': 'দেশ মুখোমুখি',
        'global_overview': '🌍 বৈশ্বিক সংক্ষিপ্ত বিবরণ',
        'total_doses': 'মোট ডোজ',
        'people_vaccinated': 'টিকা প্রাপ্ত মানুষ',
        'fully_vaccinated': 'সম্পূর্ণ টিকা প্রাপ্ত',
        'global_coverage': 'বৈশ্বিক কভারেজ',
        'country_analysis': '📊 দেশ বিশ্লেষণ',
        'select_countries': 'তুলনার জন্য দেশ নির্বাচন করুন:',
        'vaccination_trends': '📈 টিকাদানের প্রবণতা',
        'daily_vaccinations': 'দৈনিক টিকাদান',
        'cumulative_progress': 'ক্রমপুঞ্জিত অগ্রগতি',
        'population_coverage': 'জনসংখ্যা কভারেজ',
        'tab_daily': 'দৈনিক টিকাদান',
        'tab_cumulative': 'ক্রমপুঞ্জিত অগ্রগতি',
        'tab_coverage': 'জনসংখ্যা কভারেজ',
        'daily_vax_chart': 'দৈনিক টিকাদান (৭-দিনের গড়)',
        'cumulative_vax_chart': 'ক্রমপুঞ্জিত টিকার ডোজ',
        'pct_vax_chart': 'টিকা প্রাপ্ত জনসংখ্যার শতাংশ',
        'impact_analysis': '📉 প্রভাব বিশ্লেষণ: টিকা বনাম মৃত্যু',
        'impact_description': 'টিকাদানের হার বৃদ্ধি এবং মৃত্যুর হার হ্রাসের মধ্যে সম্পর্ক।',
        'select_impact_country': 'প্রভাব বিশ্লেষণের জন্য দেশ নির্বাচন করুন:',
        'insight_impact': '💡 **অন্তর্দৃষ্টি:** লক্ষ্য করুন কিভাবে টিকা (নীল রেখা) বাড়লে মৃত্যু (লাল রেখা) কমে যায়।',
        'calc_deaths': 'কাঁচা ডেটা থেকে প্রতি মিলিয়নে মৃত্যু গণনা করা হয়েছে।',
        'no_overlap': '{country}-এর জন্য কোনো ওভারল্যাপিং ডেটা নেই।',
        'forecast_title': '🔮 টিকাদানের পূর্বাভাস',
        'select_forecast_country': '৩০-দিনের পূর্বাভাসের জন্য দেশ নির্বাচন করুন:',
        'generate_forecast': 'পূর্বাভাস তৈরি করুন',
        'forecast_period': 'পূর্বাভাস সময়কাল',
        'avg_daily_forecast': 'গড় দৈনিক পূর্বাভাস',
        'total_expected': 'মোট প্রত্যাশিত',
        'forecast_days': '৩০ দিন',
        'forecast_doses': 'ডোজ',
        'insufficient_data': '{country}-এর জন্য অপর্যাপ্ত ডেটা। অন্তত ৩০ দিনের ইতিহাস প্রয়োজন।',
        'select_one_country': '👆 ভিজ্যুয়ালাইজেশন দেখতে অনুগ্রহ করে অন্তত একটি দেশ নির্বাচন করুন',
        'global_map': '🗺️ বৈশ্বিক টিকাদান মানচিত্র',
        'top_performers': '🏆 শীর্ষ পারফর্ম করা দেশ',
        'no_data_latest': 'সর্বশেষ তারিখের জন্য কোনো ডেটা উপলব্ধ নেই।',
        'chatbot_subtitle': 'COVID-19 তথ্যের জন্য আপনার স্মার্ট সঙ্গী',
        'chatbot_help_title': 'আমি কীভাবে সাহায্য করতে পারি?',
        'chatbot_help_desc': """
        আমি এই বিষয়গুলো সম্পর্কে প্রশ্নের উত্তর দিতে পারি:
        - 💉 **টিকা** (নিরাপত্তা, পার্শ্ব প্রতিক্রিয়া, বুস্টার)
        - 🦠 **ভেরিয়েন্ট** (ওমিক্রন, ডেল্টা)
        - 🩺 **লক্ষণ** এবং পরীক্ষা
        - 😷 **নিরাপত্তা নির্দেশিকা** (মাস্ক, আইসোলেশন)
        - 🤰 **বিশেষ গ্রুপ** (শিশু, গর্ভাবস্থা)
        """,
        'chatbot_placeholder': 'আপনার প্রশ্ন এখানে টাইপ করুন...',
        'chatbot_thinking': 'ভাবছি...',
        'chatbot_welcome': 'হ্যালো! 👋 আমি আপনার COVID-19 স্বাস্থ্য সহায়ক। আজ আমি আপনাকে কীভাবে সাহায্য করতে পারি?',
        'symptom_checker_title': '🩺 COVID-19 লক্ষণ স্ব-মূল্যায়ন',
        'medical_disclaimer_title': '⚠️ চিকিৎসা দাবিত্যাগ',
        'medical_disclaimer_text': 'এটি কোনো ডায়াগনস্টিক টুল নয় এবং পেশাদার চিকিৎসা পরামর্শের বিকল্প নয়। যদি আপনার লক্ষণ থাকে, তবে অনুগ্রহ করে ডাক্তারের পরামর্শ নিন।',
        'symptom_intro': 'এই মূল্যায়নটি WHO এবং CDC দ্বারা স্বীকৃত লক্ষণগুলির উপর ভিত্তি করে।',
        'check_symptoms': '📋 আপনার লক্ষণগুলি পরীক্ষা করুন',
        'primary_symptoms': 'প্রাথমিক লক্ষণ:',
        'other_symptoms': 'অন্যান্য লক্ষণ:',
        'assess_risk': '🔍 ঝুঁকি মূল্যায়ন করুন',
        'sym_fever': '🌡️ জ্বর (>১০০.৪°F / ৩৮°C)',
        'sym_cough': '🤧 নতুন ক্রমাগত কাশি',
        'sym_breathing': '😮‍💨 শ্বাসকষ্ট',
        'sym_taste_smell': '👃 স্বাদ বা গন্ধের ক্ষতি',
        'sym_fatigue': '😴 অস্বাভাবিক ক্লান্তি',
        'sym_body_aches': '💪 পেশী বা শরীরে ব্যথা',
        'sym_sore_throat': '🗣️ গলা ব্যথা',
        'sym_headache': '🤕 মাথাব্যথা',
        'sym_congestion': '🤧 নাক বন্ধ বা সর্দি',
        'sym_nausea': '🤢 বমি বমি ভাব বা বমি',
        'sym_diarrhea': '🚽 ডায়রিয়া',
        'q_exposure': 'আপনি কি গত ১৪ দিনে কোনো COVID-19 পজিটিভ ব্যক্তির সংস্পর্শে এসেছেন?',
        'q_vaccination': 'টিকাদানের অবস্থা:',
        'ans_no': 'না',
        'ans_yes_14': 'হ্যাঁ, গত ১৪ দিনের মধ্যে',
        'ans_unsure': 'নিশ্চিত নই',
        'vax_unvaccinated': 'টিকা দেওয়া হয়নি',
        'vax_partially': 'আংশিকভাবে টিকা দেওয়া হয়েছে',
        'vax_fully': 'সম্পূর্ণ টিকা দেওয়া হয়েছে',
        'vax_boosted': 'বুস্টার ডোজ নেওয়া হয়েছে',
        'high_risk_title': '🚨 উচ্চ ঝুঁকি মূল্যায়ন',
        'high_risk_text': """
        আপনার লক্ষণের উপর ভিত্তি করে, আপনার COVID-19 হতে পারে।
        
        **তাৎক্ষণিক পদক্ষেপ:**
        1. ✅ **অবিলম্বে পরীক্ষা করান**
        2. 🏠 **সেলফ-আইসোলেট করুন**
        3. 😷 **মাস্ক পরুন**
        4. 📞 **ডাক্তারের সাথে যোগাযোগ করুন**
        """,
        'moderate_risk_title': '⚠️ মাঝারি ঝুঁকি মূল্যায়ন',
        'moderate_risk_text': """
        আপনার কিছু লক্ষণ আছে যা COVID-19 নির্দেশ করতে পারে।
        
        **সুপারিশকৃত পদক্ষেপ:**
        1. ✅ **পরীক্ষা করান**
        2. 🏠 **বাড়িতে থাকুন**
        3. 😷 **মাস্ক পরুন**
        4. 👁️ **লক্ষণগুলি পর্যবেক্ষণ করুন**
        """,
        'low_risk_title': '✅ কম ঝুঁকি মূল্যায়ন',
        'low_risk_text': """
        আপনার উত্তরের উপর ভিত্তি করে, বর্তমানে COVID-19 এর ঝুঁকি কম।
        
        **প্রতিরোধমূলক ব্যবস্থা চালিয়ে যান:**
        - 💉 টিকা আপডেট রাখুন
        - 😷 ভিড়যুক্ত স্থানে মাস্ক পরুন
        - 👐 ঘন ঘন হাত ধোন
        """,
        'refresh_data': '🔄 ডেটা রিফ্রেশ করুন',
        'refresh_success': 'ডেটা সফলভাবে আপডেট করা হয়েছে!',
        'download_pdf': '📥 PDF রিপোর্ট ডাউনলোড করুন',
        'pdf_help': 'আপনার লক্ষণ মূল্যায়নের বিস্তারিত PDF রিপোর্ট ডাউনলোড করুন',
        'pdf_info': '💡 **এই রিপোর্টটি ভালো পরামর্শের জন্য আপনার ডাক্তারের সাথে শেয়ার করা যেতে পারে।**',
        'find_testing': '🔬 COVID-19 পরীক্ষা কেন্দ্র খুঁজুন',
        'testing_tip': '💡 **টিপ:** অনেক ফার্মেসি এবং ক্লিনিক র‍্যাপিড টেস্টিং সুবিধা দেয়।',
        'data_source': 'ডেটা উৎস',
        'built_with': 'Streamlit • Prophet • Plotly দিয়ে ❤️ তৈরি',
        'about_title': 'আমাদের সম্পর্কে',
        'about_text': """
        এই ড্যাশবোর্ড [Our World in Data](https://ourworldindata.org/) থেকে ডেটা ব্যবহার করে 
        বৈশ্বিক COVID-19 টিকাদান অগ্রগতি ট্র্যাক করে।
        """,
        'data_info': '📅 ডেটা তথ্য',
        'last_updated': 'সর্বশেষ আপডেট',
        'countries_count': 'দেশ',
        'total_records': 'মোট রেকর্ড',
    },

    'ta': {
        'page_title': 'COVID-19 தடுப்பூசி டிராக்கர்',
        'chatbot_title': '🤖 AI சுகாதார உதவியாளர்',
        'dashboard_title': '💉 COVID-19 தடுப்பூசி டிராக்கர்',
        'dashboard_subtitle': 'நிகழ்நேர உலகளாவிய தடுப்பூசி கண்காணிப்பு மற்றும் முன்னறிவிப்பு',
        'nav_title': '📍 வழிசெலுத்தல்',
        'nav_dashboard': 'டாஷ்போர்டு',
        'nav_chatbot': 'AI சுகாதார உதவியாளர்',
        'nav_settings': '⚙️ அமைப்புகள்',
        'nav_about': 'பற்றி',
        'nav_go_to': 'செல்லவும்:',
        'nav_simulator': 'தொற்றுநோய் சிமுலேட்டர்',
        'nav_comparison': 'நாடு முகப்பு',
        'global_overview': '🌍 உலகளாவிய கண்ணோட்டம்',
        'total_doses': 'மொத்த டோஸ்கள்',
        'people_vaccinated': 'தடுப்பூசி போடப்பட்டவர்கள்',
        'fully_vaccinated': 'முழுமையாக தடுப்பூசி போடப்பட்டவர்கள்',
        'global_coverage': 'உலகளாவிய கவரேஜ்',
        'country_analysis': '📊 நாடு பகுப்பாய்வு',
        'select_countries': 'ஒப்பிடுவதற்கு நாடுகளைத் தேர்ந்தெடுக்கவும்:',
        'vaccination_trends': '📈 தடுப்பூசி போக்குகள்',
        'daily_vaccinations': 'தினசரி தடுப்பூசிகள்',
        'cumulative_progress': 'ஒட்டுமொத்த முன்னேற்றம்',
        'population_coverage': 'மக்கள் தொகை கவரேஜ்',
        'tab_daily': 'தினசரி தடுப்பூசிகள்',
        'tab_cumulative': 'ஒட்டுமொத்த முன்னேற்றம்',
        'tab_coverage': 'மக்கள் தொகை கவரேஜ்',
        'daily_vax_chart': 'தினசரி தடுப்பூசிகள் (7-நாள் சராசரி)',
        'cumulative_vax_chart': 'ஒட்டுமொத்த தடுப்பூசி டோஸ்கள்',
        'pct_vax_chart': 'தடுப்பூசி போடப்பட்ட மக்கள் தொகை சதவீதம்',
        'impact_analysis': '📉 தாக்கம் பகுப்பாய்வு: தடுப்பூசிகள் vs இறப்புகள்',
        'impact_description': 'தடுப்பூசி விகிதங்கள் அதிகரிப்பதற்கும் இறப்பு விகிதங்கள் குறைவதற்கும் உள்ள தொடர்பைக் காணுதல்.',
        'select_impact_country': 'தாக்கம் பகுப்பாய்விற்கு நாட்டைத் தேர்ந்தெடுக்கவும்:',
        'insight_impact': '💡 **உண்ணோட்டம்:** தடுப்பூசி (நீலக் கோடு) அதிகரிக்கும் போது இறப்புகள் (சிவப்புக் கோடு) எவ்வாறு குறைகின்றன என்பதைக் கவனியுங்கள்.',
        'calc_deaths': 'மூலத் தரவிலிருந்து ஒரு மில்லியனுக்கு இறப்புகள் கணக்கிடப்பட்டன.',
        'no_overlap': '{country}-க்கு ஒன்றுடன் ஒன்று தரவு இல்லை.',
        'forecast_title': '🔮 தடுப்பூசி முன்னறிவிப்பு',
        'select_forecast_country': '30-நாள் முன்னறிவிப்புக்கு நாட்டைத் தேர்ந்தெடுக்கவும்:',
        'generate_forecast': 'முன்னறிவிப்பை உருவாக்கு',
        'forecast_period': 'முன்னறிவிப்பு காலம்',
        'avg_daily_forecast': 'சராசரி தினசரி முன்னறிவிப்பு',
        'total_expected': 'மொத்த எதிர்பார்க்கப்படும்',
        'forecast_days': '30 நாட்கள்',
        'forecast_doses': 'டோஸ்கள்',
        'insufficient_data': '{country}-க்கு போதுமான தரவு இல்லை. குறைந்தது 30 நாட்கள் வரலாறு தேவை.',
        'select_one_country': '👆 காட்சிப்படுத்தல்களைக் காண குறைந்தது ஒரு நாட்டையாவது தேர்ந்தெடுக்கவும்',
        'global_map': '🗺️ உலகளாவிய தடுப்பூசி வரைபடம்',
        'top_performers': '🏆 சிறப்பாக செயல்படும் நாடுகள்',
        'no_data_latest': 'சமீபத்திய தேதிக்கு தரவு இல்லை.',
        'chatbot_subtitle': 'COVID-19 தகவலுக்கான உங்கள் ஸ்மார்ட் துணை',
        'chatbot_help_title': 'நான் எப்படி உதவ முடியும்?',
        'chatbot_help_desc': """
        நான் இவற்றைப் பற்றிய கேள்விகளுக்கு பதிலளிக்க முடியும்:
        - 💉 **தடுப்பூசிகள்** (பாதுகாப்பு, பக்க விளைவுகள், பூஸ்டர்கள்)
        - 🦠 **மாறுபாடுகள்** (ஓமிக்ரான், டெல்டா)
        - 🩺 **அறிகுறிகள்** மற்றும் சோதனை
        - 😷 **பாதுகாப்பு வழிகாட்டுதல்கள்** (முகமூடிகள், தனிமைப்படுத்தல்)
        - 🤰 **சிறப்பு குழுக்கள்** (குழந்தைகள், கர்ப்பம்)
        """,
        'chatbot_placeholder': 'உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யவும்...',
        'chatbot_thinking': 'யோசிக்கிறேன்...',
        'chatbot_welcome': 'வணக்கம்! 👋 நான் உங்கள் COVID-19 சுகாதார உதவியாளர். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?',
        'symptom_checker_title': '🩺 COVID-19 அறிகுறி சுய மதிப்பீடு',
        'medical_disclaimer_title': '⚠️ மருத்துவ மறுப்பு',
        'medical_disclaimer_text': 'இது ஒரு நோயறிதல் கருவி அல்ல மற்றும் தொழில்முறை மருத்துவ ஆலோசனைக்கு மாற்றாக இல்லை. உங்களுக்கு அறிகுறிகள் இருந்தால், மருத்துவரை அணுகவும்.',
        'symptom_intro': 'இந்த மதிப்பீடு WHO மற்றும் CDC அங்கீகரித்த அறிகுறிகளை அடிப்படையாகக் கொண்டது.',
        'check_symptoms': '📋 உங்கள் அறிகுறிகளைச் சரிபார்க்கவும்',
        'primary_symptoms': 'முதன்மை அறிகுறிகள்:',
        'other_symptoms': 'பிற அறிகுறிகள்:',
        'assess_risk': '🔍 ஆபத்தை மதிப்பிடுங்கள்',
        'sym_fever': '🌡️ காய்ச்சல் (>100.4°F / 38°C)',
        'sym_cough': '🤧 புதிய தொடர் இருமல்',
        'sym_breathing': '😮‍💨 மூச்சுத் திணறல்',
        'sym_taste_smell': '👃 சுவை அல்லது வாசனை இழப்பு',
        'sym_fatigue': '😴 அசாதாரண சோர்வு',
        'sym_body_aches': '💪 தசை அல்லது உடல் வலி',
        'sym_sore_throat': '🗣️ தொண்டை வலி',
        'sym_headache': '🤕 தலைவலி',
        'sym_congestion': '🤧 மூக்கு ஒழுகுதல்',
        'sym_nausea': '🤢 குமட்டல் அல்லது வாந்தி',
        'sym_diarrhea': '🚽 வயிற்றுப்போக்கு',
        'q_exposure': 'கடந்த 14 நாட்களில் COVID-19 பாசிட்டிவ் நபருடன் தொடர்பில் இருந்தீர்களா?',
        'q_vaccination': 'தடுப்பூசி நிலை:',
        'ans_no': 'இல்லை',
        'ans_yes_14': 'ஆம், கடந்த 14 நாட்களில்',
        'ans_unsure': 'நிச்சயமில்லை',
        'vax_unvaccinated': 'தடுப்பூசி போடப்படவில்லை',
        'vax_partially': 'பகுதி தடுப்பூசி போடப்பட்டது',
        'vax_fully': 'முழுமையாக தடுப்பூசி போடப்பட்டது',
        'vax_boosted': 'பூஸ்டர் போடப்பட்டது',
        'high_risk_title': '🚨 அதிக ஆபத்து மதிப்பீடு',
        'high_risk_text': """
        உங்கள் அறிகுறிகளின் அடிப்படையில், உங்களுக்கு COVID-19 இருக்கலாம்.
        
        **உடனடி நடவடிக்கைகள்:**
        1. ✅ **உடனடியாக சோதனை செய்யுங்கள்**
        2. 🏠 **தனிமைப்படுத்திக் கொள்ளுங்கள்**
        3. 😷 **முகமூடி அணியுங்கள்**
        4. 📞 **மருத்துவரைத் தொடர்பு கொள்ளுங்கள்**
        """,
        'moderate_risk_title': '⚠️ மிதமான ஆபத்து மதிப்பீடு',
        'moderate_risk_text': """
        COVID-19 ஐக் குறிக்கும் சில அறிகுறிகள் உங்களிடம் உள்ளன.
        
        **பரிந்துரைக்கப்பட்ட நடவடிக்கைகள்:**
        1. ✅ **சோதனை செய்யுங்கள்**
        2. 🏠 **வீட்டிலேயே இருங்கள்**
        3. 😷 **முகமூடி அணியுங்கள்**
        4. 👁️ **அறிகுறிகளைக் கண்காணிக்கவும்**
        """,
        'low_risk_title': '✅ குறைந்த ஆபத்து மதிப்பீடு',
        'low_risk_text': """
        உங்கள் பதில்களின் அடிப்படையில், தற்போது COVID-19 ஆபத்து குறைவு.
        
        **தடுப்பு நடவடிக்கைகளைத் தொடரவும்:**
        - 💉 தடுப்பூசியைப் புதுப்பித்த நிலையில் வைத்திருங்கள்
        - 😷 கூட்டமான இடங்களில் முகமூடி அணியுங்கள்
        - 👐 அடிக்கடி கைகளை கழுவுங்கள்
        """,
        'refresh_data': '🔄 தரவைப் புதுப்பிக்கவும்',
        'refresh_success': 'தரவு வெற்றிகரமாக புதுப்பிக்கப்பட்டது!',
        'download_pdf': '📥 PDF அறிக்கையைப் பதிவிறக்கவும்',
        'pdf_help': 'உங்கள் அறிகுறி மதிப்பீட்டின் விரிவான PDF அறிக்கையைப் பதிவிறக்கவும்',
        'pdf_info': '💡 **சிறந்த ஆலோசனைக்காக இந்த அறிக்கையை உங்கள் மருத்துவரிடம் பகிரலாம்.**',
        'find_testing': '🔬 COVID-19 சோதனை மையங்களைக் கண்டறியவும்',
        'testing_tip': '💡 **உதவிக்குறிப்பு:** பல மருந்தகங்கள் மற்றும் கிளினிக்குகள் விரைவான சோதனையை வழங்குகின்றன.',
        'data_source': 'தரவு ஆதாரம்',
        'built_with': 'Streamlit • Prophet • Plotly உடன் ❤️ உருவாக்கப்பட்டது',
        'about_title': 'பற்றி',
        'about_text': """
        இந்த டாஷ்போர்டு [Our World in Data](https://ourworldindata.org/) தரவைப் பயன்படுத்தி 
        உலகளாவிய COVID-19 தடுப்பூசி முன்னேற்றத்தைக் கண்காணிக்கிறது.
        """,
        'data_info': '📅 தரவு தகவல்',
        'last_updated': 'கடைசியாக புதுப்பிக்கப்பட்டது',
        'countries_count': 'நாடுகள்',
        'total_records': 'மொத்த பதிவுகள்',
    },

    'te': {
        'page_title': 'COVID-19 వ్యాక్సిన్ ట్రాకర్',
        'chatbot_title': '🤖 AI ఆరోగ్య సహాయకుడు',
        'dashboard_title': '💉 COVID-19 వ్యాక్సిన్ ట్రాకర్',
        'dashboard_subtitle': 'రియల్ టైమ్ గ్లోబల్ వ్యాక్సినేషన్ పర్యవేక్షణ మరియు సూచన',
        'nav_title': '📍 నావిగేషన్',
        'nav_dashboard': 'డ్యాష్‌బోర్డ్',
        'nav_chatbot': 'AI ఆరోగ్య సహాయకుడు',
        'nav_settings': '⚙️ సెట్టింగ్‌లు',
        'nav_about': 'గురించి',
        'nav_go_to': 'వెళ్ళండి:',
        'nav_simulator': 'మహమ్మారి సిమ్యులేటర్',
        'nav_comparison': 'దేశ ముఖాముఖి',
        'global_overview': '🌍 ప్రపంచ అవలోకనం',
        'total_doses': 'మొత్తం మోతాదులు',
        'people_vaccinated': 'టీకా వేసుకున్న ప్రజలు',
        'fully_vaccinated': 'పూర్తిగా టీకా వేసుకున్నవారు',
        'global_coverage': 'ప్రపంచ కవరేజ్',
        'country_analysis': '📊 దేశ విశ్లేషణ',
        'select_countries': 'పోల్చడానికి దేశాలను ఎంచుకోండి:',
        'vaccination_trends': '📈 టీకా పోకడలు',
        'daily_vaccinations': 'రోజువారీ టీకాలు',
        'cumulative_progress': 'సంచిత పురోగతి',
        'population_coverage': 'జనాభా కవరేజ్',
        'tab_daily': 'రోజువారీ టీకాలు',
        'tab_cumulative': 'సంచిత పురోగతి',
        'tab_coverage': 'జనాభా కవరేజ్',
        'daily_vax_chart': 'రోజువారీ టీకాలు (7-రోజుల సగటు)',
        'cumulative_vax_chart': 'సంచిత టీకా మోతాదులు',
        'pct_vax_chart': 'టీకా వేసుకున్న జనాభా శాతం',
        'impact_analysis': '📉 ప్రభావ విశ్లేషణ: టీకాలు vs మరణాలు',
        'impact_description': 'పెరుగుతున్న టీకా రేట్లు మరియు తగ్గుతున్న మరణాల రేట్ల మధ్య సంబంధాన్ని చూడటం.',
        'select_impact_country': 'ప్రభావ విశ్లేషణ కోసం దేశాన్ని ఎంచుకోండి:',
        'insight_impact': '💡 **అంతర్దృష్టి:** టీకా (నీలి రేఖ) పెరిగినప్పుడు మరణాలు (ఎరుపు రేఖ) ఎలా తగ్గుతాయో గమనించండి.',
        'calc_deaths': 'ముడి డేటా నుండి మిలియన్‌కు మరణాలు లెక్కించబడ్డాయి.',
        'no_overlap': '{country} కోసం అతివ్యాప్తి డేటా లేదు.',
        'forecast_title': '🔮 టీకా సూచన',
        'select_forecast_country': '30-రోజుల సూచన కోసం దేశాన్ని ఎంచుకోండి:',
        'generate_forecast': 'సూచనను రూపొందించండి',
        'forecast_period': 'సూచన కాలం',
        'avg_daily_forecast': 'సగటు రోజువారీ సూచన',
        'total_expected': 'మొత్తం ఆశించినది',
        'forecast_days': '30 రోజులు',
        'forecast_doses': 'మోతాదులు',
        'insufficient_data': '{country} కోసం తగినంత డేటా లేదు. కనీసం 30 రోజుల చరిత్ర అవసరం.',
        'select_one_country': '👆 విజువలైజేషన్లను చూడటానికి దయచేసి కనీసం ఒక దేశాన్ని ఎంచుకోండి',
        'global_map': '🗺️ ప్రపంచ టీకా మ్యాప్',
        'top_performers': '🏆 ఉత్తమ పనితీరు కనబరిచిన దేశాలు',
        'no_data_latest': 'తాజా తేదీకి డేటా అందుబాటులో లేదు.',
        'chatbot_subtitle': 'COVID-19 సమాచారం కోసం మీ స్మార్ట్ తోడు',
        'chatbot_help_title': 'నేను ఎలా సహాయం చేయగలను?',
        'chatbot_help_desc': """
        నేను వీటి గురించి ప్రశ్నలకు సమాధానం ఇవ్వగలను:
        - 💉 **టీకాలు** (భద్రత, దుష్ప్రభావాలు, బూస్టర్లు)
        - 🦠 **వేరియంట్లు** (ఓమిక్రాన్, డెల్టా)
        - 🩺 **లక్షణాలు** మరియు పరీక్ష
        - 😷 **భద్రతా మార్గదర్శకాలు** (మాస్క్‌లు, ఐసోలేషన్)
        - 🤰 **ప్రత్యేక సమూహాలు** (పిల్లలు, గర్భం)
        """,
        'chatbot_placeholder': 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...',
        'chatbot_thinking': 'ఆలోచిస్తున్నాను...',
        'chatbot_welcome': 'నమస్తే! 👋 నేను మీ COVID-19 ఆరోగ్య సహాయకుడిని. ఈ రోజు నేను మీకు ఎలా సహాయం చేయగలను?',
        'symptom_checker_title': '🩺 COVID-19 లక్షణ స్వీయ-అంచనా',
        'medical_disclaimer_title': '⚠️ వైద్య నిరాకరణ',
        'medical_disclaimer_text': 'ఇది రోగనిర్ధారణ సాధనం కాదు మరియు వృత్తిపరమైన వైద్య సలహాకు ప్రత్యామ్నాయం కాదు. మీకు లక్షణాలు ఉంటే, దయచేసి వైద్యుడిని సంప్రదించండి.',
        'symptom_intro': 'ఈ అంచనా WHO మరియు CDC గుర్తించిన లక్షణాలపై ఆధారపడి ఉంటుంది.',
        'check_symptoms': '📋 మీ లక్షణాలను తనిఖీ చేయండి',
        'primary_symptoms': 'ప్రాథమిక లక్షణాలు:',
        'other_symptoms': 'ఇతర లక్షణాలు:',
        'assess_risk': '🔍 ప్రమాదాన్ని అంచనా వేయండి',
        'sym_fever': '🌡️ జ్వరం (>100.4°F / 38°C)',
        'sym_cough': '🤧 కొత్త నిరంతర దగ్గు',
        'sym_breathing': '😮‍💨 ఊపిరి ఆడకపోవడం',
        'sym_taste_smell': '👃 రుచి లేదా వాసన కోల్పోవడం',
        'sym_fatigue': '😴 అసాధారణ అలసట',
        'sym_body_aches': '💪 కండరాల లేదా శరీర నొప్పులు',
        'sym_sore_throat': '🗣️ గొంతు నొప్పి',
        'sym_headache': '🤕 తలనొప్పి',
        'sym_congestion': '🤧 ముక్కు దిబ్బడ',
        'sym_nausea': '🤢 వికారం లేదా వాంతులు',
        'sym_diarrhea': '🚽 విరేచనాలు',
        'q_exposure': 'మీరు గత 14 రోజుల్లో COVID-19 పాజిటివ్ వ్యక్తితో సన్నిహితంగా ఉన్నారా?',
        'q_vaccination': 'టీకా స్థితి:',
        'ans_no': 'కాదు',
        'ans_yes_14': 'అవును, గత 14 రోజుల్లో',
        'ans_unsure': 'ఖచ్చితంగా తెలియదు',
        'vax_unvaccinated': 'టీకా వేసుకోలేదు',
        'vax_partially': 'పాక్షికంగా టీకా వేసుకున్నారు',
        'vax_fully': 'పూర్తిగా టీకా వేసుకున్నారు',
        'vax_boosted': 'బూస్టర్ తీసుకున్నారు',
        'high_risk_title': '🚨 అధిక ప్రమాద అంచనా',
        'high_risk_text': """
        మీ లక్షణాల ఆధారంగా, మీకు COVID-19 ఉండవచ్చు.
        
        **తక్షణ చర్యలు:**
        1. ✅ **వెంటనే పరీక్ష చేయించుకోండి**
        2. 🏠 **మిమ్మల్ని మీరు వేరుగా ఉంచుకోండి (Self-isolate)**
        3. 😷 **మాస్క్ ధరించండి**
        4. 📞 **వైద్యుడిని సంప్రదించండి**
        """,
        'moderate_risk_title': '⚠️ మితమైన ప్రమాద అంచనా',
        'moderate_risk_text': """
        COVID-19 ను సూచించే కొన్ని లక్షణాలు మీకు ఉన్నాయి.
        
        **సిఫార్సు చేసిన చర్యలు:**
        1. ✅ **పరీక్ష చేయించుకోండి**
        2. 🏠 **ఇంట్లోనే ఉండండి**
        3. 😷 **మాస్క్ ధరించండి**
        4. 👁️ **లక్షణాలను గమనించండి**
        """,
        'low_risk_title': '✅ తక్కువ ప్రమాద అంచనా',
        'low_risk_text': """
        మీ సమాధానాల ఆధారంగా, ప్రస్తుతం COVID-19 ప్రమాదం తక్కువగా ఉంది.
        
        **నివారణ చర్యలను కొనసాగించండి:**
        - 💉 టీకాలను అప్‌డేట్‌గా ఉంచుకోండి
        - 😷 రద్దీగా ఉండే ప్రదేశాలలో మాస్క్ ధరించండి
        - 👐 తరచుగా చేతులు కడుక్కోండి
        """,
        'refresh_data': '🔄 డేటాను రీఫ్రెష్ చేయండి',
        'refresh_success': 'డేటా విజయవంతంగా నవీకరించబడింది!',
        'download_pdf': '📥 PDF నివేదికను డౌన్‌లోడ్ చేయండి',
        'pdf_help': 'మీ లక్షణ అంచనా యొక్క వివరణాత్మక PDF నివేదికను డౌన్‌లోడ్ చేయండి',
        'pdf_info': '💡 **మెరుగైన సలహా కోసం ఈ నివేదికను మీ వైద్యుడితో పంచుకోవచ్చు.**',
        'find_testing': '🔬 COVID-19 పరీక్షా కేంద్రాలను కనుగొనండి',
        'testing_tip': '💡 **చిట్కా:** అనేక ఫార్మసీలు మరియు క్లినిక్‌లు రాపిడ్ టెస్టింగ్‌ను అందిస్తాయి.',
        'data_source': 'డేటా మూలం',
        'built_with': 'Streamlit • Prophet • Plotly తో ❤️ రూపొందించబడింది',
        'about_title': 'గురించి',
        'about_text': """
        ఈ డ్యాష్‌బోర్డ్ [Our World in Data](https://ourworldindata.org/) నుండి డేటాను ఉపయోగించి 
        ప్రపంచ COVID-19 టీకా పురోగతిని ట్రాక్ చేస్తుంది.
        """,
        'data_info': '📅 డేటా సమాచారం',
        'last_updated': 'చివరిగా నవీకరించబడింది',
        'countries_count': 'దేశాలు',
        'total_records': 'మొత్తం రికార్డులు',
    }
}

def get_text(key, lang='en'):
    """Get translated text for a given key and language"""
    if lang not in UI_TRANSLATIONS:
        lang = 'en'  # Fallback to English
    
    return UI_TRANSLATIONS[lang].get(key, UI_TRANSLATIONS['en'].get(key, key))

def t(key):
    """
    Translation helper function
    Gets text based on current session language
    """
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    return get_text(key, st.session_state.language)
