import datetime
import os
from concurrent.futures import ProcessPoolExecutor
import yaml


class Webscraper:
    def __init__(self, config_file):
        with open(config_file, 'r') as config:
            cfg = yaml.load(config)
        # data types that we want
        self.product_list = cfg['data_to_retrieve']['product_list']
        self.tile_list = cfg['data_to_retrieve']['tile_list']
        self.urllist = []
        # directory info
        self.root_directory = cfg["directory_data"]["root_directory"]
        self.data_directory = cfg["directory_data"]["data_directory"]
        # authentification info
        self.user = cfg["website_data"]["user"]
        self.password = cfg["website_data"]["password"]
        # urls we are interested in
        self.scrape_url = cfg['website_data']['url_to_scrape']
        self.dap_base_url = cfg["website_data"]["dap_base_url"]
        self.data_base_url = cfg["website_data"]["data_base_url"]
        self.collection = cfg["website_data"]["collection"]
        self.cookie = cfg["website_data"]["cookie"]
        self.authentification_ticket = cfg["website_data"]["auth_tkt"]

    def put_all_product_data_in_files(self):
        """
        A method to put all products given in the product list in
        the instantation of webscraper into their own files
        """
        for product in self.product_list:
            file_location = f'{self.data_directory}/{product}.txt'
            if (os.path.exists(file_location)):
                print(f'file {product}.txt already exists')
            else:
                # catch login errors with exception handling
                location = f'"cd {self.scrape_url[-17:]}/{product}{self.collection}'
                bash_command = f'lftp -u {self.user},' \
                               f'{self.password} ' \
                               f'-e {location}; ls -lR;quit"  ' \
                               f'ftp{self.dap_base_url[10:]} > ' \
                               f'{self.data_directory}'\
                               f'/{product}.txt'
                # eBYhWdi - 0
                # lftp - u jlewis005, password - e "cd
                # neodc/modis/data/MOD11A2/collection6;ls -lR;quit" ftp.ceda.ac.uk > MOD11A2.txt
                print(f'putting {product} data in file {product}.txt')
                os.popen(bash_command).read()
                print("data put in file")


    def convert_file_name_to_date(self, file_name):
        """
        Method to extract the date from a file whose name contains
        it's date within full stops.
        :param file_name: the name, from which to extract the date.
        A string
        :return date: A string. The date extracted, in the correct
        format
        """
        years = file_name.split('.')[1][1:5]
        days = file_name.split('.')[1][5:]
        date_string = f'{years}/{days}'
        datetime_obj = datetime.datetime.strptime(date_string, '%Y/%j')
        correct_format = datetime_obj.strftime('%Y/%m/%d')
        return correct_format


    def construct_urls(self):
        """
        Method to construct a url from the file name. Allows for
        downloading.
        :param file_name:  A string. The file name to convert to a
        url  to be downloaded.
        :param product: A string. The product to be used.
        :return urls: A string list. The list of urls to be
        downloaded - for this product.
        """
        for product in self.product_list:
            for tile in self.pick_tiles(product):
                # obtaining the file name without the extra information
                file_name = tile.split(' ')[-1][:-1]
                url = f'{self.scrape_url}{product}{self.collection}' \
                      f'/{self.convert_file_name_to_date(tile)}/{file_name}'
                self.urllist.append(url)
        return self.urllist

    def pick_tiles(self, product):
        """
        Method to sort through a .txt file and pick the data
        relating to the tiles in the tile list.
        :param product: the product for which to find the tiles
        :return relevant_tiles: a list of all the relevant tiles for
        a given product
        """
        relevant_tiles = []
        with open(f'{self.data_directory}/{product}.txt') as file:
            file_list = file.readlines()
            for line in file_list:
                for tile in self.tile_list:
                    if tile in line:
                        relevant_tiles.append(line)
        return(relevant_tiles)

    def download_files(self):

        with ProcessPoolExecutor(2) as executor:
           res = executor.map(self.download_file, self.urllist[0:10])

    def download_file(self, url):
        # getting the file name
        file_name = url.split('/')[-1]
        product = url.split('/')[9]
        data_dir = f'{self.scrape_url[-17:]}{product}{self.collection}/{self.convert_file_name_to_date(file_name)}'

        thredds_url = os.path.join(self.dap_base_url, 'thredds', 'fileServer', data_dir, file_name)
        data_url = os.path.join(self.data_base_url, data_dir)

        bash_command = (f'curl \'{thredds_url}\' '
            f'-o {self.data_directory}/{file_name} '
            f'-H \'Referer: {data_url}\' '
            f'-H \'Cookie: {self.cookie}'
            f'auth_tkt={self.authentification_ticket}'
            f'!{{\\\"userkey\\\": \\\"35335\\\"\\054 '
            f'\\\"accountid\\\": \\\"NotAssigned\\\"}}\"\'')

        os.popen(bash_command).read()




