import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'daomeng_movies'
    allowed_domains = ['nexttix.net'] #过滤不在范围内的域名
    start_urls = ['https://ticket.nexttix.net/cinemas?movieid=1285486']
    def parse(self, response):
        content = response.body
        f = open("daomeng_detail.html","wb+")
        f.write(content)
        f.close()