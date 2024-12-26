import os
import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") or st.secrets["YOUTUBE_API_KEY"]
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

# Initialize APIs
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# Set page configuration
st.set_page_config(
    page_title="AI YouTube Channel Name Generator",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        background-color: #ff0000;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        min-width: 200px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        height: 100%;
    }
    .suggestion-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ff0000;
        margin-bottom: 1rem;
        height: 100%;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .center-content {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def search_channels(niche):
    """Search for YouTube channels in the given niche."""
    search_response = youtube.search().list(
        q=niche,
        type="channel",
        part="snippet",
        maxResults=5
    ).execute()
    
    channels = []
    for item in search_response["items"]:
        channel_id = item["id"]["channelId"]
        channel_data = youtube.channels().list(
            part="statistics,snippet",
            id=channel_id
        ).execute()
        
        stats = channel_data["items"][0]["statistics"]
        snippet = channel_data["items"][0]["snippet"]
        
        channels.append({
            "name": snippet["title"],
            "description": snippet["description"][:100] + "...",
            "subscribers": int(stats.get("subscriberCount", 0)),
            "views": int(stats.get("viewCount", 0)),
            "videos": int(stats.get("videoCount", 0))
        })
    return channels

def suggest_channel_names_gemini(channels, niche):
    """Generate channel name suggestions using AI."""
    prompt = f"""
    As a YouTube branding expert, analyze these top {niche} channels:
    {channels}
    
    Create 5 unique channel name suggestions that:
    1. Stand out in the {niche} niche
    2. Are memorable and brandable
    3. Reflect current YouTube trends
    
    For each suggestion, provide:
    - The channel name
    - A brief explanation of its appeal
    - Why it would work well in this niche
    
    Format each suggestion clearly with emojis and bullet points.
    """
    
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"❌ Oops! Something went wrong,tTry Again in Few Moment")

# Main UI
st.title("🎥 YouTube Channel Name Generator")
st.markdown("### Transform your content idea into a standout channel name")

# Centered input container
container = st.container()
with container:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        niche = st.text_input(
            "What's your content niche?",
            placeholder="e.g.,Cooking, Travel",
            help="Enter the main topic or theme of your YouTube channel"
        )
        st.write("")  # Add some spacing
        if st.button("✨ Generate Ideas", use_container_width=True):
            if niche:
                try:
                    with st.spinner("🔍 Analyzing top channels in your niche..."):
                        channels = search_channels(niche)
                        suggestions = suggest_channel_names_gemini(channels, niche)
                        
                        # Create two columns for results
                        col_left, col_right = st.columns(2)
                        
                        # Left column: Top Channels
                        with col_left:
                            st.markdown("### 📊 Top Channels in Your Niche")
                            for channel in channels:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h4>{channel['name']}</h4>
                                    <p><small>{channel['description']}</small></p>
                                    <table>
                                        <tr>
                                            <td>👥 {channel['subscribers']:,} subscribers</td>
                                            <td>👀 {channel['views']:,} views</td>
                                            <td>🎥 {channel['videos']:,} videos</td>
                                        </tr>
                                    </table>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Right column: Suggestions
                        with col_right:
                            st.markdown("### ✨ Suggested Channel Names")
                            st.markdown(f"""
                            <div class="suggestion-card">
                                {suggestions}
                            </div>
                            """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"❌ Oops! Something went wrong,tTry Again in Few Moment")
            else:
                st.warning("🎯 Please enter your content niche to get started!")

# Tips section at the bottom
with st.expander("📌 Tips for choosing your channel name"):
    st.markdown("""
    - Keep it memorable and easy to spell
    - Avoid special characters or numbers if possible
    - Check if the name is available across social media
    - Consider your long-term content strategy
    - Test the name with potential viewers
    """)

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ for content creators",
    unsafe_allow_html=True
)



hide_links_style = """
        <style>
        a {
            pointer-events: none;
            cursor: default;
            text-decoration: none;
            color: inherit;
        }
        </style>
        """
st.markdown(hide_links_style, unsafe_allow_html=True)