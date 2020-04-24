import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys



url = 'http://dap.ceda.ac.uk/thredds/catalog/neodc/modis/data/catalog.html'


def convert_url_to_soup(url):
    """
    method to convert a url to a useable format - BeautifulSoup
    :param url: The url As a string
    :return: soup - a beautiful sp...
    """
    try:
        options = webdriver.FirefoxOptions()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.get(url)
        print(browser.page_source)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
    finally:
        try:
            browser.close()
        except:
            pass
    return soup




convert_url_to_soup(url)