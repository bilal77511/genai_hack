import streamlit as st
from main import PostCreatorCrew

st.set_page_config(page_title="Post Creator", layout="wide")

# Required inputs with descriptions
st.subheader("Required Information")
news_topic = st.text_input("Enter the news topic", 
    help="The main topic or subject of your post")
target_audience = st.text_input("Target Audience", 
    help="e.g., Professionals, students, general public, tech enthusiasts, etc.")
platform = st.selectbox("Select Platform", 
    ["LinkedIn", "Twitter/X", "Facebook", "Instagram", "Medium", "Other"],
    help="Choose the platform where you'll share this post")

# Optional inputs with descriptions
st.subheader("Optional Customization")
col1, col2 = st.columns(2)
with col1:
    tone = st.text_input("Tone of the Post", 
        help="e.g., Professional, casual, humorous, formal, etc.")
    word_count = st.text_input("Word Count or Length",
        help="e.g., Short (< 100 words), Medium (100-300 words), Long (300+ words)")
with col2:
    language = st.text_input("Language",
        value="English",
        help="e.g., English, Spanish, French, etc.")
    include_emojis = st.checkbox("Include Emojis", 
        help="Add relevant emojis to make the post more engaging")

# Advanced options
st.subheader("Additional Preferences")
special_requests = st.text_area("Special Requests or Additional Information",
    help="Any specific requirements, hashtags, formatting preferences, or additional context")

if st.button("Create Post"):
    with st.spinner("Generating your post..."):
        creator_crew = PostCreatorCrew(
            news_topic=news_topic,
            target_audience=target_audience,
            platform=platform,
            tone=tone,
            word_count=word_count,
            language=language,
            include_emojis=include_emojis,
            special_requests=special_requests
        )
        result = creator_crew.run()
    
    # Create tabs for different views of the content
    tab1, tab2 = st.tabs(["📱 Formatted Post", "📝 Markdown Source"])
    
    with tab1:
        # Display the formatted markdown
        st.markdown(result)
    
    with tab2:
        # Display the raw markdown in a code block
        st.code(result, language="markdown")
    
    # Add a download button for the markdown
    st.download_button(
        label="Download Markdown",
        data=result,
        file_name=f"post_{platform.lower().replace('/', '_')}.md",
        mime="text/markdown"
    )