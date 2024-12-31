import streamlit as st
import random

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

def generate_channel_names(niche):
    """Generate channel name suggestions based on predefined patterns and the given niche."""
    
    # Enhanced word lists for more variety
    prefixes = [
        "The", "Pro", "Best", "Top", "Epic", "Amazing", "Creative", "Daily", 
        "Smart", "Expert", "Elite", "Premium", "Ultimate", "Super", "Master"
    ]
    
    suffixes = [
        "Hub", "Pro", "Master", "Guide", "Tips", "Zone", "World", "Space", 
        "Lab", "Studio", "Central", "HQ", "Academy", "Nation", "Sphere"
    ]
    
    # Enhanced niche-specific dictionaries
    niche_specific = {
        "cooking": [
            "Chef", "Kitchen", "Recipe", "Food", "Cuisine", "Tasty", "Delicious", 
            "Flavor", "Gourmet", "Cooking", "Culinary", "Foodie", "Dishes", "Bites"
        ],
        "gaming": [
            "Gamer", "Gaming", "Play", "Stream", "Level", "Quest", "Achievement", 
            "Player", "Score", "League", "Console", "Arcade", "Champion", "Guild"
        ],
        "travel": [
            "Traveler", "Adventure", "Journey", "Explore", "Wanderlust", "Discovery", 
            "Globe", "Trip", "Voyage", "Tour", "Nomad", "Explorer", "Passport"
        ],
        "tech": [
            "Tech", "Digital", "Gadget", "Innovation", "Code", "Hack", "System", 
            "Device", "Program", "Binary", "Cyber", "Future", "Smart", "Bot"
        ],
        "fitness": [
            "Fit", "Health", "Strong", "Muscle", "Workout", "Training", "Exercise", 
            "Power", "Athletic", "Energy", "Beast", "Strength", "Gains", "Wellness"
        ],
        "education": [
            "Learn", "Study", "Teach", "Knowledge", "Academy", "School", "Education",
            "Class", "Course", "Tutorial", "Lesson", "Training", "Skills"
        ],
        "business": [
            "Business", "Success", "Entrepreneur", "Money", "Wealth", "Growth",
            "Strategy", "Leader", "Expert", "Guru", "Mentor", "Coach"
        ]
    }
    
    # Convert niche to appropriate category
    niche = niche.lower()
    for category in niche_specific:
        if category in niche:
            specific_words = niche_specific[category]
            break
    else:
        specific_words = [niche.capitalize()] * 5 + [w.capitalize() for w in niche.split()]
    
    suggestions = []
    explanations = []
    
    # Generate 10 suggestions with more patterns
    for i in range(10):
        name_type = random.randint(1, 6)
        
        if name_type == 1:
            # Pattern: The + [Niche] + Suffix
            name = f"{random.choice(prefixes)} {random.choice(specific_words)} {random.choice(suffixes)}"
            explanation = f"Combines professionalism with {niche} expertise"
        
        elif name_type == 2:
            # Pattern: [Niche]Pro/Master
            name = f"{random.choice(specific_words)}{random.choice(['Pro', 'Master', 'Expert', 'Guru'])}"
            explanation = f"Short and powerful name emphasizing {niche} expertise"
        
        elif name_type == 3:
            # Pattern: Daily + [Niche] + Tips
            name = f"{random.choice(['Daily', 'Weekly', 'Pro'])} {random.choice(specific_words)} {random.choice(['Tips', 'Guide', 'Hub'])}"
            explanation = f"Emphasizes regular, valuable {niche} content"
        
        elif name_type == 4:
            # Pattern: Creative + [Niche] + Zone
            name = f"{random.choice(prefixes)} {random.choice(specific_words)} {random.choice(['Zone', 'Space', 'World'])}"
            explanation = f"Creates a unique brand identity in the {niche} space"
        
        elif name_type == 5:
            # Pattern: [Niche] + Academy/School/Lab
            name = f"{random.choice(specific_words)} {random.choice(['Academy', 'School', 'Lab', 'Workshop'])}"
            explanation = f"Positions your channel as an educational resource for {niche}"
        
        else:
            # Pattern: Mr/Ms + [Niche]
            name = f"{random.choice(['Mr', 'Ms', 'The'])} {random.choice(specific_words)} {random.choice(['TV', 'Show', 'Channel'])}"
            explanation = f"Personal branding approach for {niche} content"
        
        suggestions.append(name)
        explanations.append(explanation)
    
    return suggestions, explanations

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
            placeholder="e.g., Cooking, Gaming, Travel, Tech",
            help="Enter the main topic or theme of your YouTube channel"
        )
        st.write("")
        if st.button("✨ Generate Ideas", use_container_width=True):
            if niche:
                try:
                    with st.spinner("🔍 Generating creative channel names..."):
                        suggestions, explanations = generate_channel_names(niche)
                        
                        st.markdown("### ✨ Suggested Channel Names")
                        for suggestion, explanation in zip(suggestions, explanations):
                            st.markdown(f"""
                            <div class="suggestion-card">
                                <h3>🎯 {suggestion}</h3>
                                <p>💡 {explanation}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error("❌ Oops! Something went wrong. Please try again.")
            else:
                st.warning("🎯 Please enter your content niche to get started!")

# Tips section
with st.expander("📌 Tips for choosing your channel name"):
    st.markdown("""
    - Keep it memorable and easy to spell
    - Avoid special characters or numbers if possible
    - Check if the name is available across social media
    - Consider your long-term content strategy
    - Test the name with potential viewers
    - Make sure it's easy to pronounce
    - Keep it relevant to your content
    - Consider your target audience
    - Make it unique and brandable
    - Avoid trendy terms that might date quickly
    """)

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ for content creators",
    unsafe_allow_html=True
)

# Hide links
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