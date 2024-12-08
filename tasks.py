from textwrap import dedent
from crewai import Task

class NewsTasks:
    def retrieve_news_task(self, agent, news_topic):
        return Task(
            description=dedent(f"""
                Retrieve all news articles related to the topic: {news_topic}.
                Provide a list of articles with their titles, sources, and publication dates.
                Focus on finding comprehensive and reliable sources.

                Your final answer should be a detailed list of news articles with:
                - Titles
                - Sources
                - Publication dates
                - Brief description of each article
            """),
            agent=agent,
            expected_output="Comprehensive list of news articles related to the topic"
        )

    def validate_and_summarize_task(self, agent, news_content, news_topic):
        return Task(
            description=dedent(f"""
                Validate and summarize the news content about: {news_topic}

                Content to validate: {news_content}

                Your tasks:
                1. Verify the information across multiple sources
                2. Fact-check key claims
                3. Create a high-level summary of all verified information
                4. Highlight any discrepancies or conflicting information
                5. Provide a final, comprehensive summary of the topic

                Your final answer should include:
                - Validation results
                - Comprehensive summary
                - Key findings
                - Any notable discrepancies
            """),
            agent=agent,
            expected_output="Validated and summarized news content"
        )

    def create_post_task(self, agent, news_content, target_audience, platform, 
                         tone, word_count, language, include_emojis, special_requests):
        emoji_instruction = "Include relevant emojis throughout the post." if include_emojis else ""
        special_instruction = f"\nAdditional requirements: {special_requests}" if special_requests else ""
        
        return Task(
            description=dedent(f"""
                Create a {platform} post based on the following validated news content:
                {news_content}

                Target Audience: {target_audience}
                Platform: {platform}
                Tone: {tone if tone else 'Use appropriate tone for the platform and audience'}
                Length: {word_count if word_count else 'Use appropriate length for the platform'}
                Language: {language}
                {emoji_instruction}
                {special_instruction}

                Ensure the post:
                1. Is optimized for the specified platform
                2. Speaks directly to the target audience
                3. Uses appropriate formatting and structure
                4. Includes relevant hashtags if appropriate
                5. Follows platform-specific best practices
                6. Includes engaging statistics or data when available
                7. Uses quotes and highlights for important information
                8. Incorporates a clear call-to-action
                
                Format your response in markdown with:
                - Headers using #
                - Bold text using **
                - Lists using - or 1.
                - Quote blocks using >
                - Code/special formatting using `
                - Links in proper markdown format [text](url)
                - Statistics and numbers highlighted in **bold**
                
                Structure the output as:
                # Generated Post for {platform}
                
                ## Post Content
                [The actual post content]
                
                ## Post Details
                - **Platform**: [platform]
                - **Target Audience**: [audience]
                - **Tone**: [tone]
                - **Length**: [word count]
                
                ## Engagement Elements
                - Key statistics used
                - Quotes included
                - Call-to-action
                
                ## Hashtags and Keywords
                [relevant hashtags and keywords]
                
                Your final answer should be the complete markdown-formatted content.
            """),
            agent=agent
        )