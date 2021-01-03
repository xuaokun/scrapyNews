# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'maoyan_movies'
    allowed_domains = ['maoyan.com'] #过滤不在范围内的域名
    start_urls = ['https://maoyan.com/films?showType=1&offset=0','https://maoyan.com/films?showType=1&offset=30','https://maoyan.com/films?showType=1&offset=60']
    def parse(self, response):
        content = response.body
        # f = open("movie_detail.html","wb+")
        # f.write(content)
        # f.close()
        nodes = response.xpath('//div[@class="channel-detail movie-item-title"]')
        for node in nodes:
            next_url = node.css('a::attr(href)').extract_first("")
            next_url =parse.urljoin('https://maoyan.com/films', next_url)
            print(next_url)
            if(next_url):
                yield Request(url=next_url, callback=self.parse_buyurl)  #http的request请求


    def parse_buyurl(self, response):
        #content = response.body
        # f = open("movie_detail.html","wb+")
        # f.write(content)
        # f.close()

        # items = MoviesItem()
        # items['url']=response.url
        node = response.css('body > div.banner > div > div.celeInfo-right.clearfix > div.action-buyBtn')
        buy_url = node.css('a::attr(href)').extract_first("")
        buy_url = parse.urljoin('https://maoyan.com/films',buy_url)
        #print("buyurl",buy_url)
        if (buy_url):
            yield Request(url=buy_url, callback=self.parse_detail)  # http的request请求




    def parse_detail(self, response):
        #content = response.body
        #f = open("maoyan_buy.html","wb+")
        #f.write(content)
        #f.close()
        items = MoviesItem()
        items['movie_name'] = response.xpath('/html/body/div[3]/div/div[2]/div[1]/h3/text()').extract()[0]
        print(items['movie_name'])
        nodes = response.xpath('//div[@class="cinema-cell"]')

        for node in nodes:
            cineme_ma = node.css('div>a::text').extract_first()
            print(cineme_ma)
            cineme_add = node.css('div p::text').extract_first()
            print(cineme_add)
            # ticket_price = node.css('div.price > span.price-num.red > span::text').extract_first()
            # print(ticket_price)
            buy_url = node.css('div.buy-btn > a::attr(href)').extract_first()
            buy_url = parse.urljoin('https://maoyan.com/films',buy_url)
            print("购票链接",buy_url)