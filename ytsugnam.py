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
    page_title="YouTube Channel Name Generator",
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
        width: 100%;
        background-color: #ff0000;
        color: white;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .suggestion-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ff0000;
        margin: 1rem 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
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
    """Generate channel name suggestions using Gemini."""
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
st.title("🎥 AI YouTube Channel Name Generator")
st.markdown("### Transform your content idea into a standout channel name")

# Two-column layout for input
col1, col2 = st.columns([2, 1])

with col1:
    niche = st.text_input(
        "What's your content niche?",
        placeholder="e.g., Python Programming, Cooking, Travel",
        help="Enter the main topic or theme of your YouTube channel"
    )

with col2:
    st.write("")
    st.write("")
    if st.button("✨ Generate Ideas", use_container_width=True):
        if niche:
            try:
                with st.spinner("🔍 Analyzing top channels in your niche..."):
                    channels = search_channels(niche)
                    
                    # Display current channels in cards
                    st.markdown("### 📊 Top Channels in Your Niche")
                    for i, channel in enumerate(channels, 1):
                        with st.container():
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
                    
                    # Generate and display suggestions
                    with st.spinner("🎯 Generating creative channel names..."):
                        suggestions = suggest_channel_names_gemini(channels, niche)
                        
                        st.markdown("### ✨ Suggested Channel Names")
                        st.markdown(f"""
                        <div class="suggestion-card">
                            {suggestions}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Tips section
                        with st.expander("📌 Tips for choosing your channel name"):
                            st.markdown("""
                            - Keep it memorable and easy to spell
                            - Avoid special characters or numbers if possible
                            - Check if the name is available across social media
                            - Consider your long-term content strategy
                            - Test the name with potential viewers
                            """)
            
            except Exception as e:
                st.error(f"❌ Oops! Something went wrong,tTry Again in Few Moment")
        else:
            st.warning("🎯 Please enter your content niche to get started!")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ for content creators  ",
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