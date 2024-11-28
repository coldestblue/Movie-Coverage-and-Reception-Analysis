import requests
import re
import json
from datetime import datetime, timedelta

NEWS_API_URL = "https://newsapi.org/v2/everything"
api_key = "0ecacbc8b79c42d08cf9fb1ba8f26014"
movies_keywords = '"Wicked" OR "Gladiator" OR "Red One" OR "Heretic" OR "Moana"'


def fetch_latest_news(api_key, movies_keywords, start_date, end_date):
 
    params = {
        "apiKey": api_key,
        "q": movies_keywords,
        "searchIn" : "title,description",
        "from": start_date,
        "to": end_date,
        "language": "en",
    }
    
    response = requests.get(NEWS_API_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching news: {response.status_code}")
    

    return response.json().get("articles", [])

def collect_data(api_key, movies_keywords, lookback_days=5):
    all_articles = []
    start_date = datetime.now() - timedelta(days=30)

    for i in range(6):
        from_date = (start_date + timedelta(lookback_days * i)).strftime("%Y-%m-%d")
        to_date = (start_date + timedelta(lookback_days * (i + 1)-1)).strftime("%Y-%m-%d")

        articles = fetch_latest_news(api_key, movies_keywords, from_date, to_date)
        all_articles.extend(articles)


    with open("movies_data.json", "w") as f:
        json.dump(all_articles, f)
    
    print(f"Total articles fetched: {len(all_articles)}")

collect_data(api_key, movies_keywords)

    
