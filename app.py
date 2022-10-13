import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
import requests
from operator import itemgetter


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login/")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    url = 'https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty'
    r = requests.get(url)
    r.text
    r.json()[0:1]

    article_ids = r.json()
    five_articles_dicts = [] 

    for article_id in article_ids[:15]: #change 10 to 202 for all articles
        url = 'https://hacker-news.firebaseio.com/v0/item/' + str(article_id) + '.json' # plug in looped id str(article_id)
        article_r = requests.get(url)
        one_article = article_r.json()
        five_articles_dict = {
            'Title': one_article['title'],
            'Discussion link': one_article['url'],
            'likes': one_article['score'],
            'id': article_id,
            'comments': one_article['descendants']
        }
        five_articles_dicts.append(five_articles_dict)

    five_articles_dicts
    sorted_dict = sorted(five_articles_dicts, key=itemgetter('likes'), reverse=True)
    sorted_dict

    for article in sorted_dict:
        print('\nTitle:', article['Title'])
        print('Discussion Link:', article['Discussion link'])
        print('likes:', article['likes'])
        print('id:', article['id'])
    #return render_template('home-page.html', sorted_dict = sorted_dict)
    return render_template("home-page.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4), sorted_dict = sorted_dict)


if __name__ == "__main__":
    app.run()