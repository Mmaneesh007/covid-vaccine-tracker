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

def display_news_feed(source='Google News', limit=25):
    """
    Display news feed in Streamlit sidebar with refresh capability.
    
    Args:
        source (str): News source
        limit (int): Number of headlines to display
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📰 Latest COVID-19 News")
    
    # News source selector
    selected_source = st.sidebar.selectbox(
        "News Source",
        options=list(NEWS_FEEDS.keys()),
        index=list(NEWS_FEEDS.keys()).index(source)
    )
    
    # Refresh button
    col1, col2 = st.sidebar.columns([3, 1])
    with col2:
        if st.button("🔄", help="Refresh news"):
            # Clear cache to fetch fresh news
            st.cache_data.clear()
            st.rerun()
    
    # Fetch and display news
    with st.sidebar:
        with st.spinner("Loading news..."):
            # Use cache but allow manual refresh via button
            headlines = fetch_news_cached(selected_source, limit)
            
            if headlines:
                st.caption(f"Showing {len(headlines)} latest headlines")
                
                # Display headlines in an expander to save space
                with st.expander("📋 View Headlines", expanded=True):
                    for i, headline in enumerate(headlines, 1):
                        # Format published date if available
                        try:
                            pub_date = datetime.strptime(
                                headline['published'], 
                                '%a, %d %b %Y %H:%M:%S %Z'
                            ).strftime('%b %d, %Y')
                        except:
                            pub_date = headline['published']
                        
                        # Display headline with link
                        st.markdown(
                            f"**{i}.** [{headline['title']}]({headline['link']})",
                            unsafe_allow_html=True
                        )
                        st.caption(f"🕒 {pub_date}")
                        
                        if i < len(headlines):
                            st.markdown("---")
            else:
                st.warning("No news available at the moment.")

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_news_cached(source, limit):
    """Cached version of fetch_news_headlines"""
    return fetch_news_headlines(source, limit)
