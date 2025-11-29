# src/feedback.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

FEEDBACK_FILE = "data/user_feedback.csv"

def initialize_feedback_file():
    """Create feedback CSV file if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(FEEDBACK_FILE):
        df = pd.DataFrame(columns=['timestamp', 'rating', 'comment', 'language'])
        df.to_csv(FEEDBACK_FILE, index=False)

def save_feedback(rating, comment, language):
    """
    Save user feedback to CSV file.
    
    Args:
        rating (int): Star rating (1-5)
        comment (str): Optional user comment
        language (str): User's selected language
    """
    initialize_feedback_file()
    
    # Create new feedback entry
    new_feedback = pd.DataFrame([{
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'rating': rating,
        'comment': comment,
        'language': language
    }])
    
    # Append to CSV
    new_feedback.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)

def display_feedback_form():
    """Display feedback form in Streamlit sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⭐ Rate This App")
    
    # Initialize session state for feedback
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    
    if not st.session_state.feedback_submitted:
        with st.sidebar.form("feedback_form"):
            # Star rating
            rating = st.select_slider(
                "How would you rate your experience?",
                options=[1, 2, 3, 4, 5],
                value=5,
                format_func=lambda x: "⭐" * x
            )
            
            # Optional comment
            comment = st.text_area(
                "Share your thoughts (optional)",
                placeholder="What did you like? What can we improve?",
                max_chars=500
            )
            
            # Submit button
            submitted = st.form_submit_button("Submit Feedback")
            
            if submitted:
                # Get current language from session state
                current_lang = st.session_state.get('language', 'en')
                
                # Save feedback
                save_feedback(rating, comment, current_lang)
                
                # Update session state
                st.session_state.feedback_submitted = True
                st.rerun()
    else:
        st.sidebar.success("✅ Thank you for your feedback!")
        if st.sidebar.button("Submit Another Review"):
            st.session_state.feedback_submitted = False
            st.rerun()

def get_feedback_stats():
    """
    Get feedback statistics (for admin/developer use).
    
    Returns:
        dict: Statistics including average rating, total count, etc.
    """
    if not os.path.exists(FEEDBACK_FILE):
        return None
    
    df = pd.read_csv(FEEDBACK_FILE)
    
    if len(df) == 0:
        return None
    
    stats = {
        'total_responses': len(df),
        'average_rating': df['rating'].mean(),
        'rating_distribution': df['rating'].value_counts().to_dict(),
        'recent_comments': df.nlargest(5, 'timestamp')[['timestamp', 'rating', 'comment']].to_dict('records')
    }
    
    return stats
