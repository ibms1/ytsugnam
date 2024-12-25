import os
import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv
import requests

# Load environment variables locally
load_dotenv()

# Get API keys from environment or Streamlit Secrets
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") or st.secrets["YOUTUBE_API_KEY"]
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_channels(niche):
    """
    Search for channels on YouTube related to the given niche.
    """
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
            part="statistics",
            id=channel_id
        ).execute()
        stats = channel_data["items"][0]["statistics"]
        channels.append({
            "name": item["snippet"]["title"],
            "subscribers": int(stats.get("subscriberCount", 0)),
            "views": int(stats.get("viewCount", 0)),
        })
    return channels

def suggest_channel_names_gemini(channels, niche):
    """
    Suggest new competitive channel names using Google Gemini API.
    """
    prompt = f"""
    You are an AI expert in YouTube channel strategy. Based on the following niche "{niche}" and these existing channels:
    
    {channels}
    
    Suggest creative, catchy, and competitive new YouTube channel names:
    """
    url = "https://gemini.googleapis.com/v1/generateText"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "maxTokens": 100,
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["text"]
    else:
        raise Exception(f"Gemini API error: {response.text}")

# Streamlit interface
st.title("YouTube Channel Name Suggestions")
st.markdown("### Enter your niche to get creative channel name ideas")

# Input niche
niche = st.text_input("Enter your niche (e.g., cooking, technology):", "")

if st.button("Get Suggestions"):
    if niche:
        st.write("Fetching and analyzing data...")
        try:
            # Fetch channels from YouTube
            channels = search_channels(niche)
            st.write("Found the following channels:")
            for i, channel in enumerate(channels, start=1):
                st.write(f"{i}. {channel['name']} - Subscribers: {channel['subscribers']}, Views: {channel['views']}")
            
            # Suggest new names using Gemini
            suggestions = suggest_channel_names_gemini(channels, niche)
            st.markdown("### Suggested Names:")
            st.write(suggestions)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a niche!")
