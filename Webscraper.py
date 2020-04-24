import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class webscraper:
    def __init__(self, url, ):
        self.base_url = url
        self.year_identifyer = "..."
        self.month_identifyer = "..."
        self.day_identifyer = "..."
        self.year_first_number = 0
        self.month_first_number = 0
        self.day_first_number = 0
        self.year_last_number = 0
        self.month_last_number = 0
        self.day_last_number = 0
        self.tile_list = []
        self.tile_list_index = []
        self.product_list = []
        self.product_list_index = []


    def convert_url_to_soup(self, url):
        """
        method to convert a url to a useable format - BeautifulSoup
        :param url: The url, as a string, to be converted to soup
        :return: soup - a beautiful soup to be used
        """
        try:
            options = webdriver.FirefoxOptions()
            options.headless = True
            browser = webdriver.Firefox(options=options)
            browser.get(url)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
        finally:
            try:
                browser.close()
            except:
                pass
        return soup

    def find_the_urls(self, url, identifyer, index_of_first, index_of_last):
        """
        method that takes a url and finds all links below it. For example if the url pertains to a year then the method
        returns all the month related urls below that year
        :param url: the url to find, as a string
        :param identifyer: identifying class name of the urls we are looking for, a string, also a class name in html
        :param index_of_identifyer: a number, the first instance of an important url
        :return urllist: a list of urls 'underneath' the initial url
        """
        soup = self.convert_url_to_soup(url)
        list_of_class_tags = soup.findAll(identifyer)
        urllist = []
        for class_tag in list_of_class_tags[index_of_first:index_of_last]:
            suffix = class_tag['href']
            urllist.append('http://data.ceda.ac.uk' + suffix + '/catalog.html')
        print(urllist)
        return urllist

    def flatten(self, two_D_list):
        """
        method that takes a 2D array and flattens it into a 1D array in the natural way
        :param two_D_array:
        :return: A flattened 1D array
        """
        one_D = [j for sub_list in two_D_list for j in sub_list]
        return one_D

    def obtain_next_urls(self, urllist, identifyer, index_of_first, index_of_last):
        """
        follows the 'rabbit holes'. This method takes a list of urls and finds all of the urls that lie underneath that
        list. e.g if you have a list of year-type urls, then it will find all the month-type urls.
        :param urllist: the list of urls to be extended down a level
        :param identifyer: the identifying signature of the urls e.g an <a> tag. A list of same size as urllist
        :param index_of_identifyer: the first instance of the important information within the identifyers
        :return urllist: a complete list of all the urls.
        """
        for i in range(len(urllist)):
            urllist[i] = self.find_the_urls(urllist[i], identifyer, index_of_first, index_of_last)
        urllist = self.flatten(urllist)
        return urllist

    def main(self):
        """
        Calling all the functions to achieve the webscraping task
        :param identifyer_for_MOD11A1: identifyers for the data we are looking for.
        :param identifyer_for_MOD13A2:
        :param identifyer_for_MCD43A3:
        :param identifyer_for_h17v02: identifyers for the tiles that are of interest to us
        :param identifyer_for_h17v03:
        :param identifyer_for_h17v04:
        :param identifyer_for_h18v03:
        :return a complete list of urls to be downloaded:
        """
        urllist = []
        for index, product in enumerate(self.product_list):
            urllist.append(self.find_the_urls(self.base_url, product, self.product_list_index[index]))

            lftp - u jlewis005, GYP - -980 n - e "cd neodc/modis/data/MOD11A2/collection6;ls -lR;quit"
            ftp.ceda.ac.uk > MOD11A2.txt

        for index, url in enumerate(urllist):
            url = url.split('/')
            url.insert(len(url) - 1, 'collection6')
            urllist[index] = "/".join(url)

        urllist = self.obtain_next_urls(urllist, self.year_identifyer, self.year_identifying_number)
        urllist = self.obtain_next_urls(urllist, self.month_identifyer, self.month_identifying_number)
        urllist = self.obtain_next_urls(urllist, self.day_identifyer, self.day_identifying_number)
        urllist = self.find_the_urls(urllist, identifyer_for_h17v02)
        return urllist

jim = webscraper('http://dap.ceda.ac.uk/thredds/catalog/neodc/modis/data/')
assert jim.flatten([[1,2],[3,4]]) == [1,2,3,4], 'hasnt flattened correctly'
jim.convert_url_to_soup(jim.base_url)
jim.find_the_urls(jim.base_url, 'a', 0)

assert isinstance(jim.base_url, str)
