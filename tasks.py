from robocorp.tasks import task
from robocorp import browser

@task
def compass_robot_tasks():
    """Open compass website and add relevant filters"""
    browser.configure(slowmo=1000,)
    open_compass_website()
    cookieMonster()
    getLinks()


def open_compass_website():
    """Navigate to compass website"""
    browser.goto("https://www.compass-group.fi/ravintolat-ja-ruokalistat/")


def cookieMonster():
    """Mercilessly decline all cookies"""
    page = browser.page()
    page.click('#declineButton')

def getLinks():
    """Reads all links and prints those bastards to the log"""
    page = browser.page()
    links = page.query_selector_all("//a[contains(.,'Näytä ruokalista')]")
    
    for link in links:
        link_value = link.get_attribute('href')
        print('https://compass-group.fi' + link_value)