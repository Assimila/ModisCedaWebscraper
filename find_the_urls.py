import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


url = 'http://dap.ceda.ac.uk/thredds/catalog/neodc/modis/data/catalog.html'

def convert_url_to_soup(url):
    """
    method to convert a url to a useable format - BeautifulSoup
    :param url: The url As a string
    :return: soup - a beautiful sp...
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    finally:
        pass
    return soup

def flatten(two_D_list):
    """
    method that takes a 2D array and flattens it into a 1D array in the natural way
    :param two_D_array:
    :return: A flattened 1D array
    """
    one_D = [j for sub_list in two_D_list for j in sub_list]
    return one_D


def find_the_urls(url, identifyer, index_of_first, index_of_last):
    """
    method that takes a url and finds all links below it. For example if the url pertains to a year then the
    :param url:
    :param identifyer:
    :return: urllist
    """
    soup = convert_url_to_soup(url)
    list_of_class_tags = soup.findAll(identifyer)
    urllist = []
    for class_tag in list_of_class_tags[index_of_first:index_of_last]:
        suffix = class_tag['href']
        urllist.append(url[:-12] + suffix)
    return urllist

def obtain_next_urls(urllist, identifyer, index_of_first, index_of_last):
    """
    follows the 'rabbit holes'. This method takes a list of urls and finds all of the urls that lie underneath that
    list. e.g if you have a list of year-type urls, then it will find all the month-type urls.
    :param urllist: the list of urls to be extended down a level
    :param identifyer: the identifying signature of the urls e.g an <a> tag. A list of same size as urllist
    :param index_of_identifyer: the first instance of the important information within the identifyers
    :return urllist: a complete list of all the urls.
    """
    for i in range(len(urllist)):
        urllist[i] = find_the_urls(urllist[i], identifyer, index_of_first, index_of_last)
    urllist = flatten(urllist)
    return urllist

urllist = find_the_urls(url, 'a', 5, 6)

for index, url in enumerate(urllist):
    url = url.split('/')
    url.insert(len(url)-1, 'collection6')
    urllist[index] = "/".join(url)

start = time.time()

urllist = obtain_next_urls(urllist, 'a', 5, 6)
urllist = obtain_next_urls(urllist, 'a', 5, 6)
urllist = obtain_next_urls(urllist, 'a', 1, -4)
print("final stage")
urllist = obtain_next_urls(urllist, 'a', 5, 8)
print(urllist)

print(time.time() - start)
