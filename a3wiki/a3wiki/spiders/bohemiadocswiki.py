# -*- coding: utf-8 -*-
import scrapy
from ..items import DocumentationItem


class BohemiaDocsWiki(scrapy.Spider):
    name = 'BohemiaDocsWiki'
    start_urls = ['https://community.bistudio.com/wiki/Category:Functions',
                  'https://community.bistudio.com/wiki/Category:Scripting_Commands_Arma_3']
    base_url = "https://community.bistudio.com"

    def parse(self, response):
        link_generator = {
            'https://community.bistudio.com/wiki/Category:Functions': self.generate_bisfnc_links,
            'https://community.bistudio.com/wiki/Category:Scripting_Commands_Arma_3': self.generate_cmd_links
        }.get(response.request.url)
        for link in link_generator(response):
            yield scrapy.Request(link, callback=self.parse_documentation)

    def generate_bisfnc_links(self, response):
        for bis_function in response.css('#mw-pages a'):
            function_title = bis_function.css('::text').get()
            if function_title.startswith('BIS'):
                yield f"{self.base_url}{bis_function.css('::attr(href)').get()}"

    def generate_cmd_links(self, response):
        #  Rewrite to include first mw-category-group but filter away operators (e.g. a ^ b) and config accessors
        for script_function in response.css('.mw-category-group + .mw-category-group li a'):
            yield f"{self.base_url}{script_function.css('::attr(href)').get()}"

    def parse_documentation(self, response):
        doc_item = DocumentationItem()
        doc_item['name'] = response.css('#firstHeading').css('::text').get()
        doc_item['link'] = response.request.url
        doc_item['description'] = ''.join(response.css('dl > dt:contains(Description) + dd').css('::text').extract()).strip()
        doc_item['game_added'] = ' v'.join(response.css('div._description dl:first-of-type dd').css('::text').extract()).strip()
        yield doc_item
