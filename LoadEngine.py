from sqlalchemy import create_engine
import pymysql
import pandas as pd
from datetime import date

def load_data():

    today = date.today()
    csv_charged = pd.read_csv(f'/Users/samantha/Desktop/FN_2017/{today}_NewsArticlesCleaned.csv')
    news_df = pd.DataFrame(csv_charged)

    # Create a list for each column in DataFrame
    news_id_list = []

    for i in range(0,len(news_df['news_id'])-1):
        news_id_list.append(news_df['news_id'][i])

    news_title_list = []

    for i in range(0,len(news_df['title'])-1):
        news_title_list.append(news_df['title'][i])
        
    news_date_list = []

    for i in range(0,len(news_df['date'])-1):
        news_date_list.append(news_df['date'][i])
        
    news_author_list = []

    for i in range(0,len(news_df['author'])-1):
        news_author_list.append(news_df['author'][i])
        
    news_body_list = []

    for i in range(0,len(news_df['body'])-1):
        news_body_list.append(news_df['body'][i])
        
    news_url_list = []

    for i in range(0,len(news_df['url'])-1):
        news_url_list.append(news_df['url'][i])
        
    news_host_list = []

    for i in range(0,len(news_df['host'])-1):
        news_host_list.append(news_df['host'][i])
        
    news_language_list = []

    for i in range(0,len(news_df['language'])-1):   
        news_language_list.append(news_df['language'][i])
        
        
    # Create a dictionary that contains all previous list
    data_dict = {'news_id': news_id_list,
                'title' : news_title_list,
                'date' : news_date_list,
                'author' : news_author_list,
                'body' : news_body_list,
                'url' : news_url_list,
                'host' : news_host_list,
                'language' : news_language_list
                }

    connection = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = '123456',
        db = 'news_fn2017'
    )

    tableName = "article_news_table"

    dataFrame = pd.DataFrame(data=data_dict)  

    engine = create_engine('mysql+pymysql://root:123456@localhost/news_fn2017')

    try:
        dataFrame.to_sql(tableName, con = engine, if_exists='fail')

    except ValueError as vx:
        print(vx)

    except Exception as ex:   
        print(ex)

    else:
        print(f'Table {tableName} created successfully.')   

    finally:
        connection.close()

    return None