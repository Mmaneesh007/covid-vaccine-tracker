"""
Vaccine Reminder Module
Calculates second dose dates and generates .ics calendar files for reminders.
Version: 1.0.1 - Fixed import issue
"""
import streamlit as st
from datetime import datetime, timedelta
import io

def generate_ics_file(event_name, start_date, description):
    """Generate iCalendar (.ics) file content"""
    # Format dates for ICS (YYYYMMDD)
    dt_start = start_date.strftime("%Y%m%d")
    dt_end = (start_date + timedelta(days=1)).strftime("%Y%m%d")
    now = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//COVID-19 Vaccine Tracker//Reminder//EN
BEGIN:VEVENT
UID:{now}-vaccine@tracker.app
DTSTAMP:{now}
DTSTART;VALUE=DATE:{dt_start}
DTEND;VALUE=DATE:{dt_end}
SUMMARY:{event_name}
DESCRIPTION:{description}
BEGIN:VALARM
TRIGGER:-PT15H
ACTION:DISPLAY
DESCRIPTION:Reminder
END:VALARM
END:VEVENT
END:VCALENDAR"""
    return ics_content

def render_vaccine_reminder():
    """Render the vaccine reminder UI"""
    st.markdown("### 📅 Vaccine Dose Reminder")
    st.markdown("Calculate when your next dose is due and add it to your calendar.")
    
    # Vaccine Guidelines (Gap between doses)
    # Source: General guidelines, may vary by country
    vaccine_gaps = {
        "Covishield (Oxford/AstraZeneca)": 84,  # 12-16 weeks (using 12 weeks/84 days)
        "Covaxin (Bharat Biotech)": 28,         # 4-6 weeks
        "Pfizer-BioNTech (Comirnaty)": 21,      # 3 weeks
        "Moderna (Spikevax)": 28,               # 4 weeks
        "Sputnik V": 21,                        # 3 weeks
        "Janssen (Johnson & Johnson)": 0        # Single dose
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        vax_type = st.selectbox("Select Vaccine Type", list(vaccine_gaps.keys()))
        
    with col2:
        dose_date = st.date_input("Date of First Dose", max_value=datetime.now())
    
    gap_days = vaccine_gaps[vax_type]
    
    if gap_days == 0:
        st.success("✅ **Janssen is a single-dose vaccine.** You are fully vaccinated 2 weeks after this dose!")
    else:
        # Calculate next dose
        next_dose_date = dose_date + timedelta(days=gap_days)
        days_remaining = (next_dose_date - datetime.now().date()).days
        
        st.divider()
        
        # Display Result
        st.subheader("Your Next Dose")
        
        res_col1, res_col2 = st.columns([2, 1])
        
        with res_col1:
            st.markdown(f"**Recommended Date:**")
            st.markdown(f"## 🗓️ {next_dose_date.strftime('%B %d, %Y')}")
            st.caption(f"Based on standard {gap_days}-day gap for {vax_type}")
            
            if days_remaining > 0:
                st.info(f"⏳ **{days_remaining} days** to go!")
            elif days_remaining == 0:
                st.warning("🚨 **It's today!** Get your shot.")
            else:
                st.error(f"⚠️ **Overdue by {abs(days_remaining)} days.** Please book ASAP.")
        
        with res_col2:
            # Generate ICS
            ics_data = generate_ics_file(
                event_name=f"2nd Dose: {vax_type}",
                start_date=next_dose_date,
                description=f"Reminder for your second dose of {vax_type} vaccine. Calculated by COVID-19 Vaccine Tracker."
            )
            
            st.write("") # Spacing
            st.download_button(
                label="📅 Add to Calendar",
                data=ics_data,
                file_name="vaccine_reminder.ics",
                mime="text/calendar",
                help="Download .ics file to add to Google Calendar, Outlook, or Apple Calendar"
            )
            
            # Social Share Card - Temporarily disabled due to import issues
            # from src.social_share import generate_vaccine_warrior_card
            # try:
            #     share_img = generate_vaccine_warrior_card()
            #     st.download_button(
            #         label="📸 Share My Journey",
            #         data=share_img,
            #         file_name="Vaccine_Warrior.png",
            #         mime="image/png",
            #         help="Download and share on social media!"
            #     )
            # except:
            #     pass  # Silently fail if image generation doesn't work


