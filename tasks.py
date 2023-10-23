from robocorp.tasks import task
from robocorp import browser
import logging

# Setting general variables
SLOWMODELAY = 500
COMPASS_WEBSITE_URL = "https://www.compass-group.fi/ravintolat-ja-ruokalistat/"
DECLINE_BUTTON_SELECTOR = "#declineButton"
FILTER_SELECTOR = ".compass-label:nth-child(7) > .compass-checkbox"
SEARCH_INPUT_SELECTOR = ".compass-input.search-input"
SEARCH_TERM = "Helsinki"
SEARCH_BUTTON_SELECTOR = "//button[contains(.,'Hae')]"
LOAD_MORE_BUTTON_SELECTOR = "//button[contains(.,'Lataa lis\u00e4\u00e4')]"
RESTAURANT_LINK_SELECTOR = "//a[contains(.,'Näytä ruokalista')]"
BASE_URL = "https://compass-group.fi"


@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""
    browser.configure(
        slowmo=SLOWMODELAY,
    )

    try:
        open_compass_website()
        decline_all_cookies()
        apply_filters()
        getLinks()
    except Exception as error:
        logging.error(f"An error occured: {str(error)}")


def open_compass_website():
    """Navigate to compass website"""
    browser.goto(COMPASS_WEBSITE_URL)
    page = browser.page()


def decline_all_cookies():
    """Decline all cookies"""
    page = browser.page()
    page.click(DECLINE_BUTTON_SELECTOR)


def apply_filters():
    """apply search Helsinki and opiskelijaruokailu"""
    page = browser.page()
    page.click(FILTER_SELECTOR)
    page.fill(SEARCH_INPUT_SELECTOR, SEARCH_TERM)
    page.click(SEARCH_BUTTON_SELECTOR)

    # Click "Lataa lisää" until theres no more links to load
    while page.is_visible(LOAD_MORE_BUTTON_SELECTOR):
        page.click(LOAD_MORE_BUTTON_SELECTOR)


def getLinks():
    """Reads all links and prints those bastards to the log"""
    full_urls = []
    page = browser.page()
    link_elements = page.query_selector_all(RESTAURANT_LINK_SELECTOR)

    # Loop through each link element and get hrefs
    for link_element in link_elements:
        full_url = BASE_URL + link_element.get_attribute("href")
        full_urls.append(full_url)
        logging.info(full_url)

    return full_urls

for url in full_urls

        from RPA.Browser.Selenium import Selenium
        from typing import List


            class Lunch:
                def __init__(self, heading: str, spans: List[str]):
                    self.heading = heading
                    self.spans = spans

                def add_spans(self, value: str):
                    self.spans.append(value)


            def create_lunch_objects(url: str) -> List[Lunch]:
                browser = Selenium()
                browser.open_available_browser(url)

                lunch_objects = []
                menu_packages = browser.find_elements("css:.lunch-menu-block__menu-package")

                for package in menu_packages:
                    heading = browser.find_element("css:h5.compass-heading", package).text
                    spans = browser.find_elements("css:span.compass-text", package)
                    spans = [span.text for span in spans]

                    lunch = Lunch(heading, spans)
                    lunch_objects.append(lunch)

                browser.close_browser()

                return lunch_objects


create_lunch_objects()


from RPA.Browser.Selenium import Selenium

class Lunch:
    def __init__(self, heading):
        self.heading = heading
        self.spans = []

    def add_spans(self, span):
        self.spans.append(span)

def get_lunch_menu(url):
    browser = Selenium()
    browser.open_available_browser(url)

    menu_elements = browser.find_elements('css:lunch-menu-block__menu-package')
    lunch_list = []

    for element in menu_elements:
        heading = browser.find_element('css:H5.compass-heading', parent=element).text
        lunch = Lunch(heading)

        span_elements = browser.find_elements('css:span.compass-text', parent=element)
        for span in span_elements:
            lunch.add_spans(span.text)

        lunch_list.append(lunch)

    browser.close_browser()

    return lunch_list