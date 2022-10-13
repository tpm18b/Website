import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"C:\Users\tmihe\Desktop\sqlite\db\pythonsqlite.db")




from flask import Flask, render_template
import requests
from operator import itemgetter

app = Flask(__name__)

@app.route('/')
def home():
    url = 'https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty'
    r = requests.get(url)
    r.text
    r.json()[0:1]

    article_ids = r.json()
    five_articles_dicts = [] 

    for article_id in article_ids[:10]: #change 10 to 202 for all articles
        url = 'https://hacker-news.firebaseio.com/v0/item/' + str(article_id) + '.json' # plug in looped id str(article_id)
        article_r = requests.get(url)
        one_article = article_r.json()
        five_articles_dict = {
        'Title': one_article['title'],
            'Discussion link': one_article['url'],
            'likes': one_article['score'],
            'id': article_id
        }
        five_articles_dicts.append(five_articles_dict)

    five_articles_dicts
    sorted_dict = sorted(five_articles_dicts, key=itemgetter('likes'), reverse=True)
    sorted_dict

    app
    for article in sorted_dict:
        print('\nTitle:', article['Title'])
        print('Discussion Link:', article['Discussion link'])
        print('likes:', article['likes'])
        print('id:', article['id'])
    return render_template('home-page.html', sorted_dict = sorted_dict)

@app.route('/login/')
def login():
    return render_template('login-page.html')

@app.route('/admin-login/')
def adminLogin():
    return render_template('adminLogin-page.html')

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=env.get("PORT", 3000))




    
    
  