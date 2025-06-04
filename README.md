# Personalized News Aggregator

This is a personalized news aggregator built with Python and Streamlit. 
The application fetches news articles from the NewsAPI based on user-defined topics, summarizes them using AWS Nova Lite, and presents them in a structured and easy-to-read format. 
The goal of this project is to create an AI-powered tool that offers a personalized news reading experience.

## Features:
- Fetch news articles based on topics of the user's choice, like AI ethics, architecture, or art.
- Summarize the fetched articles using AWS Nova Lite (or HuggingFace transformers, depending on your choice).
- Display the news in a clean and structured format with titles, summaries, and links to the original articles.

## Requirements:
Before running this project, ensure you have Python 3.x installed. You can check this by running:

```bash
python --version

## Setup `.env` File:

In order for the application to access the necessary services (AWS and NewsAPI), you need to create a `.env` file in the root directory of the project.

1. Create a new file named `.env` in the root of the project.
   
2. Add the following keys to your `.env` file:

3. Make sure to replace the placeholder text (`your-aws-access-key-id`, `your-aws-secret-access-key`, and `your-news-api-key`) with your actual credentials.

### Important:

- **AWS Keys**: You can obtain your AWS credentials from your [AWS Management Console](https://console.aws.amazon.com/iam/home#/security_credentials).
- **NewsAPI Key**: You can obtain your NewsAPI key by signing up on [NewsAPI.org](https://newsapi.org/).

After setting up the `.env` file, the application will be able to access the necessary credentials and make API requests.
