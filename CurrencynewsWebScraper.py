import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

def get_soup(url): 
    '''
    This function gets an URL and
    return a BS object.
    '''
    url_req = requests.get(url)
    if url_req.status_code !=200:
        return None
    
    url_soup = BeautifulSoup(url_req.text, 'lxml')
    
    return url_soup


def find_url_soup(soup):
    '''
    This function gets a soup and
    find the specific next button
    link for each soup.
    '''
    next_button_soup = soup.find('div', attrs = {'class':'pagination'}).find_all('a')
    next_button_link = 'https://www.currencynews.co.uk' + next_button_soup[-1].get('href')

    return next_button_link


def get_news(soup):
    '''
    This function gets a soup
    and return all URLs of articles
    in this.
    '''
    news_list = []
    
    article_list = soup.find_all('div', attrs = {'class':'newshp-item'})
    for article in article_list:
        news_list.append('https://www.currencynews.co.uk' + article.find('p', attrs={'class':'link'}).find('a').get('href'))
    
    return news_list


def scrape_article(url):
    '''
    This function gets an URL,
    convert this URL to BS object
    and call to get_info function
    for each soup.
    '''
        
    try:
        article = requests.get(url)
    except Exception as e:
        print('Ops! We have an specific problem with: ', url) 
        print(e)
        return None
    
    if article.status_code !=200:
        print(f'Sorry human I can not get requests for {url}') 
        return None
    
    article_soup = BeautifulSoup(article.text, 'lxml')
    
    news_dict = get_info(article_soup)
    news_dict['url'] = url
    
    return news_dict


def get_info(soup):
    '''
    This function gets a soup
    and scrape it data to save
    it on news_dict.
    '''
    
    news_dict = {}
    
    # Get the title
    try:
        title = soup.find('div', attrs={'class':'newshp-item'}).find('h3').get_text()
        if title:
            news_dict['title'] = title
        else:
            news_dict['title'] = None
    except:
        news_dict['title'] = soup.find('div', attrs={'class':'newshp-item'}).find('h2').get_text()
    
    #Get the date
    date = soup.find('div', attrs={'class':'newshp-item'}).find('i').get_text()
    if date:
        news_dict['date'] = date
    else:
        news_dict['date'] = None
        
    #Get the author
    author = soup.find('div', attrs={'class':'newshp-item'}).find('a').get_text()
    if author:
        news_dict['author'] = author
    else:
        news_dict['author'] = None
    

    #Get the body
    body = soup.find('div', attrs={'class':'newshp-item'}).get_text()
    if body:
        news_dict['body'] = body
    else:
        news_dict['body'] = None
    
    return news_dict


def init_cn():

    url = 'https://www.currencynews.co.uk/'

    # Search all section links and get the soup for each one
    url_mod = url
    soups_for_sections = []

    for i in range(0, 15):
        s = get_soup(url_mod)
        soups_for_sections.append(s)
        url_mod = find_url_soup(s)
        
    # Gets all the news links for each section soup and save there on <<links_news>>
    links_news = []
    for soup in soups_for_sections:
        links_news.extend(get_news(soup))
        
    # Pass each link to scrape_article function for get article info and save there on <<data>>
    data = []
    print('--' * 10)
    print('Scrape Currency News.com')
    print('--' * 10)
    for i, url in enumerate(links_news):
        print(f'Scrape article {i}/{len(links_news)}') 
        data.append(scrape_article(url))
        
    # Convert the data to CSV with Pandas
    df = pd.DataFrame(data)
    today = date.today()
    df.to_csv(f'/Users/samantha/Desktop/FN_2017/df_currencynews_{today}.csv')

    return None