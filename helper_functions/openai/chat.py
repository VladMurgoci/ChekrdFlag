import openai
from openai import OpenAI


with open('/Users/murguuu/Documents/Programming/ChekrdFlag/helper_functions/openai/key.txt', 'r') as file:
    key = file.read().rstrip()
client = OpenAI(api_key=key)
from helper_functions.scraping.news import get_news
from helper_functions.scraping.f1com import get_full_race_report, get_full_qualy_report
import os

def get_race_summary(year, race_id, race_name, driver):
    """
    Get a race summary that can be posted on twitter
    @param year: year of the race
    @param race_id: id of the race
    @param race_name: name of the race
    @param driver: selenium driver
    @return: race report string
    """
    report = get_full_race_report(year, race_id, driver)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Formula 1 AI reporter that posts on a twitter account."},
        {"role": "user", "content": f"Please summarize the {year} {race_name}, so you can post it on twitter, it must be at most 280 characters long: \n" + report},
    ],
    temperature=0.5)
    output = response.choices[0].message.content
    while len(output) > 280:
        output = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Formula 1 AI reporter that posts on a twitter account."},
            {"role": "user",
             "content": "Please try to cut down in the number of characters of this tweet, while keeping its information intact \n" + output},
        ],
        temperature=0.5)['choices'][0]['message']['content']
    return output

def get_qualy_summary(year, race_id, race_name, driver):
    report = get_full_qualy_report(year, race_id, driver)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Formula 1 AI reporter that posts on a twitter account."},
        {"role": "user", "content": f"Please summarize the {year} {race_name} qualifying session, so you can post it on twitter, it must be at most 280 characters long: \n" + report},
    ],
    temperature=0.5)
    output = response.choices[0].message.content
    while len(output) > 280:
        output = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Formula 1 AI reporter that posts on a twitter account."},
            {"role": "user",
             "content": "Please try to cut down in the number of characters of this tweet, while keeping its information intact \n" + output},
        ],
        temperature=0.8)['choices'][0]['message']['content']
    return output

def get_news_summary() -> str:
    """
    Get a summary of a news article
    @param news: headline, content, title, type
    @return:
    """
    news = get_news()
    if news is None:
        return None
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Formula 1 AI reporter that posts on a twitter account."},
        {"role": "user", "content": f"Please summarize the following news article, so you can post it on twitter, it must be at most 280 characters long: " +
                                    f"\nNews Headline: {news['headline']}" +
                                    f"\nNews Content:  + {news['content']}"}
    ],
    temperature=0.5)
    output = response.choices[0].message.content
    while len(output) > 280:
        output = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Formula 1 AI reporter that posts on a twitter account."},
            {"role": "user",
             "content": "Please try to cut down in the number of characters of this tweet, while keeping its information intact: \n" + output},
        ],
        temperature=0.5)['choices'][0]['message']['content']
    return output
