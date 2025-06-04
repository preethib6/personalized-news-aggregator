import os
from dotenv import load_dotenv
import boto3
import requests
import json
import streamlit as st
import time

# Load environment variables (including AWS credentials)
load_dotenv()

# Fetch AWS credentials from environment
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Set up AWS client for Bedrock (Nova Lite)
bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",  # Replace with your desired AWS region
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Define NewsAPI key (Ensure this is stored in your .env file)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Function to fetch news based on user input topics with refined queries
def get_news(query):
    # Clean up the query (replace spaces with '+' for URL compatibility)
    query = query.strip().replace(" ", "+")

    # Fetch articles for each individual keyword/topic entered by the user
    api_url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize=5"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        st.error("Failed to fetch news articles!")
        return []
    
    articles = response.json().get("articles", [])
    return articles  # Return raw articles for structured display

# Function to interact with Amazon Nova via Bedrock (for summarization)
def summarize_with_nova(articles):
    summaries = []
    
    for article in articles:
        # Summarize each article individually
        title = article['title']
        url = article['url']
        content = article.get('content', article.get('description', ''))
        
        prompt_data = f"Summarize the following article:\n\n{content}"
        
        # Prepare the message list without the 'type' field
        message_list = [
            {
                "role": "user",  # User input message
                "content": [
                    {
                        "text": prompt_data  # Content of the message
                    }
                ]
            }
        ]
        
        # Prepare the request body
        body = {
            "messages": message_list,
        }

        model_id = "us.amazon.nova-lite-v1:0"  # Correct model version for Nova Lite
        accept = "application/json"
        content_type = "application/json"
        
        # Function to invoke the model
        try:
            start_time = time.time()
            response = bedrock_runtime.invoke_model(
                body=json.dumps(body),
                modelId=model_id,
                accept=accept,
                contentType=content_type
            )
            elapsed_time = time.time() - start_time
            print(f"\n⏱️ Model invocation took {elapsed_time:.2f} seconds.")
            
            response_body = json.loads(response.get("body").read())
            # Extract and return the summarized response
            summary = response_body.get("output").get("message").get("content")[0].get("text")
            summaries.append({'title': title, 'summary': summary, 'url': url})
        
        except Exception as e:
            print(f"\n❌ Couldn't invoke {model_id}")
            print(f"Error: {e}")
            summaries.append({'title': title, 'summary': "Error: Could not generate summary.", 'url': url})
    
    return summaries

# Streamlit interface
def main():
    st.title("Personalized News Aggregator")

    # Ask user to input topics
    topics_input = st.text_input("What topics are you interested in learning about today? (e.g., architecture, finance, sports)")

    if st.button("Get Articles"):
        if topics_input:
            # Split the user input into separate topics (e.g., "architecture", "finance", "sports")
            topics = [topic.strip().lower() for topic in topics_input.split(",")]
            
            all_articles = []

            # Fetch news for each topic independently
            for topic in topics:
                articles = get_news(topic)
                all_articles.extend(articles)  # Add articles for each topic to the final list

            if all_articles:
                # Summarize articles with Amazon Nova
                summaries = summarize_with_nova(all_articles)

                if summaries:
                    # Display the summarized articles in a structured format
                    for summary in summaries:
                        st.write(f"### {summary['title']}")
                        st.write(f"**Summary:** {summary['summary']}")
                        st.write(f"[Read more]({summary['url']})")
                        st.markdown("---")
                else:
                    st.error("Error: Could not generate summaries.")
            else:
                st.warning("No articles found for the given topics.")
        else:
            st.warning("Please enter a topic to learn about.")

if __name__ == "__main__":
    main()
