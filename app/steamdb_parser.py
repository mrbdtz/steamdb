import csv
import time
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from proxy_finder import ProxyFinder

class SteamdbParser(object):
    def __init__(self):
        self.proxy = ProxyFinder()
        self.url_charts = 'https://steamdb.info/charts/'
        self.url_sellers = 'https://steamdb.info/topsellers/'
        self.file_charts = 'data/charts.csv'
        self.file_sellers = 'data/topsellers.csv'
        self.data_charts = None
        self.data_sellers = None

    def parse_data(self, url):
        res = requests.get(url, headers={'User-Agent':UserAgent().chrome}, proxies=self.proxy.active_proxy)
        time.sleep(2)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            return soup, res.status_code
        else: 
            return None, res.status_code

    def get_charts_data(self):
        soup, status_code = self.parse_data(self.url_charts)
        if status_code == 200:
            headers = ['Position', 'Name', 'Current', '24h Peak', 'All-Time Peak']
            all_data = []
            apps = soup.find_all("tr", {"class": "app"})
            for app in apps:
                name = app.find('a', href=True, string=True).text.strip()
                values = [int(v.text.replace(',','')) for v in app.find_all('td', attrs={'data-sort':True})]
                all_data.append(['"'+name+'"'] + values)
            all_data = sorted(all_data, key=lambda g: g[1], reverse=True)
            all_data = [[i+1] + all_data[i] for i in range(len(all_data))]
            all_data.insert(0, headers)
            self.data_charts = all_data
        else:
            pass
        return status_code

    def get_sellers_data(self):
        soup, status_code  = self.parse_data(self.url_sellers)
        if status_code == 200:
            headers = ['Position', 'Name', 'Developer', 'Release date', 'Tags']
            all_data = [headers]

            apps = soup.find_all("tr", {"class": "app"})
            for app in apps:
                position = app.find('td', class_='seller-pos').text.strip()
                name = app.find('a', class_='b').text.strip()
                developer = app.find('a', class_='b').parent.find_next_sibling().text.strip()
                release_date = app.find('a', class_='b').parent.find_next_sibling().find_next_sibling().text.strip()
                try:
                    tags = '; '.join([t.text for t in app.find('a', class_='b').parent.find_all('span')])
                except:
                    tags = ''
                all_data.append([position, '"'+name+'"', '"'+developer+'"', release_date, tags])
            self.data_sellers= all_data
        else:
            pass
        return status_code

    def save_to_csv(self, file_name):
        if file_name == self.file_charts:
            all_data = self.data_charts
        elif file_name == self.file_sellers:
            all_data = self.data_sellers
        if all_data is not None:
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(all_data)
            return 'data saved to csv'
        else:
            return 'no data to save'

    def get_and_save_charts(self):
        try:
            self.get_charts_data()
            res_message = self.save_to_csv(self.file_charts)
            return res_message
        except:
            pass

    def get_and_save_sellers(self):
        try:
            self.get_sellers_data()
            res_message = self.save_to_csv(self.file_sellers)
            return res_message
        except:
            pass