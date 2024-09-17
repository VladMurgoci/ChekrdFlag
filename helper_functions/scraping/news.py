import requests
from datetime import date, datetime, timedelta
import os

url = "https://site.api.espn.com/apis/site/v2/sports/racing/f1/news"

def get_espn_articles():
    """
    Get a list of article descriptions from ESPN
    @return: list of news
    """
    response = requests.get(url)
    news = response.json()
    return [article for article in news['articles'] if article['type'] == 'HeadlineNews']

def get_news_from_date(date: date) -> list[dict]:
    """
    Get the news from a specific date
    @param date: date of the news
    @return: list of news
    """
    news = get_espn_articles()
    date_news = []
    for article in news:
        date_string = article['published']
        datetime_object = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        date_object = datetime_object.date()
        if date_object == date:
            date_news.append(article)

def get_article(link: str) -> dict:
    """
    Get the article from a link
    @param link: link to the article
    @return: article
    """
    response = requests.get(link)
    article = response.json()
    return article['headlines'][0]

def get_article_content(link: str) -> dict:
    """
    Get the content of an article
    @param link: link to the article
    @return: content of the article
    """
    article = get_article(link)
    article_content = {}
    article_content['headline'] = article['headline']
    article_content['title'] = article['title']
    article_content['content'] = article['story']
    article_content['type'] = article['type']
    article_content['link'] = link
    return article_content

def get_most_recent_article() -> dict:
    """
    Get the most recent article
    @return: most recent article
    """
    news = get_espn_articles()
    article_links = []
    for article in news:
        article_links.append((article['links']['api']['news']['href'], datetime.fromisoformat(article['published'].replace('Z', '+00:00'))))
    article_links.sort(key=lambda x: x[1], reverse=True)
    print(article_links)
    article_link = article_links[0][0]
    return get_article_content(article_link)


def mark_news_as_posted(link: str):
    """
    Mark the news as posted
    @param link: link to the article
    @param file: file to store the links
    @return: null
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../../'))
    file_path = os.path.join(project_root, 'storage', 'news.txt')
    with open(file_path, 'r') as f:
        links = f.readlines()
    new_link = link if link.endswith('\n') else link + '\n'
    links.insert(0, new_link)
    with open(file_path, 'w') as f:
        limit = min(30, len(links))
        f.writelines(links[:limit])

def was_news_posted(link: str) -> bool:
    """
    Check if the news was posted
    @param link: link to the article
    @param file: file to store the links
    @return: True if the news was posted, False otherwise
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../../'))
    file_path = os.path.join(project_root, 'storage', 'news.txt')
    with open(file_path, 'r') as f:
        links = [line.strip() for line in f.readlines()]
    return link.strip() in links

def get_news() -> dict:
    """
    Get the news
    @return: news
    """
    news = get_most_recent_article()
    print(news['headline'])
    if not was_news_posted(news['link']):
        print('Got new article!')
        mark_news_as_posted(news['link'])
        return news
    return None

if __name__ == "__main__":
    # Get the news
    news = get_news()
