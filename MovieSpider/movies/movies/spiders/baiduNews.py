import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import NewsItem

class ExampleSpider(scrapy.Spider):
    name = 'baidu_home'
    allowed_domains = ['baidu.com'] #过滤不在范围内的域名
    start_urls = ['https://news.baidu.com/']
    def parse(self, response):
        # content = response.body
        # f = open("qqmusic_toplist.html","wb+")
        # f.write(content)
        # f.close()
        nodes = response.xpath('//a/@href')
        itemsCnt = 0
        for node in nodes:
            url = node.extract()
            if url and ('baijiahao.baidu.com' in str(url)):
                itemsCnt += 1
                print('本次爬取第{}条数据'.format(++itemsCnt))
                print(url)
                # if(itemsCnt > 9):
                #     break
                yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        f = open("baidu.txt", "a+")
        item = NewsItem()
        url = response.url
        # print(url)
        # print('新闻详情页：')
        node = response.xpath('//div[@id="detail-page"]')
        if node and node[0]:
            title = node.css('.article-title > h2::text').extract_first().strip()
            print(title)
            # print('-----')
            date = node.css('.date::text').extract_first()
            print(date)
            # print('-----')
            author = node.css('.author-name > a::text').extract_first()
            print(author)
            # print('-----')
            # contentList = node.css('.article-content p span.bjh-p::text').extract()
            contentList = node.css('.article-content p span.bjh-p')
            content = ''
            for par in contentList:
                if par.css('.bjh-strong').extract():
                    for subStrong in par.css('.bjh-strong::text').extract():
                        content += subStrong
                    content += '\n'
                else:
                    content += par.css('::text').extract_first().strip() + '\n'
            print(content)
            print('-------------------')
            item['url'] = url
            item['title'] = title
            item['date'] = date
            item['author'] = author
            item['content'] = content
            # yield item
            f.write(url + '\n')
            f.write(title + ' ' + date + ' ' + author + '\n')
            f.write(content)
        f.close()