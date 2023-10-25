from datetime import date
import time
from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Email.ImapSmtp import ImapSmtp
from RPA.FileSystem import FileSystem
from selenium.webdriver.common.by import By
import logging

# Setting general variables
SLOWMODELAY = 1500
COMPASS_WEBSITE_URL = "https://www.compass-group.fi/ravintolat-ja-ruokalistat/"
DECLINE_BUTTON_SELECTOR = "css:#declineButton"
FILTER_SELECTOR = "css:.compass-label:nth-child(7) > .compass-checkbox"
SEARCH_INPUT_SELECTOR = "css:.compass-input.search-input"
SEARCH_TERM = "Helsinki"
SEARCH_BUTTON_SELECTOR = "xpath://button[contains(.,'Hae')]"
LOAD_MORE_BUTTON_SELECTOR = "xpath://button[contains(.,'Lataa lisää')]"
RESTAURANT_LINK_SELECTOR = "xpath://a[contains(.,'Näytä ruokalista')]"
RESTAURANT_NAME_SELECTOR = "css:h1.compass-heading"
BASE_URL = "https://compass-group.fi"
LUNCH_MENU_PACKAGE = "css:.lunch-menu-block__menu-package"
LUNCH_NAME_SELECTOR = "h5.compass-heading"
MEALS_SELECTOR = "css:.lunch-menu-block__content--meals"
EMAIL_RECIPIENTS = ["olli.puustinen@student.laurea.fi"]

browser = Selenium()
fs = FileSystem()


# MAIN FUNCTION STARTS HERE
@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""

    try:
        open_compass_website()
        decline_all_cookies()
        apply_filters()
        clear_file()
        destinationUrls = getLinks()
        for destination in destinationUrls:
            try:
                getMenu(destination)
            except:
                pass

        send_html_email()
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
    time.sleep(3)
    # Click "Lataa lisää" until theres no more links to load
    while browser.is_element_visible(LOAD_MORE_BUTTON_SELECTOR):
        browser.click_element(LOAD_MORE_BUTTON_SELECTOR)
        time.sleep(5)


def getLinks():
    """Reads all links and returns array of full urls"""
    full_urls = []
    browser.wait_until_element_is_visible(RESTAURANT_LINK_SELECTOR)
    link_elements = browser.find_elements(RESTAURANT_LINK_SELECTOR)

    # Loop through each link element and get hrefs
    for link_element in link_elements:
        url = link_element.get_attribute("href")
        full_urls.append(url)
        logging.info(url)
    return full_urls


def getMenu(url):
    """Scrapes lunch info from given restaurant url"""
    try:
        # Browse to given url passed as argument
        browser.go_to(url)

        # Wait until all nessessary info is visible
        browser.wait_until_element_is_visible(LUNCH_MENU_PACKAGE)

        # Get high level menu packages into iterable menuPackages.
        # Scrape and write name of restaurant into temp file.
        menuPackages = browser.find_elements(LUNCH_MENU_PACKAGE)
        restaurantName = browser.get_text(RESTAURANT_NAME_SELECTOR)
        write_to_file(
            f"<h3 style=font-family:Montserrat; style=font-size:20 px;>Ravintola: {restaurantName}</h3>\n"
        )

        # Loop through menuPackages and get different menus as a child list.
        # Iterate through menuPackages list and get heading
        for menuPackage in menuPackages:
            menuName = browser.get_text(
                menuPackage.find_element(By.CSS_SELECTOR, ".compass-heading")
            )
            menuPrice = browser.get_text(
                menuPackage.find_element(By.CSS_SELECTOR, ".compass-text")
            )

            # Write H5 and price in the file
            write_to_file(
                f"<h5 style=font-family:Montserrat; style=font-size:18 px;><b>{menuName}</b><br><i>{menuPrice}</i></h5>"
            )

            # Get meal names and write those into file
            mealItems = menuPackage.find_elements(By.CSS_SELECTOR, ".compass-accordion")
            for mealItem in mealItems:
                mealName = browser.get_text(
                    mealItem.find_element(By.CSS_SELECTOR, "span.compass-text")
                )

                mealDiet = browser.get_text(mealItem.find_element(By.TAG_NAME, "p"))

                write_to_file(
                    f"<ul style=font-family:Montserrat; style=font-size:16 px;><b>{mealName}</b><br><i style=font-size:14 px;>{mealDiet}</i></ul>"
                )
    except Exception as error:
        write_to_file(
            f"An error occured while getting info from: {url}\n Error: {str(error)}"
        )
        logging.error(f"An error occured: {str(error)}")
        pass


def clear_file():
    if fs.does_file_exist("output/lunchlist.html"):
        fs.remove_file("output/lunchlist.html")
    fs.create_file("output/lunchlist.html")


def write_to_file(txtToAppend):
    with open("output/lunchlist.html", "a", encoding="utf-8") as file:
        file.write(txtToAppend)


def send_html_email():
    # Create an instance of the ImapSmtp class
    mail = ImapSmtp()

    # Read html payload
    payload = fs.read_file("output/lunchlist.html")
    # Configure SMTP server settings. Normally these would be located hidden.
    mail.account = "compasrobot@gmail.com"
    mail.password = "nohnpuggskupcqdi"
    mail.smtp_server = "smtp.gmail.com"
    mail.smtp_port = 587
    mail.smtp_starttls = True

    # Authenticate with the SMTP server
    mail.authorize_smtp()

    # Send an email
    mail.send_message(
        "compasrobot@gmail.com",
        EMAIL_RECIPIENTS,
        f"Päivän ruokalistat olkaa hyvä ({date.today()})",
        payload,
        html=True,
    )
