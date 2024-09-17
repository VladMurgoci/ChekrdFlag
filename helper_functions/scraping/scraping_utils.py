from selenium import webdriver

def initialize_webdriver() -> webdriver.Chrome:
    """
    Return an initialized chrome webdriver
    @return: Chrome webdriver
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=chrome_options)