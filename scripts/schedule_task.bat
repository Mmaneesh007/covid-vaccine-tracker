@echo off
set "TASK_NAME=COVID19VaccineTrackerUpdate"
set "SCRIPT_PATH=c:\Users\Manish\Desktop\COVID-19 vaccine tracker\scripts\update_data.bat"

echo Creating daily task to run %SCRIPT_PATH% at 09:00 AM...

:: Create the task
:: /tn: Task Name
:: /tr: Task Run (path to script)
:: /sc: Schedule (daily)
:: /st: Start Time (09:00)
:: /f: Force (overwrite if exists)
:: /rl: Run Level (highest - requires admin if needed, but for user task maybe not)
:: Note: Running as current user. If password is needed, /rp might be required, but usually for local user it works if logged in.

schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\"" /sc daily /st 09:00 /f

if %errorlevel% equ 0 (
    echo Task "%TASK_NAME%" created successfully.
    echo You can view it in Task Scheduler.
    echo.
    echo To manually run the task now to test:
    echo schtasks /run /tn "%TASK_NAME%"
) else (
    echo Failed to create task. Please run this script as Administrator.
)
pause
