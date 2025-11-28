$Action = New-ScheduledTaskAction -Execute "c:\Users\Manish\Desktop\COVID-19 vaccine tracker\scripts\update_data.bat"
$Trigger = New-ScheduledTaskTrigger -Daily -At 9am
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -TaskName "CovidVaccineTrackerUpdate" -Description "Daily update for COVID-19 Vaccine Tracker"

Write-Host "Task 'CovidVaccineTrackerUpdate' created successfully. It will run daily at 9:00 AM."
