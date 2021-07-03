# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import scrapy
from elasticsearch_dsl import Document,Completion,Keyword,Text,Integer,Double,Date
from elasticsearch_dsl.analysis import CustomAnalyzer
from elasticsearch_dsl.connections import connections
# es = connections.create_connection(hosts=['47.94.250.123:9200'])
es = connections.create_connection(hosts=['127.0.0.1:9200'])
print(es)
ik_analyzer = CustomAnalyzer('ik_max_word',filter = ["lowercase"])
#新闻类型
class newsType(Document):
    class Meta:
        index = 'news'
        #index = 'qqmusic_news'
        doc_type = '_doc'

    class Index:
        name  = 'news'
        #name = 'qqmusic_news'
        doc_type = '_doc'
    url = Keyword()
    #music_rank = Integer()
    title = Text(analyzer = 'ik_max_word')
    author = Text(analyzer = 'ik_max_word')
    # date = Text(analyzer='ik_max_word')
    pubdate = Text(analyzer='ik_max_word')
    content = Text(analyzer = 'ik_max_word')
    suggest = Completion(analyzer = ik_analyzer)

class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # movie_name = scrapy.Field()
    # url = scrapy.Field()
    cinema_info = scrapy.Field()
    top_number = scrapy.Field()
    music_name = scrapy.Field()
    singer_name = scrapy.Field()
    music_img = scrapy.Field()
    top_number = scrapy.Field()
    music_time = scrapy.Field()
    music_url = scrapy.Field()

#     搜狐新闻
class NewsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    pubdate = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    def save_to_es(self):
        # self.fill_item()
        news = newsType()
        news.url = self['url']
        news.author = self['author']
        # news.date = self['date']
        news.pubdate = self['date'] + ':00'
        # news.pubdate = datetime.strptime(self['date'], format('%Y-%m-%d %H:%M'))
        news.title = self['title']
        news.content = self['content']
        news.suggest = self.gen_suggests(((news.title, 50),(news.content,30),(news.author,30)))
        # #print(music.suggest)
        # #music.meta.id = self['music_url']
        news.meta.id = self['url']
        news.save()
        return
    def gen_suggests(index, info_tuple):
        used_words = set()  # 去重
        suggests = []
        for text, weight in info_tuple:
            if text:
                #print("text", text)
                words = es.indices.analyze(body={'text': text, 'analyzer': 'ik_max_word'})
                #print("words", words)
                anayzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
                new_words = anayzed_words - used_words
            else:
                new_words = set()

            if new_words:
                suggests.append({'input': list(new_words), 'weight': weight})
        return suggests
