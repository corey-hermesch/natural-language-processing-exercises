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

# defining a function to get ALL codeup blogs' title and content
def get_all_codeup_blogs(start_url = 'https://codeup.com/blog/', fresh=False):
    """
    This function will
    - web scrape the title and content of all codeup blog articles
    - and save them to a locally cached json file
    - (OR read them from said json file)
    - return a list of dictionaries of the form:
        { 'title': title of the article
        , 'content': full text content of the article}
    """
    # see if cached file exists
    cache_file_name = 'codeup_blogs.json'
    if os.path.isfile(cache_file_name) and (not fresh):
        results_dict_list = json.load(open(cache_file_name))
        print ('cached file found and read')
        return results_dict_list
    
    # else go webscrape it 
    # initialize results
    results_dict_list = []
    # set my user-agent (this is the one from my computer/browser)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0'}
    # setup for the while loop:
    next_url = start_url
    
    # as long as there is an "Older Entries" link to follow, keep following it
    while True:
        # get the response from the next page of blog titles
        response = get(next_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # parse soup for all the blog post links that lead to actual blogs
        more_links = soup.find_all('a', class_='more-link')
        more_links = [link['href'] for link in more_links]
        
        # for each link, go get the title and content
        for link in more_links:
            # get dictionary of results for each url
            results_dict = get_title_content(link)
            results_dict_list.append(results_dict)

        # see if there is another link for Older Entries
        all_links = soup.select('a')
        # set a flag to decide whether to continue to while loop or not
        flag = False
        # brute force: check each link to see if it contains the text 'Older Entries'
        for link in all_links:
            if link.text.__contains__('Older Entries'):
                # if this is true, there is another link to follow; set it as next_url
                next_url = link['href']
                # and set flag to be True, then break out of this for loop
                flag = True
                continue
        # if flag is true, start over at the top of the while loop and scrape the next page of blogs        
        if flag: 
            continue
        # if flag was false, then we're done!
        break
        
    # write fresh results to cached file
    with open(cache_file_name, 'w') as cache:
        json.dump(results_dict_list, cache)
    print('web scraped and written to cached file')

    return results_dict_list
    
    

# defining a function to scrape inshorts.com's business/sports/technology/entertainment sections
def get_news_articles(fresh=False):
    """
    This function will
    - read in news articles from a locally cached file, news_articles.json if it exists;
    - if the cached file does not exist, or if fresh=True, this function will:
        - webscrape short news articles from inshorts.com
        - business, sports, technology, entertainment sections only
        - return a list of dictionaries of the form
            {'category': type of news (sports, tech, etc.)
            ,'title': title of article
            ,'content': contents of article}
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
                results_dict_list.append({'category':section, 'title':t, 'content':c})
        # write fresh results to cached file
        with open(cache_file_name, 'w') as cache:
            json.dump(results_dict_list, cache)
        print('web scraped and written to cached file')
        
        return results_dict_list
    
    