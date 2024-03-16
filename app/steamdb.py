import requests
import csv

from scrapy.http import TextResponse, HtmlResponse
url = 'https://steamdb.info/charts/'
#res = requests.get(url)
from fake_useragent import UserAgent
res = requests.get(url, headers={'User-Agent':UserAgent().chrome})
resp = TextResponse(body=res.content, url=url)
#resp.xpath("//*[contains(text(), 'PUBG')]").getall()


if res.status_code == 200:
    apps_total = len(resp.css('tr.app').getall())
    print('data received, total apps: {}'.format(apps_total))

headers = [h for h in resp.css('th::text').extract() if (h != '#' and h !=' ')]
all_data = [headers]

apps = resp.css('tr.app')
for app in apps:
    all_data.append([x.replace(',','') for x in app.xpath('.//text()').extract() if (x !='\n' and x !='+')])


all_data[0]



file_name = 'topsellers.csv'
file_name = 'charts.csv'

def save_to_csv(file_name):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_data)


url = 'https://steamdb.info/topsellers/'
res = requests.get(url, headers={'User-Agent':UserAgent().chrome})
resp = TextResponse(body=res.content, url=url)


headers = [h for h in resp.css('th::text').extract() if h !=' ']
headers.insert(2,'last week')

all_data = [headers]

apps = resp.css('tr.app')
for app in apps:
    all_data.append([x.replace('\n','') for x in app.xpath('.//text()').extract() if x !='\n'])


from steamdb_parser import SteamdbParser

steamdb_parser = SteamdbParser()

steamdb_parser.get_charts_data()
steamdb_parser.get_sellers_data()

steamdb_parser.save_to_csv(steamdb_parser.file_sellers)
steamdb_parser.save_to_csv(steamdb_parser.file_charts)

steamdb_parser.get_and_save_charts()
steamdb_parser.get_and_save_sellers()

#How to install scrapy and splash
#https://zenrows.com/blog/scrapy-splash