import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from items import NewsItem
import chardet
class ExampleSpider(scrapy.Spider):
    name = 'cctv'
    allowed_domains = ['cctv.com'] #过滤不在范围内的域名
    start_urls = ['https://www.cctv.com/']
    def parse(self, response):
        nodes = response.xpath('//div[@class="col_w780"]//a/@href')
        for node in nodes:
            url = node.extract()
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        # f = open("xinhuanet.txt", "a+")
        item = NewsItem()
        url = response.url
        # print(url)
        print('新闻详情页：{0}'.format(url))
        node = response.xpath('//div[@class="content_18313"]') # class必须精确匹配，不能只含有多个类名中的一个
        # print(node)
        if node and node[0]:
            try:
                title = node.css('#title_area > h1::text').extract_first().strip()
                source_time = node.css('.info1::text').extract_first().strip()
                source = re.split(r'\|', source_time)[0].strip()
                date = re.split(r'\|', source_time)[1].strip()
                date = re.sub(r'[年|月]', '-', date)
                date = re.sub(r'日', '', date)
                contentList = response.css('#content_area strong::text,#content_area p::text').extract()
                content = ''
                for par in contentList:
                    if not par.strip():
                        continue
                    content += par.strip() + '\n'
            except Exception as e:
                print("新闻详情采集出错了：{0}".format(e))
                return
            item['url'] = url
            item['title'] = title
            item['date'] = date
            item['author'] = source
            item['content'] = content
            yield item
if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(["scrapy","crawl","cctv"])
