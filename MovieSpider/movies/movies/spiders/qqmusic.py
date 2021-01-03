import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'qq_music'
    allowed_domains = ['qq.com'] #过滤不在范围内的域名
    start_urls = ['https://y.qq.com/']
    def parse(self, response):
        # content = response.body
        # f = open("qqmusic_index_after.html","wb+")
        # f.write(content)
        # f.close()
        nodes = response.xpath('//div[@class="songlist__item_box"]')
        item = MoviesItem()
        for node in nodes:
            print('------------------')
            music_name = node.css('div.songlist__cont > h3 > a::attr(title)').extract_first()
            item['music_name'] = music_name
            print(music_name)
            singer_name = node.css(' div.songlist__item_box > div.songlist__cont > p > a::attr(title)').extract_first()
            item['singer_name'] = singer_name
            print(singer_name)
            music_img = node.css(' a > img::attr(src)').extract_first()
            item['music_img'] = ['http:' + music_img]
            music_url =  node.css('div.songlist__cont > h3 > a::attr(href)').extract_first()
            print(music_url)
            music_time = node.css('div.songlist__time.c_tx_thin::text').extract_first()
            item['music_time'] = music_time
            print(music_time)
            #yield item
