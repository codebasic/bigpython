import os

import pytest
import selenium

from bigpython import webscrap

@pytest.fixture
def webdriver():
    driverpath = os.path.join('.', 'chromedriver')
    if not os.path.exists(driverpath):
        return webscrap.setup_webdriver(test=False)
    return driverpath

def test_get_browser(webdriver):
    print(webdriver)
    chrome = webscrap.get_browser(driverpath=webdriver)
    assert type(chrome) == selenium.webdriver.chrome.webdriver.WebDriver
    chrome.quit()
