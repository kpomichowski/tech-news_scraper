import requests
import json
import os
from datetime import datetime

class DataParser:
    """ 
        DataParser extracts, clean the data, 
        load the data to the structurure (list of dictionaries),
        saves the list to a json file.
    """

    data = []
    news = []

    """ Parsing the data based on url """
    def __init__(self, request):
        self.request = request

    def __search_request(self):
        # Load the data to structure 
        self.data = json.loads(self.request.text)


    def __extract_news(self):
        
        # Lookup to resources in data structure
        if not self.data: 
            raise TypeError('Unexpected empty list.')

        filters = ['by', 'id', 'score', 'time', 'title', 'url']
        self.news = [None for x in range(len(self.data[:51]))]

        for index, value in enumerate(self.data[:51]):
            post_id = self.data.pop(index)
            # Retrieve the data from website
            print(f"[{datetime.utcnow().strftime('%d-%m-%Y %X')}] Fetched post: {index} - ID: {value}")
            req = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty')
            news_post = json.loads(req.text)
            self.news[index] = {key: value for key, value in news_post.items() if key in filters}
        

        # Convert the each time field from post, timestamp to UTC 
        for index in range(len(self.news)):
            post = self.news[index]
            timestamp = post.get('time')
            post['time'] = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %X')

        # Sort posts by score in descending order
        self.news = sorted(self.news, key=lambda k: k['score'], reverse=True)

        return self.news

    def to_json(self):
        # Extracts each occurence from dictionary news and save to json
        if not self.news:
            raise ValueError(f'News collection is empty! Nothing to JSONize.')
        
        # Load the file to the news folder
        if not os.path.exists('../news/'): 
            raise FileNotFoundError('Directory "news" does not exist.')
        
        if 'newstories' in self.request.url:
            f = open('../news/json_hackernews-news.json', 'w')
        elif 'beststories' in self.request.url:
            f = open('../news/json_hackernews-beststories.json', 'w')

        json.dump(self.news, f, indent=4, ensure_ascii=True)
        f.close()
        print(f'[{datetime.utcnow().strftime("%d-%m-%Y %X")}] Succesfully saved json file to news.')
            
    def read_content(self):

        # Searches and extracts the news
        self.__search_request()
        data = self.__extract_news()
        return data





