# -*- coding: utf-8 -*-
import scrapy

from MyFirstScrapy.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        # 利用CSS选择器来解析页面
        quotes = response.css(".quote")
        # print("---------------------\n", quotes)
        for quote in quotes:
            quote_item = QuoteItem()
            quote_item['text'] = quote.css(".text::text").extract_first()
            quote_item['author'] = quote.css(".author::text").extract_first()
            quote_item['tags'] = quote.css(".tags .tag::text").extract()

            yield quote_item

        next_url = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next_url)
        yield scrapy.Request(url=url, callback=self.parse)
