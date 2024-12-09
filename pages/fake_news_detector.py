import streamlit as st
from utils import load_css, show_error, show_success
from crewai import Crew
from agents import NewsAgents
from tasks import NewsTasks
from dotenv import load_dotenv

load_dotenv()

class FakeNewsDetectorCrew:
    def __init__(self, news_content):
        self.news_content = news_content

    def run(self):
        agents = NewsAgents()
        tasks = NewsTasks()

        detector_agent = agents.fake_news_detector_agent()
        
        verify_task = tasks.verify_news_authenticity_task(
            detector_agent,
            self.news_content
        )

        crew = Crew(
            agents=[detector_agent],
            tasks=[verify_task],
            verbose=True
        )

        result = crew.kickoff()
        return result

# Page Configuration
st.set_page_config(page_title="Fake News Detector", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state for verification history
if 'verification_history' not in st.session_state:
    st.session_state.verification_history = []

# Title
st.markdown("<h1 class='main-title'>Fake News Detector 🔍</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Verify the authenticity of news content using AI</p>", unsafe_allow_html=True)

# Input Section
st.markdown("<h2 class='sub-title'>News Content</h2>", unsafe_allow_html=True)
news_content = st.text_area(
    "Paste the news content or article you want to verify",
    height=200,
    help="Include the full text of the news article or content you want to verify"
)

# Analysis Button
if st.button("Verify News", type="primary"):
    if not news_content:
        show_error("Please enter some news content to verify")
    else:
        with st.spinner("Analyzing news content..."):
            try:
                detector = FakeNewsDetectorCrew(news_content)
                result = detector.run()
                
                # Add to history
                st.session_state.verification_history.append({
                    "content": news_content[:200] + "...",  # Store truncated content
                    "analysis": result
                })
                
                show_success("Analysis completed!")
                
                # Display Results
                st.markdown("<h2 class='sub-title'>Analysis Results</h2>", unsafe_allow_html=True)
                st.markdown(result)
                
                # Download button for full report
                st.download_button(
                    label="Download Full Report",
                    data=result,
                    file_name="news_verification_report.md",
                    mime="text/markdown"
                )
            
            except Exception as e:
                show_error(f"Error during analysis: {str(e)}")

# Display History
if st.session_state.verification_history:
    st.markdown("<h2 class='sub-title'>Recent Verifications</h2>", unsafe_allow_html=True)
    for verification in reversed(st.session_state.verification_history[-5:]):
        st.markdown(
            f"""<div class='card'>
                <p><strong>Analyzed Content:</strong></p>
                <p class='info-text'>{verification['content']}</p>
                <div class='response-area'>{verification['analysis']}</div>
            </div>""",
            unsafe_allow_html=True
        )
