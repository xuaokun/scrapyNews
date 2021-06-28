import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import NewsItem
import chardet
class ExampleSpider(scrapy.Spider):
    name = 'news_qq'
    allowed_domains = ['qq.com'] #过滤不在范围内的域名
    start_urls = ['https://new.qq.com/']
    def parse(self, response):
        content = response.body
        print(content)
        # f = open("news_qq.html","wb+")
        # f.write(content)
        # f.close()
        nodes = response.xpath('//a/@href')
        itemsCnt = 0
        for node in nodes:
            url = node.extract()
            if url and ('new.qq.com/omn' in str(url)) and ('new.qq.com/omn/author' not in str(url)):
                itemsCnt += 1
                print('本次爬取第{}条数据'.format(++itemsCnt))
                print(url)
                # if(itemsCnt > 1):
                #     break
                yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        # f = open("sohu.txt", "a+")
        item = NewsItem()
        url = response.url
        # print(url)
        # print('新闻详情页：')
        node = response.xpath('//div[@class="LEFT"]')
        if node and node[0]:
            title = node.css('h1::text').extract_first().strip()
            # print(title)
            # print('-----')
            year = node.css('.year span::text').extract_first()
            # print(year)
            dateList = node.css('#LeftTool .md::text').extract()
            date = ''
            for oneStr in dateList:
                date += str(oneStr)
            # print(date)
            timeList = node.css('#LeftTool .time::text').extract()
            time = ''
            for oneStr in timeList:
                time += str(oneStr)
            # print(time)
            # print('-----')
            date = year + '-' + date[0:2] + '-' + date[3:] + ' ' + time
            # print(date)
            author = node.css('.author > div::text').extract_first()
            # print(author)
            # print('-----')
            contentList = node.css('.content-article strong::text,p::text').extract()
            content = ''
            for par in contentList:
                if '原标题：' in str(par):
                    continue
                if '责任编辑：' in str(par):
                    continue
                content += par.strip() + '\n'
            # print(content)
            item['url'] = url
            item['title'] = title
            item['date'] = date
            item['author'] = author
            item['content'] = content
            print(item)
            # return
            yield item
            # f.write(url + '\n')
            # f.write(title + ' ' + date + ' ' + author + '\n')
            # f.write(content)
        # f.close()
        if __name__ == '__main__':
            from scrapy import cmdline
            cmdline.execute(["scrapy","crawl","news_qq"])
