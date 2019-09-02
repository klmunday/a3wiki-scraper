# -*- coding: utf-8 -*-
import scrapy
from ..items import BISFunctionItem


class BisFunctionWiki(scrapy.Spider):
    name = 'bisfunctionwiki'
    start_urls = ['https://community.bistudio.com/wiki/Category:Functions']
    base_url = "https://community.bistudio.com"

    def parse(self, response):
        for bis_function in response.css('#mw-pages a'):
            function_title = bis_function.css('::text').get()
            if function_title.startswith('BIS'):
                function_link = f"{self.base_url}{bis_function.css('::attr(href)').get()}"
                yield scrapy.Request(function_link, callback=self.parse_function)

    def parse_function(self, response):
        bis_function = BISFunctionItem()
        bis_function['name'] = response.css('#firstHeading').css('::text').get()
        bis_function['description'] = ''.join(response.css('dl:nth-child(6) dd').css('::text').extract()).strip()
        bis_function['game_added'] = ' v'.join(response.css('div._description.fnc dl:first-of-type dd').css('::text').extract()).strip()
        yield bis_function
