# src/pwa_injector.py
"""
PWA Component Injector for Streamlit
Injects Progressive Web App meta tags and service worker registration into the app.
"""

import streamlit.components.v1 as components

def inject_pwa_components():
    """
    Inject PWA meta tags, manifest link, and service worker registration
    into the Streamlit app's HTML head section.
    """
    pwa_html = """
    <head>
        <!-- PWA Manifest -->
        <link rel="manifest" href="/assets/pwa/manifest.json">
        
        <!-- Theme Color -->
        <meta name="theme-color" content="#667eea">
        <meta name="msapplication-TileColor" content="#667eea">
        
        <!-- Apple Touch Icon -->
        <link rel="apple-touch-icon" href="/assets/pwa/icon-512.png">
        
        <!-- Apple Mobile Web App -->
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="VaxTracker">
        
        <!-- Mobile Viewport -->
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes">
        
        <!-- Description -->
        <meta name="description" content="Track global COVID-19 vaccination progress with real-time data, forecasts, and AI insights">
        
        <!-- Service Worker Registration -->
        <script>
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                    navigator.serviceWorker.register('/assets/pwa/sw.js')
                        .then((registration) => {
                            console.log('✅ Service Worker registered:', registration.scope);
                            
                            // Check for updates every hour
                            setInterval(() => {
                                registration.update();
                            }, 3600000);
                        })
                        .catch((error) => {
                            console.error('❌ Service Worker registration failed:', error);
                        });
                });
                
                // Handle service worker updates
                navigator.serviceWorker.addEventListener('controllerchange', () => {
                    console.log('🔄 New Service Worker activated');
                });
            }
        </script>
        
        <!-- Install PWA Prompt Handler (for browsers that support it) -->
        <script>
            let deferredPrompt;
            
            window.addEventListener('beforeinstallprompt', (e) => {
                // Prevent Chrome 67 and earlier from automatically showing the prompt
                e.preventDefault();
                // Stash the event so it can be triggered later
                deferredPrompt = e;
                console.log('💡 PWA install prompt available');
            });
            
            window.addEventListener('appinstalled', () => {
                console.log('✅ PWA installed successfully');
                deferredPrompt = null;
            });
        </script>
    </head>
    """
    
    # Inject into Streamlit using components
    components.html(pwa_html, height=0, width=0)


def show_install_instructions():
    """
    Display platform-specific installation instructions in Streamlit.
    """
    import streamlit as st
    
    st.info("""
    ### 📱 Install This App
    
    **Android (Chrome/Edge/Firefox):**
    1. Tap the menu (⋮) → "Add to Home screen" or "Install app"
    2. Follow the prompt to install
    
    **iOS (Safari only):**
    1. Tap the Share button (□↑)
    2. Scroll down and tap "Add to Home Screen"
    3. Tap "Add" to install
    
    **Desktop (Chrome/Edge):**
    1. Look for the install icon (+) in the address bar
    2. Click it to install
    
    Once installed, launch the app from your home screen for a native app experience!
    """)
