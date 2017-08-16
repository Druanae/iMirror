from app import app
from flask import render_template
from app import response_pool
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import webbrowser

ask = Ask(app, "/reddit_reader")

@app.route('/')
def blank():
    return render_template("blank.html")

@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/welcome')
def welcome():
    welcome_message = response_pool.randomResponse()
    return render_template("welcome.html", welcome_message = welcome_message)

@app.route('/menu')
def menu():
    return render_template("menu.html")


###alexa server

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)

@ask.intent("OpenDashboard")
def dashboard():
    text = 'Opening dashboard'
    webbrowser.open('http://0.0.0.0:5005/index')
    return statement(text)


def get_headlines():
    user_pass_dict = {'user': '',
                      'passwd': '',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles  




@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
