import selenium.webdriver as webdriver
from helper_functions.twitter.postreports import create_race_report_post, create_qualy_report_post, create_news_post
from helper_functions.scraping.f1com import get_full_qualy_report, get_full_race_report


def main():
    create_news_post()

if __name__ == "__main__":
    main()


