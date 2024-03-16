import requests

from scrapy.http import TextResponse
url = 'https://steamdb.info/charts/'
res = requests.get(url)
from fake_useragent import UserAgent
res = requests.get(url, headers={'User-Agent':UserAgent().chrome})
resp = TextResponse(body=res.content, url=url)
resp.xpath("//*[contains(text(), 'PUBG')]").getall()
len(resp.css('tr.app').getall())


#How to install scrapy and splash
#https://zenrows.com/blog/scrapy-splash
