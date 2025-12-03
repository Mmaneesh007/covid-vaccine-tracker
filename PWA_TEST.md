# PWA Quick Test Script

This script verifies that the PWA implementation is working correctly.

## Files Created

✅ assets/pwa/icon-192.png
✅ assets/pwa/icon-512.png  
✅ assets/pwa/manifest.json
✅ assets/pwa/sw.js
✅ src/pwa_injector.py
✅ PWA_INSTALLATION_GUIDE.md

## Integration Points

✅ app/streamlit_app.py - imports pwa_injector
✅ .streamlit/config.toml - enableStaticServing = true

## How to Test

### 1. Start the App

```bash
streamlit run app/streamlit_app.py
```

### 2. Open DevTools (Chrome/Edge)

- Press F12 or Ctrl+Shift+I
- Go to **Application** tab
- Check sections:
  - **Manifest**: Should show "COVID-19 Vaccine Tracker"
  - **Service Workers**: Should show registered worker
  - **Icons**: Should display 192x192 and 512x512 icons

### 3. Test Installation (Desktop)

- Look for install icon (+) in address bar
- Click to install
- App should open in standalone window

### 4. Test on Mobile (HTTPS Required)

- Deploy to Streamlit Cloud or Railway
- Test on Android Chrome
- Test on iOS Safari
- Follow PWA_INSTALLATION_GUIDE.md

## Expected Results

When you open the app:

1. PWA components inject successfully (no errors)
2. Service worker registers in console
3. Manifest is accessible at `/assets/pwa/manifest.json`
4. Icons are accessible
5. Install prompts appear on supported browsers

## Console Messages to Look For

```
✅ Service Worker registered: http://localhost:8501/
💡 PWA install prompt available (on supported browsers)
```

## Troubleshooting

If you see errors:

- Check that `enableStaticServing = true` in config.toml
- Verify all files exist in `/assets/pwa/`
- Ensure Python path includes parent directory
- Check browser console for specific errors
