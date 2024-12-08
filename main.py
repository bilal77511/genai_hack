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

if __name__ == "__main__":
    print("## Welcome to Post Creator")
    print('-----------------------------')
    news_topic = input("Enter the news topic: ")
    target_audience = input("Enter target audience: ")
    platform = input("Enter platform: ")
    tone = input("Enter tone of the post: ")
    word_count = input("Enter word count: ")
    language = input("Enter language: ")
    
    creator_crew = PostCreatorCrew(news_topic, target_audience, platform, tone, word_count, language)
    result = creator_crew.run()
    print("\n\n########################")
    print("## Generated Post:")
    print("########################\n")
    print(result)