import Webscraper_BASH_method

CEDA_data = Webscraper_BASH_method.Webscraper('/workspace/webscraping/Config Webscraper_BASH_method.yaml')
CEDA_data.put_all_product_data_in_files()
CEDA_data.construct_urls()
CEDA_data.download_files()
print(CEDA_data.urllist)