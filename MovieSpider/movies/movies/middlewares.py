# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
notActiveUrl = ['cctv.com', 'sohu.com']

class SeleniumMiddleware(object):
    # 动态页面
    def process_request(self, request, spider):
        # if 'sohu.com' in request.url:
        #     return None
        for url in notActiveUrl:
            if url in request.url:
                return None
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # 指定谷歌浏览器路径
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path='D:/chromedriver')
        self.driver.get(request.url)
        #需要向下滑动的页面
        for x in range(1, 12, 2):
            i = float(x) / 11
            # scrollTop 从上往下的滑动距离
            js = 'document.body.scrollTop=document.body.scrollHeight * %f' % i
            self.driver.execute_script(js)
            time.sleep(0.1)
        #加载评论信息
        # if 'sohu.com' in request.url:
        #     try:
        #         while(True):
        #             self.driver.find_element_by_class_name('c-comment-more').click()
        #             print('{0}点击更多'.format(request.url))
        #             time.sleep(1)
        #     except Exception as e:
        #         print('{0}:{1}'.format(request.url, e))

        if 'http://www.xinhuanet.com/' == request.url:
            try:
                for i in range(3):
                    self.driver.find_element_by_class_name('xpage-more-btn').click()
            except Exception as e:
                print('{0}:{1}'.format(request.url, e))

        html = self.driver.page_source
        self.driver.quit()
        return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8',
                                        request=request)
class MoviesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MoviesDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
