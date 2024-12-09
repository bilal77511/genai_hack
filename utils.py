import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_ai_model():
    """Initialize AI model with error handling"""
    try:
        return ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
    except Exception as e:
        st.error(f"Error initializing AI model: {str(e)}")
        return None

def generate_content(prompt, system_prompt=""):
    """Generate content using the AI model"""
    try:
        model = init_ai_model()
        if not model:
            return "Error: Could not initialize AI model"

        template = ChatPromptTemplate.from_template(
            system_prompt + "\n\n" + prompt if system_prompt else prompt
        )
        chain = template | model | StrOutputParser()
        return chain.invoke({})

    except Exception as e:
        return f"Error: {str(e)}"

def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #FF4B4B;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 500;
        color: #FAFAFA;
        margin: 1rem 0;
    }
    
    .card {
        background-color: #262730;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .response-area {
        background-color: #1E1E1E;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #FF4B4B;
    }
    
    .info-text {
        color: #B2B2B2;
        font-size: 0.9rem;
        font-style: italic;
    }
    </style>
    """

def show_error(message):
    st.error(f"🚨 {message}")

def show_success(message):
    st.success(f"✅ {message}")

def show_info(message):
    st.info(f"ℹ️ {message}")