from robocorp.tasks import task
from RPA.FileSystem import FileSystem
from RPA.Browser.Selenium import Selenium
import logging
from selenium.webdriver.common.by import By

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
RESTAURANT_NAME_SELECTOR = "css:h1.compass-heading"
BASE_URL = "https://compass-group.fi"
LUNCH_MENU_PACKAGE = "css:.lunch-menu-block__menu-package"
LUNCH_NAME_SELECTOR = "h5.compass-heading"
MEALS_SELECTOR = "css:.lunch-menu-block__content--meals"

browser = Selenium()


# MAIN FUNCTION STARTS HERE
@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""
    try:
        clear_file()
        open_compass_website()
        decline_all_cookies()
        apply_filters()
        getLinks()
        browser.close_browser()
    except Exception as error:
        logging.error(f"An error occured: {str(error)}")
        browser.close_browser()


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


def getMenu(url):
    browser.go_to(url)
    browser.wait_until_element_is_visible(LUNCH_MENU_PACKAGE)
    menuPackages = browser.find_elements(LUNCH_MENU_PACKAGE)
    restaurantName = browser.get_text(RESTAURANT_NAME_SELECTOR)
    write_to_file(f" {restaurantName}\n")

    for menuPackage in menuPackages:
        menuNames = menuPackage.find_elements(By.CSS_SELECTOR, ".meal-item")
        menuName = browser.get_text(
            menuPackage.find_element(By.CSS_SELECTOR, ".compass-heading")
        )
        write_to_file(f"\n{menuName}\n")
        for menuName in menuNames:
            menu_name_text = browser.get_text(
                menuName.find_element(By.CSS_SELECTOR, ".compass-accordion")
            )
            write_to_file(f"{menu_name_text}\n")


def clear_file():
    fs = FileSystem()
    if fs.does_file_exist("output/lunchlist.txt"):
        fs.remove_file("output/lunchlist.txt")
        fs.create_file("output/lunchlist.txt", "Todays lunch! @ ")


def write_to_file(txtToAppend):
    fs = FileSystem()
    with open("output/lunchlist.txt", "a", encoding="utf-8") as file:
        file.write(txtToAppend)
