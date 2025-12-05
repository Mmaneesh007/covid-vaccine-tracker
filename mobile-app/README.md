# 📱 COVID-19 Vaccine Tracker Mobile App

This is the official mobile application for the Vaccine Tracker, built with **React Native** and **Expo**.

## 🚀 Quick Start

### 1. Start the Backend API (Required)

The mobile app fetches data from your local Python backend.
Open a terminal in the root `COVID-19 vaccine tracker` folder:

```powershell
# Activate your environment if needed
python app/api/main.py
```

*Ensure the API is running on port 8001.*

### 2. Run the Mobile App

Open a **new terminal** and navigate to this folder:

```powershell
cd mobile-app
npm install  # Install dependencies (only first time)
npx expo start
```

### 3. Test on Your Phone

1. Download **Expo Go** from the App Store (iOS) or Google Play (Android).
2. Scan the **QR Code** shown in the terminal.
3. The app will load on your phone!

## 🛠 Troubleshooting

- **"Network Error"**: Make sure your phone and computer are on the **same Wi-Fi**.
- **Android Emulator**: The app is pre-configured to check `10.0.2.2:8001` for the backend (standard emulator localhost).
- **Physical Device**: You may need to update `src/api/client.ts` to use your computer's local IP address (e.g., `192.168.1.X:8001`) instead of `localhost`.
