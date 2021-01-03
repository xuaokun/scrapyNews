# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import MoviesItem

class ExampleSpider(scrapy.Spider):
    name = 'mtime_movies'
    allowed_domains = ['mtime.com'] #过滤不在范围内的域名
    start_urls = ['http://theater.mtime.com/China_Beijing/']
    def parse(self, response):
        nodes = response.xpath('//div[@class="firstmovie fl"]//div[@class="moviebtn"]')
        print(nodes)
        for node in nodes:
            first_url = node.css('a::attr(href)').extract_first("")
            if(first_url):
                yield Request(url=parse.urljoin('http://theater.mtime.com/China_Beijing/', first_url), callback=self.parse_detail)  #http的request请求
        nodes = response.xpath('//div[@class="othermovie fr"]//dd[@class="btns"]')
        for node in nodes:
            next_url = node.css('a::attr(href)').extract_first("")
            if(next_url):
                yield Request(url=parse.urljoin('http://theater.mtime.com/China_Beijing/', next_url), callback=self.parse_detail)
        nodes = response.xpath('//div[@class="othermovie"]//dd[@class="btns"]')
        for node in nodes:
            next_url = node.css('a::attr(href)').extract_first("")
            if(next_url):
                yield Request(url=parse.urljoin('http://theater.mtime.com/China_Beijing/', next_url), callback=self.parse_detail)


    def parse_detail(self, response):
        content = response.body
        #f = open("movie_detail.html","wb+")
        #f.write(content)
        items = MoviesItem()
        items['url']=response.url
        node = response.css('body > div.newshowtime > div.nstimemid > div.nbg_cinema > div.nstimecon.clearfix > div.main > div.videoname')
        items['movie_name'] = node.css('h2::attr(title)').extract_first("")
        print("电影名", items['movie_name'])
        print("购票链接:", items['url'])
        scripts = response.xpath('//script/text()').extract()
        for script in scripts:
            if 'cinemasJson =' in str(script):
                #print('found cinemasJson,in script', scripts.index(script), ':', script)  # log
                script = str(script).split('cinemasJson = ')[1]  # 获取'cinemasJson ='之后的内容
                script = script.split('];')[0]  # 获取'var showtimesJson'之前的内容
                infos = script[1:-1]  # 去掉头尾，因为头尾是中括号
                infos = re.split('[:,]', infos)  # 以:和,做分割符分割
                #print(infos) # 打印确认获取到想要的内容（一个list）
                items['cinema_info'] = []
                for info_index,info in enumerate(infos):
                        if(info == '"cname"'):
                            #print("found cinema_name index in infos",infos.index(info)+1)
                            cname_index = info_index + 1
                            cname = infos[cname_index]
                            cname = cname[1:-1]
                            print("-----------------")
                            print("影院名",cname )
                        if(info == '"address"'):
                            #print("found cinema_address index in infos",infos.index(info)+1)
                            address_index = info_index + 1
                            address = infos[address_index]
                            address = address[1:-1]
                            print("影院地址", address)
                        if (info == '"isticket"'):
                            #print("found isticket index in infos", infos.index(info) + 1)
                            isticket_index = info_index + 1
                            isticket = infos[isticket_index]
                            #print("是否在映:",isticket)
                            if(isticket == False):
                                #items['cinema_info'].append([cname,address,isticket])
                                continue
                        if (info == '"lowestprice"'):
                            #print("found lowestprice index in infos", infos.index(info) + 1)
                            lowestprice_index = info_index + 1
                            lowestprice = infos[lowestprice_index]
                            lowestprice = re.split('[""]', lowestprice)[1]
                            print("该影院价格", lowestprice)
                            items['cinema_info'].append([cname, address,lowestprice])
                print(items)
                f = open('movie_info.txt', 'a')  # append的方式打开文件
                f.write(str(items))
                f.write('\n')
                f.close()
                # print("电影名", items['movie_name'])
                # print("影院名：", items['cinema_name'])
                # print("影院地址", items['cinema_add'])
                # print("该影院价格", items['ticket_price'])
                # print("购票链接:", items['url'])


    #学姐提取信息方法
    # def parse_detail(self, response):
    #     scripts = response.xpath('//script/text()').extract()
    #     for script in scripts:
    #         if 'cinemasJson =' in str(script):
    #             #print('found cinemasJson,in script', scripts.index(script), ':', script)  # log
    #             script = str(script).split('cinemasJson =')[1]  # 获取'cinemasJson ='之后的内容
    #             script = script.split('var showtimesJson')[0]  # 获取'var showtimesJson'之前的内容
    #             #print(script)  # 打印确认获取到想要的内容（一个list）
    #
    #             # TODO: 获取数据list
    #             right = 0  # 记录还没找到对应的}的{有几个
    #             start = 0  # 数据起始下标
    #             data = []
    #             for i in range(len(script)):  # 遍历每个字符
    #                 if script[i] == '{':
    #                     if right == 0:
    #                         start = i + 1  # 新的数据起始下标是第一个{的下一个字符
    #                     right += 1  # {入栈
    #                 elif script[i] == '}':
    #                     right -= 1  # {出栈
    #                     if right == 0:  # 当前数据结束
    #                         #print(script[start:i])  # log:打印这条数据确认提取成功
    #                         data.append(script[start:i])  # 提取到一条数据，即一个影院的信息
    #
    #             for data_i in data:  # 遍历每条数据，即一个影院的信息
    #             #     # TODO: 分割每条数据为数据项list。根据逗号确定每个数据项，只有当{}、[]都完成匹配后的那个逗号才是真正的分割符
    #                 big_right = 0  # {
    #                 middle_right = 0  # [
    #                 start = 0
    #                 items_string = []
    #                 for i,char_i in enumerate(data_i):  # 遍历这条数据的每个字符
    #                     if char_i == ',' and big_right == 0 and middle_right == 0:  # 当前item结束，注意影院信息循环结束最后一项信息被丢弃了
    #                         while data_i[start] == '[' or data_i[start] == '{':
    #                             start += 1
    #                         #print(data_i[start:i])  # log打印确认该数据的一个item
    #                         items_string.append(data_i[start:i])  # 添加
    #                         start = i + 1
    #                     elif char_i == '{':
    #                         big_right += 1
    #                     elif char_i == '}':
    #                         big_right -= 1
    #                     elif char_i == '[':
    #                         middle_right += 1
    #                     elif char_i == ']':
    #                         middle_right -= 1
    #                     elif (i == len(data_i) - 1):
    #                         #print(data_i[start:i])
    #                         items_string.append(data_i[start:i])
    #
    #                 # TODO: 根据数据项string提取想要的信息
    #                 items = {}
    #                 for string_i in items_string:
    #                     if '"cname":' in string_i:
    #                         items.update({'cname': string_i.split(':')[1]})
    #                     elif '"lowestprice":' in string_i:
    #                         items.update({'lowestprice': string_i.split(':')[1]})
    #                 print(items)