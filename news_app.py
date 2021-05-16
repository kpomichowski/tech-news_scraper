import os
import random
from flask import Flask, render_template, json, request
from flask.views import View
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_paginate import Pagination, get_page_parameter

ROWS_PER_PAGE = 10

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    DEBUG=True,
    APPLICATION_ROOT=os.getcwd()
)

Bootstrap(app)


def get_json_file(news_type):
    if news_type == 'news':
        filename = os.path.join(app.config.get('APPLICATION_ROOT'),
                                'news', 'json_hackernews-news.json')
    elif news_type == 'beststories':
        filename = os.path.join(app.config.get('APPLICATION_ROOT'),
                                'news', 'json_hackernews-beststories.json')

    file = open(filename, 'r')
    data = json.load(file)

    return data


def randomize_data(news):
    return random.choices(news, k=3)


news = get_json_file('news')
beststories = get_json_file('beststories')


@app.route("/", methods=['GET'])
def main_page_news():
    data = randomize_data(news) + randomize_data(beststories)
    return render_template('base.html', data=data)


# Hacker news - newstories
@app.route('/hackernews/news', methods=['GET'])
def hackernews_news_page():
    data = news
    copy = None
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    if page == 1:
        copy = data[:ROWS_PER_PAGE]
    elif page == 2:
        copy = data[12: 12 + ROWS_PER_PAGE]
    elif page == 3:
        copy = data[22: 22 + ROWS_PER_PAGE]
    elif page == 4:
        copy = data[32: 32 + ROWS_PER_PAGE]
    elif page == 5:
        copy = data[42: 42 + ROWS_PER_PAGE]

    pagination = Pagination(page=page,
                            per_page=ROWS_PER_PAGE, total=len(data) - 1,
                            search=search, record_name='data', css_framework='foundation')
    return render_template('newstories.html', data=copy, pagination=pagination)

# Hacker news - beststories


@app.route('/hackernews/beststories', methods=['GET'])
def hacker_news_beststories_page():
    ...


# Render the navbar for bootstrap template
nav = Nav()

nav.register_element('top', Navbar(
    View('Home', 'main_page_news'),
    View('Hacker news', 'hackernews_news_page'),
    View('Hackernews - bestories', 'hacker_news_beststories_page')
))


nav.init_app(app)
