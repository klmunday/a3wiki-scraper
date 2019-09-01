# -*- coding: utf-8 -*-
import scrapy


class BisfncSpider(scrapy.Spider):
    name = 'bisfnc'
    start_urls = ['https://community.bistudio.com/wiki/Category:Functions']

    def parse(self, response):
        for bis_function in response.css('#mw-pages a'):
            function_title = bis_function.css('::text').get().replace(' ', '_')
            if function_title.startswith('BIS'):
                yield {'title': function_title}
