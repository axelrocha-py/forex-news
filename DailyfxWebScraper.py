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
    next_button_link = soup.find('div', attrs={'class':'dfx-paginator d-flex w-100 dfx-font-size-3 font-weight-bold my-3'}).find('a', attrs={'class':'dfx-paginator__link ml-auto'}).get('href')

    return next_button_link


def get_news(soup):
    '''
    This function gets a soup
    and return all URLs of articles
    in this.
    '''
    news_list = []
    
    article_list = soup.find('div', attrs={'class':'dfx-articleList jsdfx-articleList'}).find_all('a')
    for article in article_list:
        news_list.append(article.get('href'))
    
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
    title = soup.find('h1', attrs={'class':'dfx-articleHead__header m-0'}).get_text()
    if title:
        news_dict['title'] = title
    else:
        news_dict['title'] = None
    
    #Get the date
    date = soup.find('div', attrs={'class':'dfx-articleHead__displayDate'}).get('data-time')
    if date:
        news_dict['date'] = date
    else:
        news_dict['date'] = None
        
    #Get the author
    try:
        author = soup.find('div', attrs={'class':'dfx-articleHead__articleDetails'}).find('a').get_text()
        if author:
            news_dict['author'] = author
        else:
            news_dict['author'] = None
    except:
        news_dict['author'] = soup.find('span', attrs={'class':'dfx-articleHead__authorName'}).get_text()
        pass

    #Get the body
    body = soup.find('div', attrs={'class':'dfx-articleBody__content'}).get_text()
    if body:
        news_dict['body'] = body
    else:
        news_dict['body'] = None
    
    return news_dict

def init_fx():

    url = 'https://www.dailyfx.com/espanol/noticias-trading/articulos'

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
    print('Scrape Dailyfx.com')
    print('--' * 10)
    for i, url in enumerate(links_news):
        print(f'Scrape article {i}/{len(links_news)}') 
        data.append(scrape_article(url))
        
    # Convert the data to CSV with Pandas
    df = pd.DataFrame(data)
    today = date.today()
    df.to_csv(f'/Users/samantha/Desktop/FN_2017/df_dailyfx_{today}.csv')

    return None