@echo off
cd /d "c:\Users\Manish\Desktop\COVID-19 vaccine tracker"
echo Starting COVID-19 Vaccine Tracker Update...
python run_all.py
echo Update process finished.
timeout /t 10
