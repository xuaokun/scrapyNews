import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'txpc_movies'
    allowed_domains = ['txpc.cn'] #过滤不在范围内的域名
    start_urls = ['http://www.txpc.cn/index.html?city=110100']
    def parse(self, response):
        # content = response.body
        # f = open("txpc_detail.html","wb+")
        # f.write(content)
        # f.close()
        allmovies_url = response.css('body > div.page.index > div.container.panel.m-t-10.p-x-20.no-bottom-r.layer-1 > div.col-xs-9.p-x-0.p-r-16.left > div.row.panel-header.m-x-0 > div.col-xs-1.text-right.p-x-0.right > a.btn-more::attr(href)').extract_first()
        allmovies_url = parse.urljoin('http://www.txpc.cn/index.html?city=110100',allmovies_url)
        #print(allmovies_url)
        yield Request(url=allmovies_url, callback=self.parse_allmovies)  # http的request请求

    def parse_allmovies(self,response):
        # content = response.body
        # f = open("txpc_detail.html","wb+")
        # f.write(content)
        # f.close()
        single_movie_url = response.css('#hot_movie_tab > div.row.m-x-0.best-wrap > div.col-xs-9.p-l-40.content-wrap > div.row.m-x-0.bottom-part-wrap > div:nth-child(2) > div > a::attr(href)').extract_first()
        single_movie_url = parse.urljoin('http://www.txpc.cn/index.html?city=110100',single_movie_url)
        #print(single_movie_url)
        yield Request(url=single_movie_url, callback=self.parse_singlemovie)  # http的request请求


    def parse_singlemovie(self,response):
        # content = response.body
        # f = open("txpc_detail.html","wb+")
        # f.write(content)
        # f.close()
        scripts = response.xpath('//script/text()').extract()