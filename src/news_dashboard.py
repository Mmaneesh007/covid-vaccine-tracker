# src/news_feed.py
import feedparser
import streamlit as st
from datetime import datetime

# RSS Feed URLs for COVID-19 news
NEWS_FEEDS = {
    'WHO': 'https://www.who.int/rss-feeds/news-english.xml',
    'Google News': 'https://news.google.com/rss/search?q=COVID-19+vaccine&hl=en-US&gl=US&ceid=US:en'
}

def fetch_news_headlines(source='Google News', limit=25):
    """
    Fetch latest COVID-19 news headlines from RSS feed.
    
    Args:
        source (str): News source ('WHO' or 'Google News')
        limit (int): Maximum number of headlines to fetch
    
    Returns:
        list: List of dictionaries with 'title', 'link', and 'published' keys
    """
    try:
        feed_url = NEWS_FEEDS.get(source, NEWS_FEEDS['Google News'])
        feed = feedparser.parse(feed_url)
        
        headlines = []
        for entry in feed.entries[:limit]:
            headline = {
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', '#'),
                'published': entry.get('published', 'Unknown date')
            }
            headlines.append(headline)
        
        return headlines
    except Exception as e:
        st.error(f"Failed to fetch news: {str(e)}")
        return []

def render_news_dashboard(source='Google News', limit=6):
    """
    Display news feed in the main dashboard with premium card styling.
    """
    st.markdown("### 📰 Global Health Updates")
    
    # Initialize refresh counter
    if 'news_refresh_count' not in st.session_state:
        st.session_state.news_refresh_count = 0
        
    # Controls row
    col1, col2 = st.columns([4, 1])
    with col1:
        selected_source = st.selectbox(
            "Source",
            options=list(NEWS_FEEDS.keys()),
            index=list(NEWS_FEEDS.keys()).index(source),
            label_visibility="collapsed"
        )
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.news_refresh_count += 1
            st.rerun()

    # Fetch news (uncached for freshness or using session state counter)
    headlines = fetch_news_headlines(selected_source, limit)
    
    if headlines:
        # Display in a grid of cards
        for i in range(0, len(headlines), 2):
            c1, c2 = st.columns(2)
            
            # Card 1
            if i < len(headlines):
                with c1:
                    item = headlines[i]
                    st.markdown(
                        f"""
                        <div style="
                            background: rgba(255,255,255,0.8);
                            padding: 20px;
                            border-radius: 16px;
                            border: 1px solid rgba(0,0,0,0.05);
                            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                            height: 100%;
                            transition: transform 0.2s;
                        ">
                            <div style="font-size: 0.8rem; color: #667eea; font-weight: 600; margin-bottom: 8px;">
                                {item.get('published', 'Just now')}
                            </div>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin-bottom: 12px; line-height: 1.4;">
                                {item['title']}
                            </div>
                            <a href="{item['link']}" target="_blank" style="
                                display: inline-block;
                                text-decoration: none;
                                color: #764ba2;
                                font-weight: 500;
                                font-size: 0.9rem;
                            ">
                                Read Article →
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.write("") # Spacer
            
            # Card 2
            if i + 1 < len(headlines):
                with c2:
                    item = headlines[i+1]
                    st.markdown(
                        f"""
                        <div style="
                            background: rgba(255,255,255,0.8);
                            padding: 20px;
                            border-radius: 16px;
                            border: 1px solid rgba(0,0,0,0.05);
                            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                            height: 100%;
                            transition: transform 0.2s;
                        ">
                            <div style="font-size: 0.8rem; color: #667eea; font-weight: 600; margin-bottom: 8px;">
                                {item.get('published', 'Just now')}
                            </div>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin-bottom: 12px; line-height: 1.4;">
                                {item['title']}
                            </div>
                            <a href="{item['link']}" target="_blank" style="
                                display: inline-block;
                                text-decoration: none;
                                color: #764ba2;
                                font-weight: 500;
                                font-size: 0.9rem;
                            ">
                                Read Article →
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.write("") # Spacer
    else:
        st.warning("Unable to fetch news at this time.")
