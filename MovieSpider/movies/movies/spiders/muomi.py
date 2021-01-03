import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'muomi_movies'
    allowed_domains = ['nuomi.com'] #过滤不在范围内的域名
    start_urls = ['https://dianying.nuomi.com/movie/detail?movieId=96075']
    def parse(self, response):
        content = response.body
        f = open("nuomi_moives.html","wb+")
        f.write(content)
        f.close()