import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from items import NewsItem
import chardet
class ExampleSpider(scrapy.Spider):
    name = 'xinhuanet'
    allowed_domains = ['xinhuanet.com'] #过滤不在范围内的域名
    start_urls = ['http://www.xinhuanet.com/']
    def parse(self, response):
        content = response.body
        # print(content)
        # f = open("news_qq.html","wb+")
        # f.write(content)
        # f.close()
        nodes = response.xpath('//div[@id="mCSB_2"]//a/@href')
        # print(nodes)
        itemsCnt = 0
        for node in nodes:
            url = node.extract()
            print(url)
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        # f = open("xinhuanet.txt", "a+")
        item = NewsItem()
        url = response.url
        # print(url)
        print('新闻详情页：{0}'.format(url))
        node = response.xpath('//div[@class="header-cont clearfix"]') # class必须精确匹配，不能只含有多个类名中的一个
        # print(node)
        if node and node[0]:
            title = node.css('.title::text').extract_first().strip()
            # print(title)
            # print('-----')
            year = node.css('.year em::text').extract_first().strip()
            # print(year)
            date = node.css('.day::text').extract_first().strip()
            # print(date)
            time = node.css('.time::text').extract_first().strip()
            # print(time)
            # print('-----')
            date = year + '-' + date[0:2] + '-' + date[3:] + ' ' + time
            # print(date)
            author = node.css('.source::text').extract_first().strip().replace('来源：', '')
            # print(author)
            # print('-----')
            contentList = response.css('#detail p::text').extract()
            content = ''
            for par in contentList:
                content += par.strip() + '\n'
            # print(content)
            item['url'] = url
            item['title'] = title
            item['date'] = date
            item['author'] = author
            item['content'] = content
            # print(item)
            # f.write(url + '\n')
            # f.write(title + ' ' + date + ' ' + author + '\n')
            # f.write(content)
            # f.close()
            yield item
if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(["scrapy","crawl","xinhuanet"])
