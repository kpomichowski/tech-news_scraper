from dtparser import DataParser
from scraper import WebScraper


# append links here
beststories = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"
newstories = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"

# Take the best stories data from hackernews and save them to the file
wb = WebScraper()
req = wb.get(beststories)
wb.content()
wb.json()

# Take the news stories from hackernews and save them to the json file

wb = WebScraper()
req = wb.get(newstories)
wb.content()
wb.json()
