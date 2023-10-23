from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
import logging

# Setting general variables
SLOWMODELAY = 1500
COMPASS_WEBSITE_URL = "https://www.compass-group.fi/ravintolat-ja-ruokalistat/"
DECLINE_BUTTON_SELECTOR = "css:#declineButton"
FILTER_SELECTOR = "css:.compass-label:nth-child(7) > .compass-checkbox"
SEARCH_INPUT_SELECTOR = "css:.compass-input.search-input"
SEARCH_TERM = "Helsinki"
SEARCH_BUTTON_SELECTOR = "xpath://button[contains(.,'Hae')]"
LOAD_MORE_BUTTON_SELECTOR = "xpath://button[contains(.,'Lataa lis\u00e4\u00e4')]"
RESTAURANT_LINK_SELECTOR = "xpath://a[contains(.,'N\u00e4yt\u00e4 ruokalista')]"
BASE_URL = "https://compass-group.fi"
H5SELECTOR = "css:h5.compass-heading"

browser = Selenium()


# MAIN FUNCTION STARTS HERE
@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""
    try:
        open_compass_website()
        decline_all_cookies()
        apply_filters()
        getLinks()
        getMenu(url)
    except Exception as error:
        logging.error(f"An error occured: {str(error)}")


# MAIN FUNCTION ENDS HERE


def open_compass_website():
    """Navigate to compass website"""
    browser.open_available_browser(COMPASS_WEBSITE_URL)
    browser.maximize_browser_window()


def decline_all_cookies():
    """Decline all cookies"""
    browser.click_element(DECLINE_BUTTON_SELECTOR)


def apply_filters():
    """apply search Helsinki and opiskelijaruokailu"""
    browser.wait_until_element_is_visible(FILTER_SELECTOR)
    browser.click_element(FILTER_SELECTOR)
    browser.input_text(SEARCH_INPUT_SELECTOR, SEARCH_TERM)
    browser.click_element(SEARCH_BUTTON_SELECTOR)

    # Click "Lataa lisää" until theres no more links to load
    while browser.is_element_visible(LOAD_MORE_BUTTON_SELECTOR):
        browser.click_element(LOAD_MORE_BUTTON_SELECTOR)


def getLinks():
    """Reads all links and prints those bastards to the log"""
    full_urls = []
    browser.wait_until_element_is_visible(FILTER_SELECTOR)
    link_elements = browser.find_elements(RESTAURANT_LINK_SELECTOR)

    # Loop through each link element and get hrefs
    for link_element in link_elements:
        full_url = BASE_URL + link_element.get_attribute("href")
        full_urls.append(full_url)
        logging.info(full_url)

    return full_urls


## VAIN TESTIIN PERKELE!
url = "https://www.compass-group.fi/ravintolat-ja-ruokalistat/foodco/kaupungit/espoo/a-bloc/"


def getMenu(url):
    browser.go_to(url)
    browser.wait_until_element_is_visible(H5SELECTOR)
    heading_elements = browser.find_elements(H5SELECTOR)
    heading_texts = [browser.get_text(heading) for heading in heading_elements]
    return heading_texts
