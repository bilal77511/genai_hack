import streamlit as st
from utils import load_css, show_info

def main():
    # Load CSS
    st.markdown(load_css(), unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='sub-title'>Quick Actions</h2>", unsafe_allow_html=True)
        st.page_link("pages/create_post.py", label="Create New Post", icon="✍️")
        
        st.markdown("<h2 class='sub-title'>Templates</h2>", unsafe_allow_html=True)
        templates = {
            "Announcement": "Share important news or updates",
            "Event Promotion": "Promote upcoming events or webinars",
            "Product Launch": "Introduce new products or services",
            "Thought Leadership": "Share industry insights and expertise"
        }
        
        selected_template = st.selectbox(
            "Choose a template:",
            list(templates.keys())
        )
        
        if selected_template:
            st.info(templates[selected_template])

    # Main Content
    st.markdown("<h1 class='main-title'>AI Post Creator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Transform Your Ideas into Engaging Social Media Content</p>", unsafe_allow_html=True)

    # Introduction Card
    st.markdown(
        """<div class='card'>
            <h3>Welcome to AI Post Creator</h3>
            <p class='info-text'>Create professional social media content in seconds using AI</p>
        </div>""",
        unsafe_allow_html=True
    )

    # Features Section
    st.markdown("<h2 class='sub-title'>Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """<div class='card'>
                <h3>Multi-Platform Support</h3>
                <p>Create content for LinkedIn, Twitter, Facebook, and more</p>
            </div>""",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """<div class='card'>
                <h3>Customizable Content</h3>
                <p>Adjust tone, length, and style to match your needs</p>
            </div>""",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Post Creator",
        page_icon="✍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()