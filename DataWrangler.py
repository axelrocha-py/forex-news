import pandas as pd
from datetime import date
import hashlib
from urllib.parse import urlparse

def fx_cleaning(daily_fx):
    '''
    This function gets a dirty Pandas 
    object and return a cleaned DataFrame
    about DailyFx News.
    '''
    # Delete Unnamed column
    daily_fx_mod = daily_fx.drop(['Unnamed: 0'], axis=1)

    # Create an unique id for each article using hashlib
    news_ids = (daily_fx_mod
        .apply(lambda row : hashlib.md5(bytes(row['url'].encode())) , axis=1)
        .apply(lambda hash_object : hash_object.hexdigest())
    )

    daily_fx_mod['news_id'] = news_ids
    daily_fx_mod.set_index('news_id', inplace=True)

    # Author cleaning
    stripped_author =(daily_fx_mod
                        .apply(lambda row : row['author'], axis = 1)
                        .apply(lambda author : list(author))
                        .apply(lambda letters: list(map(lambda letter : letter.replace('\n', ''), letters)))
                        .apply(lambda letters: list(map(lambda letter : letter.replace(',', ''), letters)))
                        .apply(lambda letters: ''.join(letters))
                        .apply(lambda letters: letters.strip())
    )

    daily_fx_mod['author'] = stripped_author

    # Body cleaning
    stripped_body =(daily_fx_mod
                        .apply(lambda row : row['body'], axis = 1)
                        .apply(lambda body : list(body))
                        .apply(lambda letters : list(map(lambda letter : letter.replace('\n', ''), letters)))
                        .apply(lambda letters : ''.join(letters))
    )

    daily_fx_mod['body'] = stripped_body

    # Date cleaning
    date_format =(daily_fx_mod
                        .apply(lambda row : row['date'], axis = 1)
                        .apply(lambda date : list(date))
                        .apply(lambda date : date[:10])
                        .apply(lambda date : ''.join(date))

    )

    daily_fx_mod['date'] = date_format
    daily_fx_mod['date'] = pd.to_datetime(daily_fx_mod['date'], infer_datetime_format=True)

    # Create host column
    daily_fx_mod['host'] = daily_fx_mod['url'].apply(lambda url : urlparse(url).netloc)

    # Create language column
    daily_fx_mod['language'] = 'ESP'
    
    return daily_fx_mod


def identify(lista):
    '''
    This is a secondary function
    for help cleaning investing function.
    Gets a word's list and itterate each
    word searching from specific words.
    '''
    i = 0
    while i >= 0 and i<= len(lista)-1:
        if comparation(lista[i]) == 'next_word':
            i += 1
        elif comparation(lista[i]) == 'Bloomberg':
            return 'Bloomberg'
        elif comparation(lista[i]) == 'Reuters':
            return 'Reuters'
        elif comparation(lista[i]) == 'surplus_text':
            author = lista[i][:2]
            author_cor = ' '.join(author)
            return author_cor
    return ' '.join(lista)

def comparation(word):
    '''
    This is the second part of the help
    cleaning function. In this we can find
    the words that our function is looking
    for.
    '''        
    if word == '(Bloomberg)' or word == '(Bloomberg' or word == 'Bloomberg':
        return 'Bloomberg'
    elif word == '(Reuters)':
        return 'Reuters'
    elif word == 'Equipo' or word == '-':
        return 'surplus_text'
    else:
        return 'next_word'

def in_cleaning(investing):
    # Delete Unnamed column
    investing_mod = investing.drop(['Unnamed: 0'], axis=1)

    # Create an unique id for each article using hashlib
    news_ids = (investing_mod
        .apply(lambda row : hashlib.md5(bytes(row['url'].encode())) , axis=1)
        .apply(lambda hash_object : hash_object.hexdigest())
    )

    investing_mod['news_id'] = news_ids
    investing_mod.set_index('news_id', inplace=True)

    # Author cleaning
    stripped_author_in =(investing_mod
                        .apply(lambda row : row['author'], axis = 1)
                        .apply(lambda author : author.split())
                        .apply(lambda words: list(map(lambda word : word.replace('By', ''), words)))
                        .apply(lambda words: ' '.join(words))
                        .apply(lambda author : author.split())
                        .apply(lambda author: identify(author))
                        )

    investing_mod['author'] = stripped_author_in

    # Body cleaning
    stripped_body_in =(investing_mod
                        .apply(lambda row : row['body'], axis = 1)
                        .apply(lambda body : list(body))
                        .apply(lambda letters : list(map(lambda letter : letter.replace('\n', ''), letters)))
                        .apply(lambda letters : list(map(lambda letter : letter.replace('©', ''), letters)))
                        .apply(lambda letters : ''.join(letters))
                        .apply(lambda words: words.split())
                        .apply(lambda words : list(map(lambda word : word.replace('Reuters.', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('Bloomberg.', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('FILE', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('PHOTO', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('(Reuters)', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('Investing.com', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('By', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('-', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace(':', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('2/2', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('10/10', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('3/3', ''), words)))
                        .apply(lambda words : list(map(lambda word : word.replace('18/18', ''), words)))
                        .apply(lambda words: ' '.join(words))
                        .apply(lambda words: words.strip())
    )

    investing_mod['body'] = stripped_body_in

    # Date cleaning
    date_format_in =(investing_mod
                        .apply(lambda row : row['date'], axis = 1)
                        .apply(lambda date : date[-25:])
                        .apply(lambda date : list(date))
                        .apply(lambda letters : list(map(lambda letter : letter.replace('(', ''), letters)))
                        .apply(lambda letters : list(map(lambda letter : letter.replace(')', ''), letters)))
                        .apply(lambda words: ''.join(words))
                        .apply(lambda words: words.strip())
                        .apply(lambda words : words[-25:-11])

    )

    investing_mod['date'] = date_format_in
    investing_mod['date'] = pd.to_datetime(investing_mod['date'], infer_datetime_format=True)

    # Create host column
    investing_mod['host'] = investing_mod['url'].apply(lambda url : urlparse(url).netloc)

    # Create language column
    investing_mod['language'] = 'ENG'
    
    return investing_mod


def cn_cleaning(currency_news):
    # Delete Unnamed column
    currency_news_mod = currency_news.drop(['Unnamed: 0'], axis=1)

    # Create an unique id for each article using hashlib
    news_ids = (currency_news_mod
        .apply(lambda row : hashlib.md5(bytes(row['url'].encode())) , axis=1)
        .apply(lambda hash_object : hash_object.hexdigest())
    )

    currency_news_mod['news_id'] = news_ids
    currency_news_mod.set_index('news_id', inplace=True)

    # Author cleaning (not neccesary for this dataframe)

    # Body cleaning
    stripped_body_cn =(currency_news_mod
                        .apply(lambda row : row['body'], axis = 1)
                        .apply(lambda words: words.split())
                        .apply(lambda words: words[10:])
                        .apply(lambda words: ' '.join(words))
                        .apply(lambda letters: list(letters))
                        .apply(lambda letters : list(map(lambda letter : letter.replace('\n', ''), letters)))
                        .apply(lambda letters : list(map(lambda letter : letter.replace('\r', ''), letters)))
                        .apply(lambda letters: ''.join(letters))
    )

    currency_news_mod['body'] = stripped_body_cn

    # Date cleaning
    date_format_cn =(currency_news_mod
                        .apply(lambda row : row['date'], axis = 1)
                        .apply(lambda words: words.split())
                        .apply(lambda words: words[:3])
                        .apply(lambda words: ' '.join(words))


    )

    currency_news_mod['date'] = date_format_cn
    currency_news_mod['date'] = pd.to_datetime(currency_news_mod['date'], infer_datetime_format=True)

    # Create host column
    currency_news_mod['host'] = currency_news_mod['url'].apply(lambda url : urlparse(url).netloc)

    # Create language column
    currency_news_mod['language'] = 'ENG'
    
    return currency_news_mod


def clean_data():

    today = date.today()

    try:
        daily_fx = pd.read_csv(f'/Users/samantha/Desktop/FN_2017/df_dailyfx_{today}.csv')
        investing = pd.read_csv(f'/Users/samantha/Desktop/FN_2017/df_investing_{today}.csv')
        currency_news = pd.read_csv(f'/Users/samantha/Desktop/FN_2017/df_currencynews_{today}.csv')

    except:
        print('Stop human! Verify the date of your csv files')
        
    df_fx_clean = fx_cleaning(daily_fx)
    df_in_clean = in_cleaning(investing)
    df_cn_clean = cn_cleaning(currency_news)

    # Unify our three dataframes in one and export like CSV file
    final_df = pd.concat([df_fx_clean, df_in_clean, df_cn_clean], axis=0)
    final_df.to_csv(f'/Users/samantha/Desktop/FN_2017/{today}_NewsArticlesCleaned.csv')

    return None