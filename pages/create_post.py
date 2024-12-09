import streamlit as st
from utils import load_css, show_error, show_success
from crewai import Crew
from textwrap import dedent
from agents import NewsAgents
from tasks import NewsTasks
from dotenv import load_dotenv

load_dotenv()

class PostCreatorCrew:
    def __init__(self, news_topic, target_audience, platform, tone="", 
                 word_count="", language="English", include_emojis=False, 
                 special_requests=""):
        self.news_topic = news_topic
        self.target_audience = target_audience
        self.platform = platform
        self.tone = tone
        self.word_count = word_count
        self.language = language
        self.include_emojis = include_emojis
        self.special_requests = special_requests

    def run(self):
        agents = NewsAgents()
        tasks = NewsTasks()

        news_retriever = agents.news_retrieval_agent()
        news_validator = agents.news_validator_agent()
        post_creator = agents.post_creator_agent()

        retrieve_news_task = tasks.retrieve_news_task(
            news_retriever,
            self.news_topic
        )
        
        validate_news_task = tasks.validate_and_summarize_task(
            news_validator,
            "{retrieve_news_task.output}",
            self.news_topic
        )
        
        create_post_task = tasks.create_post_task(
            post_creator,
            "{validate_news_task.output}",
            self.target_audience,
            self.platform,
            self.tone,
            self.word_count,
            self.language,
            self.include_emojis,
            self.special_requests
        )

        crew = Crew(
            agents=[news_retriever, news_validator, post_creator],
            tasks=[retrieve_news_task, validate_news_task, create_post_task],
            verbose=True
        )

        result = crew.kickoff()
        return result

# Load CSS and configure page
st.set_page_config(page_title="Create Post", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state for post history
if 'post_history' not in st.session_state:
    st.session_state.post_history = []

# Title
st.markdown("<h1 class='main-title'>Create Your Post</h1>", unsafe_allow_html=True)

# Required inputs with descriptions
st.markdown("<h2 class='sub-title'>Required Information</h2>", unsafe_allow_html=True)
news_topic = st.text_input("Enter the news topic", 
    help="The main topic or subject of your post")
target_audience = st.text_input("Target Audience", 
    help="e.g., Professionals, students, general public, tech enthusiasts, etc.")
platform = st.selectbox("Select Platform", 
    ["LinkedIn", "Twitter/X", "Facebook", "Instagram", "Medium", "Other"],
    help="Choose the platform where you'll share this post")

# Optional inputs with descriptions
st.markdown("<h2 class='sub-title'>Optional Customization</h2>", unsafe_allow_html=True)
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
st.markdown("<h2 class='sub-title'>Additional Preferences</h2>", unsafe_allow_html=True)
special_requests = st.text_area("Special Requests or Additional Information",
    help="Any specific requirements, hashtags, formatting preferences, or additional context")

if st.button("Create Post", type="primary"):
    if not news_topic or not target_audience:
        show_error("Please fill in all required fields")
    else:
        with st.spinner("Generating your post..."):
            try:
                # Create and run PostCreatorCrew
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
                
                # Add to history
                st.session_state.post_history.append({
                    "topic": news_topic,
                    "platform": platform,
                    "content": result
                })
                
                show_success("Post generated successfully!")
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["📱 Preview", "📝 Raw Text"])
                
                with tab1:
                    st.markdown(result)
                
                with tab2:
                    st.code(result, language="markdown")
                
                # Download button
                st.download_button(
                    label="Download Post",
                    data=result,
                    file_name=f"post_{platform.lower().replace('/', '_')}.md",
                    mime="text/markdown"
                )
            
            except Exception as e:
                show_error(f"Error generating post: {str(e)}")

# Display history
if st.session_state.post_history:
    st.markdown("<h2 class='sub-title'>Recent Posts</h2>", unsafe_allow_html=True)
    for post in reversed(st.session_state.post_history[-5:]):  # Show last 5 posts
        st.markdown(
            f"""<div class='card'>
                <p><strong>Topic:</strong> {post['topic']}</p>
                <p><strong>Platform:</strong> {post['platform']}</p>
                <div class='response-area'>{post['content']}</div>
            </div>""",
            unsafe_allow_html=True
        )