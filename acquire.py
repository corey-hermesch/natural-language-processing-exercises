## IMPORTS
from requests import get
from bs4 import BeautifulSoup

import pandas as pd
import re

import os
import json

## FUNCTIONS
# defining a function to get a single web page's content from a codeup blog article
def get_title_content(url):
    """
    This function will
    - accept a string, url, which is thet web address for a single codeup blog article
    - return a dictionary with two elements:
        - 'title' : the title of the blog
        - 'content' : the text content of the article
    """
    # set my user-agent (this is the one from my computer/browser)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0'}
    # get a response
    response = get(url, headers=headers)
    # make a soup variable holding the reponse content
    soup = BeautifulSoup(response.content, 'html.parser')
    # get the title
    title = soup.find('title').get_text()
    # use the soup object and assign the text from the article to a variable
    article = soup.find('div', id='main-content').text
    # clean up what came back by removing all the \n characters and some extra stuff at the end
    article = article.replace('\n', ' ')
    regexp = r'(.+)Our ProgramsC'
    article = re.findall(regexp, article)
    article = article[0].strip()
    # assign results to a dictionary
    results_dict = {'title': title, 'content': article}
    return results_dict

# defining a function to get data from a list of urls which are codeup blog articles
def get_blog_articles(url_list):
    """
    This function will
    - accept a list of urls that are web addresses for codeup blog articles
    - return a list of dictionaries of the form
        {'title': title of blog, 'content': text of content of blog article}
    """
    results_list = []
    for url in url_list:
        # get dictionary of results for each url
        results_dict = get_title_content(url)
        results_list.append(results_dict)
        
    return results_list

# defining a function to scrape inshorts.com's business/sports/technology/entertainment sections
def get_news_articles(fresh=False):
    """
    This function will
    - read in news articles from a locally cached file, news_articles.json if it exists;
    - if the cached file does not exist, or if fresh=True, this function will:
        - webscrape short news articles from inshorts.com
        - business, sports, technology, entertainment sections only
        - return a list of dictionaries of the form
            {'title': title of article
            ,'content': contents of article
            ,'category': type of news (sports, tech, etc.)}
    """
    # see if cached file exists
    cache_file_name = 'news_articles.json'
    if os.path.isfile(cache_file_name) and (not fresh):
        results_dict_list = json.load(open(cache_file_name))
        print ('cached file found and read')
        return results_dict_list
    else:
        # initialize results variable, a list of dictionaries
        results_dict_list = []
        # set user-agent
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0'}
        # set url for inshorts
        url = 'https://inshorts.com/en/read/'
        # make list of sections
        news_section_list = ['business', 'sports', 'technology', 'entertainment']
        # now for each news_section, scrape from url + news_section
        for section in news_section_list:
            # get a response
            response = get(url+section, headers=headers)
            # make a soup variable holding the reponse content
            soup = BeautifulSoup(response.content, 'html.parser')
            # separate titles and contents out
            titles = soup.find_all('div', class_='news-card-title')
            contents = soup.find_all('div', class_='news-card-content')
            # for each element in title/contents, add it to our results
            for title, content in zip(titles, contents):
                t = title.span.text
                c = content.div.text
                results_dict_list.append({'title':t, 'content':c, 'category':section})
        # write fresh results to cached file
        with open(cache_file_name, 'w') as cache:
            json.dump(results_dict_list, cache)
        print('web scraped and written to cached file')
        
        return results_dict_list
    