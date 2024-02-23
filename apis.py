from dotenv import find_dotenv, load_dotenv
from newsapi import NewsApiClient
import os

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(NEWS_API_KEY)

def get_news():
    news = newsapi.get_everything(
                        q="nvidia",
                        page_size=3,
                                    )

    return news