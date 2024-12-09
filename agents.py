from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
import os

class NewsAgents():
 
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL"),
            base_url=os.getenv("API_ENDPOINT"),
            api_key=os.getenv("API_KEY")
        )

    def news_retrieval_agent(self):
        return Agent(
            role='News Retriever',
            goal='Find relevant and recent news articles on the given topic',
            backstory="""You are an expert news researcher with a keen eye for 
                        finding relevant and credible news sources. Your specialty 
                        is gathering comprehensive news coverage on specific topics.""",
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True,
            llm=self.llm
        )

    def news_validator_agent(self):
        return Agent(
            role='News Validator and Summarizer',
            goal='Validate news information and create comprehensive summaries',
            backstory="""You are an experienced fact-checker and content summarizer. 
                        You verify information across multiple sources and create 
                        concise, accurate summaries of complex news topics.""",
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True,
            llm=self.llm
        )

    def post_creator_agent(self):
        return Agent(
            role='Post Creator',
            goal='Create engaging social media posts from validated news content',
            backstory="""You are a social media expert who excels at creating 
                        engaging posts tailored to specific audiences and platforms. 
                        You know how to maintain the right tone and length while 
                        maximizing engagement.""",
            tools=[],
            verbose=True,
            llm=self.llm
        )

    def fake_news_detector_agent(self):
        return Agent(
            role='Fake News Detective',
            goal='Analyze and verify news authenticity using multiple sources',
            backstory="""You are an expert fact-checker and digital forensics specialist
                        with years of experience in detecting misinformation and fake news.
                        You use multiple reliable sources to cross-reference claims and
                        provide detailed analysis of news authenticity.""",
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True,
            llm=self.llm
        )