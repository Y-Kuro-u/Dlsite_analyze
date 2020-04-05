import time
import json
import requests
import os
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, output_directory='./data', sleep_time=1.):
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        self.output_directory = output_directory
        self.sleep_time = sleep_time

    def get_bs(self,url,encoding = None):
        time.sleep(self.sleep_time)
        response = requests.get(url)
        if encoding:
            response.encoding = encoding
        return BeautifulSoup(response.text, features='html.parser')

    def output(self, output_list, file_name):
        with open(os.path.join(self.output_directory, file_name), 'w') as f:
            json.dump(output_list, f, ensure_ascii=False)