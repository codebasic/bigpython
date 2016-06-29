import os
import time

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

@pytest.mark.skip(reason='Not Implemented Yet')
def test_browser_select(webdriver):
    assert hasattr(webdriver, 'select')

def test_parse_html(webdriver):
    url = 'http://finance.naver.com/'
    webdriver.get(url)
    time.sleep(1)

    elem_kospi_index = webdriver.find_element_by_css_selector(".num_quot.up > .num")
    assert elem_kospi_index

    kospi_index = float(elem_kospi_index.text.replace(',',''))

def test_html_select(webdriver):
    assert hasattr(webscrap, 'HtmlSelect')

    target_url = 'file://' + os.path.dirname(os.path.abspath(__file__))
    target_url += '/data/forms.html'

    webdriver.get(target_url)
    time.sleep(3)

    elem_car_select = webdriver.find_element_by_name('cars')
    cars = webscrap.HtmlSelect(elem_car_select)

    value = 'porsche'
    cars.select_by_value("porsche")
    time.sleep(3)

    assert elem_car_select.get_attribute('value') == 'porsche'
