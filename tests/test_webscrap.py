import os

import pytest
import selenium

from bigpython import webscrap

@pytest.fixture
def webdriver(request):
    driverpath = os.path.join('.', 'chromedriver')
    if not os.path.exists(driverpath):
        driverpath = webscrap.setup_webdriver(test=False)

    driver = webscrap.get_browser(driverpath=driverpath)
    request.addfinalizer(lambda: driver.quit())
    return driver

def test_get_browser(webdriver):
    assert type(webdriver) == selenium.webdriver.chrome.webdriver.WebDriver
    webdriver.quit()

def test_browser_select(webdriver):
    assert hasattr(webdriver, 'select')
