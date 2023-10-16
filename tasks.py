from robocorp.tasks import task
from robocorp import browser


@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""
    browser.configure(
        slowmo=1000,
    )
    open_compass_website()
    cookieMonster()
    getLinks()


def open_compass_website():
    """Navigate to compass website"""
    browser.goto("https://www.compass-group.fi/ravintolat-ja-ruokalistat/")


def cookieMonster():
    """Mercilessly decline all cookies"""
    page = browser.page()
    page.click("#declineButton")


def getLinks():
    """Reads all links and prints those bastards to the log"""
    full_urls = []
    page = browser.page()
    link_elements = page.query_selector_all("//a[contains(.,'Näytä ruokalista')]")

    for link_element in link_elements:
        full_url = "https://compass-group.fi" + link_element.get_attribute("href")
        full_urls.append(full_url)
        print(full_url)

    return full_urls
