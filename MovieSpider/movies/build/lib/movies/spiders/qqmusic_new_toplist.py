import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'qqmusic_toplist'
    allowed_domains = ['qq.com'] #过滤不在范围内的域名
    start_urls = ['https://y.qq.com/n/yqq/toplist/27.html#stat=y_new.toplist.menu.27']
    def parse(self, response):
        # content = response.body
        # f = open("qqmusic_toplist.html","wb+")
        # f.write(content)
        # f.close()
        nodes = response.xpath('///html/body/div[2]/div[2]/div[3]/ul[2]/li')
        items = []
        for node in nodes:
            item = MoviesItem()
            print('------------------')
            top_number = node.css('div > div.songlist__number.songlist__number--top::text').extract_first()
            if(top_number):
                pass
            else:
                top_number = node.css('div > div.songlist__number::text').extract_first()
            item['top_number'] = top_number
            print(top_number)
            music_name = node.css('div > div.songlist__songname > span > a.js_song::attr(title)').extract_first()
            item['music_name'] = music_name
            print(music_name)
            singer_name = node.css(' div > div.songlist__artist::attr(title)').extract_first()
            item['singer_name'] = singer_name
            print(singer_name)
            music_img = node.css(' div > div.songlist__songname > span > a.songlist__cover.album_name > img::attr(data-original)').extract_first()
            item['music_img'] = ['https:' + music_img.split('?')[0]]
            print(item['music_img'])
            music_url = node.css('div > div.songlist__songname > span > a.js_song::attr(href)').extract_first()
            item['music_url'] = music_url
            print(music_url)
            music_time = node.css('div > div.songlist__time::text').extract_first()
            item['music_time'] = music_time
            print(music_time)
            items.append(item)
        print(items)