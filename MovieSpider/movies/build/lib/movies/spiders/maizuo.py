import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'maizuo_movies'
    allowed_domains = ['maizuo.com'] #过滤不在范围内的域名
    start_urls = ['http://m.maizuo.com/v5/#/films/nowPlaying']
    def parse(self, response):
        content = response.body
        f = open("movie_detail.html","wb+")
        f.write(content)
        f.close()
        #nodes = response.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[@class="movie-card-wrap"]')
    #     for node in nodes:
    #         next_url = node.css('a:nth-child(2)::attr(href)').extract_first("")
    #         print(next_url)
    #         if(next_url):
    #             yield Request(url=next_url, callback=self.parse_buyurl)  #http的request请求
    #
    #
    # def parse_buyurl(self, response):
    #     content = response.body
    #     f = open("taopiaopiao_detail.html","wb+")
    #     f.write(content)
    #     f.close()
    #     print('ok')