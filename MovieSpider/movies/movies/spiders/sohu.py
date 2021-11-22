import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import NewsItem

class ExampleSpider(scrapy.Spider):
    name = 'sohu_home'
    allowed_domains = ['sohu.com'] #过滤不在范围内的域名
    start_urls = ['http://news.sohu.com/']
    def parse(self, response):
        nodes = response.xpath('//a/@href')
        itemsCnt = 0
        for node in nodes:
            url = node.extract()
            if url and ('sohu.com' in str(url)):
                itemsCnt += 1
                print('本次爬取第{}条数据'.format(++itemsCnt))
                yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        # f = open("sohu.txt", "a+")
        item = NewsItem()
        url = response.url
        node = response.xpath('//div[@data-spm="content"]')
        if node and node[0]:
            title = node.css('.text-title > h1::text').extract_first().strip() \
                    or node.css('span.title-info-title::text').extract_first().strip()
            date = node.css('.time::text').extract_first()
            author = node.css('span[data-role="original-link"] > a::text,span[data-role="original-link"]::text')\
                .extract_first()
            if '来源' in author or author.strip() == '':
                author = '搜狐网'
            contentList = node.css('article strong::text,article p::text').extract()
            content = ''
            for par in contentList:
                if '原标题：' in str(par):
                    continue
                if '责任编辑：' in str(par):
                    continue
                if not par.strip():
                    continue
                content += par.strip() + '\n'
            # contentHot = node.css('#mpbox > div.c-comment-content > div > div:nth-child(2) > div').extract()
            item['url'] = url
            item['title'] = title
            item['date'] = date + ':00'
            item['author'] = author
            item['content'] = content
            yield item
        #     f.write(url + '\n')
        #     f.write(title + ' ' + date + ' ' + author + '\n')
        #     f.write(content)
        # f.close()