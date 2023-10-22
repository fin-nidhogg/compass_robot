from robocorp.tasks import task
from robocorp import browser


@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""
    browser.configure(
        slowmo=2000,
    )

    try:
        open_compass_website()
    except Exception as error:
        print(f"An error occured: {str(error)}")
    else:
        cookieMonster()
        apply_filters()
        getLinks()


def open_compass_website():
    """Navigate to compass website"""
    browser.goto("https://www.compass-group.fi/ravintolat-ja-ruokalistat/")


def cookieMonster():
    """Mercilessly decline all cookies"""
    page = browser.page()
    page.click("#declineButton")


def apply_filters():
    """apply search Helsinki and opiskelijaruokailu"""
    page = browser.page()
    page.click(".compass-label:nth-child(7) > .compass-checkbox")
    page.fill(".compass-input.search-input", "Helsinki")
    page.click("//button[contains(.,'Hae')]")

    # Click "Lataa lisää" until theres no more links to load
    while page.is_visible("//button[contains(.,'Lataa lis\u00e4\u00e4')]"):
        page.click("//button[contains(.,'Lataa lis\u00e4\u00e4')]")


def getLinks():
    """Reads all links and prints those bastards to the log"""
    full_urls = []
    page = browser.page()
    link_elements = page.query_selector_all("//a[contains(.,'Näytä ruokalista')]")

    # Loop through each link element and get hrefs
    for link_element in link_elements:
        full_url = "https://compass-group.fi" + link_element.get_attribute("href")
        full_urls.append(full_url)
        print(full_url)

    return full_urls


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
