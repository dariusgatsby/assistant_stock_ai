from dotenv import find_dotenv, load_dotenv
from newsapi import NewsApiClient
import os
import finnhub
import json
import requests
from bs4 import BeautifulSoup

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
STOCK_API_KEY = os.getenv("FINHUB_API_KEY")

fin_header = {"X+Finnhub-Token": STOCK_API_KEY}

newsapi = NewsApiClient(NEWS_API_KEY)
finnhub_client = finnhub.Client(api_key=STOCK_API_KEY)

def get_news(topic):
    news = newsapi.get_everything(
                        q=topic,
                        page_size=3,
                                    )

    return news


urls = []
j = 1
for i in news['articles']:
    url = i['url']
    urls.append(url)
    for url in urls:
        res = requests.get(url)
        if res.status_code == 200:
            html_content = res.text
            html_str = res.text

            with open(f"index{j}.html", 'w', encoding='utf-8') as file:
                file.write(html_content)
            print("yup")
            break
        else:
            print("Nope")

soup = BeautifulSoup(html_str, 'html.parser')

data = finnhub_client.company_basic_financials('AAPL', 'all')
with open("finnhub_data.json", "w") as file:
    json.dump(data, file, indent=4)

#topic = input("Enter a news topic: ")
#news = get_news(topic)
#articles = []
#blog_urls = []
#for i in news['articles']:
    # source = i['source']['name']
    # title = i["title"] 
    # content = i["content"]
 #   url = i['url']

    # item = f"Source: {source},\nTitle: {title},\nContent: {content},\nUrl: {url}\n\n"
    # articles.append(item)
  #  blog_urls.append(url)

#j = 1
#for url in blog_urls:
#        print(f"Fetching content from {url}...")
#        content = fetch_blog_content(url)
 #       if content:
            # Do something with the fetched content
  #          print(f"Content fetched successfully from {url}")
            # For demonstration, you can print the content
   #         with open(f"test_files/test_html{j}.txt", 'w') as file:
    #              file.write(content)
     #             j += 1
      #      print("\n")
       # else:
        #    print(f"Failed to fetch content from {url}")



