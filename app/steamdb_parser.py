import csv
import time
import requests
from scrapy.http import TextResponse
from fake_useragent import UserAgent

class SteamdbParser(object):
    def __init__(self):
        self.url_charts = 'https://steamdb.info/charts/'
        self.url_sellers = 'https://steamdb.info/topsellers/'
        self.file_charts = 'data/charts.csv'
        self.file_sellers = 'data/topsellers.csv'
        self.data_charts = None
        self.data_sellers = None

    def parse_data(self, url):
        for i in range(5): #5 attempt to parse page
            res = requests.get(url, headers={'User-Agent':UserAgent().chrome})
            resp = TextResponse(body=res.content, url=url)
            time.sleep(2)

            if res.status_code == 200:
                apps_total = len(resp.css('tr.app').getall())
                print('data received, total apps: {}'.format(apps_total))
                return resp
            else: 
                print('status code: ',res.status_code)
                time.sleep(8) # pause between atempts
        print('cant get data, try later')

    def get_charts_data(self):
        resp = self.parse_data(self.url_charts)
        headers = [h for h in resp.css('th::text').extract() if (h != '#' and h !=' ')]
        all_data = [headers]

        apps = resp.css('tr.app')
        for app in apps:
            all_data.append([x.replace(',','') for x in app.xpath('.//text()').extract() if (x !='\n' and x !='+')])
        self.data_charts = all_data

    def get_sellers_data(self):
        resp = self.parse_data(self.url_sellers)
        headers = [h for h in resp.css('th::text').extract() if h !=' ']
        headers.insert(2,'last week')

        all_data = [headers]

        apps = resp.css('tr.app')
        for app in apps:
            all_data.append([x.replace('\n','') for x in app.xpath('.//text()').extract() if x !='\n'])
        self.data_sellers= all_data

    def save_to_csv(self, file_name):
        if file_name == self.file_charts:
            all_data = self.data_charts
        elif file_name == self.file_sellers:
            all_data = self.data_sellers
        if all_data is not None:
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(all_data)
            print('data saved to csv')
        else:
            print('no data to save')

    def get_and_save_charts(self):
        try:
            self.get_charts_data()
            self.save_to_csv(self.file_charts)
        except:
            pass

    def get_and_save_sellers(self):
        try:
            self.get_sellers_data()
            self.save_to_csv(self.file_sellers)
        except:
            pass

