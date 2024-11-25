import tweepy
from selenium import webdriver

from helper_functions.internal.storage import read_from_storage_file
from helper_functions.scraping.scraping_utils import initialize_webdriver
from datetime import datetime
from datetime import timedelta
from helper_functions.openai.chat import get_race_summary, get_qualy_summary, get_news_summary
import fastf1 as ff1
from helper_functions.internal.race_storage import *

consumer_key = read_from_storage_file('consumer_key.txt', [])
consumer_secret = read_from_storage_file('consumer_secret.txt', [])
access_token = read_from_storage_file('access_token.txt', [])
access_token_secret = read_from_storage_file('access_token_secret.txt', [])
bearer_token = read_from_storage_file('bearer_token.txt', [])

client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret
                       )

def create_race_report_post():
    driver = initialize_webdriver()
    year = datetime.now().year
    current_date = datetime.now().date()
    n_races = len(ff1.get_event_schedule(year, include_testing=False))
    output = ''
    starting_race_id = get_current_race_idx(year)
    next_race_idx = starting_race_id
    for race_idx in range(starting_race_id, n_races):
        gp = ff1.get_event(year, race_idx)
        race_date = gp.get_session_date('R').to_pydatetime().date()
        if race_date == current_date or\
                race_date == current_date - timedelta(1):
            output = get_race_summary(year, race_idx, gp['EventName'], driver)
            next_race_idx = race_idx + 1
            break
    driver.quit()
    if output != '':
        fill_race(year, next_race_idx)
        print('POSTED RACE REPORT TWEET')

def create_qualy_report_post():
    driver = initialize_webdriver()
    year = datetime.now().year
    current_date = datetime.now().date()
    n_races = len(ff1.get_event_schedule(year, include_testing=False))
    output = ''
    starting_qualy_idx = get_current_qualy_idx(year)
    next_qualy_idx = starting_qualy_idx
    for qualy_idx in range(starting_qualy_idx, n_races):
        gp = ff1.get_event(year, qualy_idx)
        qualy_date = gp.get_session_date('Q').to_pydatetime().date()
        # if qualy_date == current_date or\
        #     qualy_date == current_date - timedelta(1):
        output = get_qualy_summary(year, qualy_idx, gp['EventName'], driver)
        next_qualy_idx = qualy_idx + 1
        break
    driver.quit()
    if output != '':
        fill_qualy(year, next_qualy_idx)
        print("POSTED QUALY REPORT TWEET")

def create_news_post():
    news = get_news_summary()
    if news is not None:
        news = news.strip('"').strip("'")
        client.create_tweet(text=news)
        current_time = datetime.now()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '../../'))
        file_path = os.path.join(project_root, 'storage', 'log.txt')
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write('')
        with open(file_path, 'a') as f:
            f.write(f"Posted news at {current_time}\n")
        print("POSTED NEWS TWEET")

