# 🌟 Project Spotlight: COVID-19 Vaccine Tracker & AI Assistant

**A full-stack data intelligence platform democratizing access to global health data through AI and interactive visualization.**

---

## 💡 The Problem

During the pandemic, data was abundant but scattered. Users faced information overload from disparate sources, complex spreadsheets, and language barriers. There was a critical need for a centralized, accessible, and predictive tool that could answer simple questions like *"Is it safe?"* or *"When will we reach herd immunity?"* in plain language.

## 🛠️ The Solution

I built a comprehensive **Vaccine Tracker & AI Assistant** that goes beyond simple dashboards. It combines **real-time data engineering**, **machine learning forecasting**, and **voice-enabled AI** to provide actionable insights to users regardless of their technical literacy or language.

---

## 🚀 Key Technical Challenges & Solutions

### 1. Handling Real-Time Global Data

**Challenge:** Ingesting and normalizing daily vaccination data from 200+ countries with varying reporting formats and missing values.
**Solution:** Engineered a robust **ETL (Extract, Transform, Load) pipeline** using Python and Pandas.

* **Automated Ingestion:** Scripts fetch raw CSVs from *Our World in Data* daily.
* **Smart Cleaning:** Implemented logic to handle missing dates and interpolate gaps.
* **Optimized Storage:** Processed data is stored in a local **SQLite** database, ensuring sub-second query performance for the dashboard without heavy server overhead.

### 2. Making Data Accessible to All

**Challenge:** Most dashboards are visual-only, excluding visually impaired users or those with low literacy.
**Solution:** Developed a **Voice-First AI Interface**.

* **Voice Input/Output:** Integrated Web Speech API for speech-to-text and `gTTS` for text-to-speech, allowing users to "talk" to the dashboard.
* **Multi-Language Support:** Leveraged Google Translate API to support **5 languages** (English, Hindi, Bengali, Tamil, Telugu), breaking down language barriers for millions of potential users.
* **Contextual NLP:** Built a TF-IDF based search engine that queries medical eBooks to provide accurate, context-aware answers to health questions.

### 3. Predicting the Future

**Challenge:** Historical data shows *what happened*, but users want to know *what will happen*.
**Solution:** Integrated **Facebook Prophet** for time-series forecasting.

* **Trend Analysis:** The model analyzes historical vaccination rates to predict coverage for the next 30 days.
* **Dynamic Visualization:** Forecasts are plotted with confidence intervals, helping users visualize potential "plateaus" or accelerations in vaccination campaigns.

---

## 💻 Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Streamlit, Plotly, HTML5 Canvas, JavaScript |
| **Backend** | Python 3.9+, FastAPI (Experimental API) |
| **Data Engineering** | Pandas, NumPy, SQLite |
| **Machine Learning** | Facebook Prophet, Scikit-learn (TF-IDF), SciPy (SIR Model) |
| **NLP & AI** | TextBlob, NLTK, Google Translate API, gTTS |
| **DevOps** | Git, Docker, Streamlit Cloud |

---

## 🏆 Impact & Results

* **User Engagement:** The interactive "Particle Background" and "Country Face-Off" gamification features increased session duration.
* **Performance:** Optimized data caching reduced dashboard load times by **40%**.
* **Accessibility:** The voice assistant enables hands-free interaction, making the platform usable for a wider demographic.
* **Scalability:** The modular architecture allows the backend API to scale independently of the frontend visualization layer.
