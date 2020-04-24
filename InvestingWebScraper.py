import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

def get_news(soup):
    '''
    This function gets a soup and
    gives all the news URL that 
    contains each soup.
    '''
    
    news_list = []
    
    article_list = soup.find('div', attrs={'class':'largeTitle'}). find_all('article', attrs={'class':'js-article-item articleItem'})
    for article in article_list:
        if article.a:
            news_list.append('https://www.investing.com' + article.a.get('href'))
    
    return news_list

def scrape_article(url):
    '''
    This function gets an URL,
    convert this URL to BS object
    and call to get_info function
    for each soup.
    '''
        
    try:
        article = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    except Exception as e:
        print('Ops! We have an specific problem with: ', url) 
        print(e)
        return None
    
    if article.status_code != 200:
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
    title = soup.find('section', attrs={'id':'leftColumn'}).find('h1', attrs={'class':'articleHeader'}).get_text()
    if title:
        news_dict['title'] = title
    else:
        news_dict['title'] = None
    
    #Get the date
    date = soup.find('div', attrs={'class':'contentSectionDetails'}).find('span').get_text()
    if date:
        news_dict['date'] = date
    else:
        news_dict['date'] = None
        
    #Get the author
    author = soup.find('div', attrs={'class':'WYSIWYG articlePage'}).find('p').get_text()
    if author:
        news_dict['author'] = author
    else:
        news_dict['author'] = None

    #Get the body
    body = soup.find('div', attrs={'class':'WYSIWYG articlePage'}).get_text()
    if body:
        news_dict['body'] = body
    else:
        news_dict['body'] = None
    
    return news_dict

def init_in():

    url = 'https://www.investing.com/news/economy'

    investing_req = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})

    if investing_req.status_code !=200:
        print('Sorry human, I can not get requests from: ', url)

    investing_soup = BeautifulSoup(investing_req.text, 'lxml')

    # Gets all the section links on footer and save there on <<section_find>>
    section_find = investing_soup.find('div', attrs = {'class':'midDiv inlineblock'}).find_all('a', attrs={'class':'pagination'})

    # Complete all links
    section_links = []
    for i in range(0, len(section_find)):
        section_links.append('https://www.investing.com' + section_find[i].get('href'))
        if section_find[i].get('href') == 'javascript:void();':
            section_links[0] = url

    # Gets all the news links for each section links on footer and save there on <<links_news>>
    links_news = []
    for link in section_links:
        try:
            r = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'lxml')
                links_news.extend(get_news(soup)) 
            else:
                print('No se pudo obtener la sección', link) 
        except:
            print('No se pudo obtener la sección', link)

    # Pass each link to scrape_article function for get article info and save there on <<data>>
    data = []
    print('--' * 10)
    print('Scrape Investing.com')
    print('--' * 10)
    for i, url in enumerate(links_news):
        print(f'Scrape article {i}/{len(links_news)}')
        data.append(scrape_article(url))

    # Convert the data to CSV with Pandas
    df = pd.DataFrame(data)
    today = date.today()
    df.to_csv(f'/Users/samantha/Desktop/FN_2017/df_investing_{today}.csv')

    return None