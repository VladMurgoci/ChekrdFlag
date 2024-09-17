import selenium.webdriver
from selenium.webdriver.common.by import By


def get_gp_link(year : int,
                race_id : int,
                driver : selenium.webdriver.Chrome):
    """
    Get the f1.com grand prix weekend link
    @param year: year of the season
    @param race_id: id of the race, starts from 1 on the website
    @param driver: selenium webdriver
    @return: f1.com link for the weekend overview
    """
    season_schedule_link = f"https://www.formula1.com/en/racing/{year}.html"
    driver.get(season_schedule_link)
    current_element = driver.find_element(By.XPATH, f"//legend[@class='card-title f1-uppercase f1-color--warmRed' and contains(text(), 'ROUND {race_id + 1}')]")
    # Find the parent element that contains the href attribute
    while True:
        parent_element = current_element.find_element(By.XPATH, "..")
        if parent_element.get_attribute("href"):
            break  # If found, break out of the loop
        current_element = parent_element

    # Get the href attribute value from the parent element
    href_value = parent_element.get_attribute("href")
    return href_value

def get_full_report(driver : selenium.webdriver.Chrome
                    , link : str):
    """
    Get the full f1 report
    @param year: year of the race
    @param race_id: id of the race, increment by 1 for the website
    @param driver: selenium webdriver
    @param link: link to the report
    @return: string containing f1 race report
    """
    driver.get(link)
    report = ""
    text_boxes = driver.find_elements(By.CLASS_NAME, "f1-article--rich-text")
    for textBox in text_boxes:
        # TODO: Extract header text, might be important
        paragraphs = textBox.find_elements(By.TAG_NAME, 'p')
        for paragraph in paragraphs:
            report += paragraph.text + "\n"
    driver.close()
    return report

def get_full_qualy_report(year : int,
                          race_id : int,
                          driver : selenium.webdriver.Chrome):
    """
    Get the qualifying report
    @param year: year of the qualy session
    @param race_id: id of the qualy
    @param driver: selenium webdriver
    @return: string report
    """
    driver.get(get_gp_link(year, race_id, driver))
    qualy_timetable_row = driver.find_element(By.XPATH,
                                         "//div[@class='row js-qualifying']")

    report_btn = qualy_timetable_row.find_elements(By.TAG_NAME, "a")[1]
    link = report_btn.get_attribute("href")
    return get_full_report(driver, link)

def get_full_race_report(year, race_id, driver):
    driver.get(get_gp_link(year, race_id, driver))
    report_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Report')]")
    parent_anchor_element = report_element.find_element(By.XPATH, ".//ancestor::a")
    href = parent_anchor_element.get_attribute("href")
    return get_full_report(driver, href)