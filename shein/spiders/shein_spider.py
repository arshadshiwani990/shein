import scrapy
import re
import random

class SheinSpiderSpider(scrapy.Spider):
    name = "shein_spider"
    allowed_domains = ["shein.com"]
    start_urls = ["https://shein.com"]


    seen_urls=[]


    def start_requests(self):
    
        url='https://us.shein.com/sitemap-index.xml'
        yield scrapy.Request(url=url, callback=self.parse_sitemap)

    def parse_sitemap(self,response):

        product_sitemaps=re.findall('loc>(.+-products-\d+.[^<]+)<',response.text)
        for product_sitemap in product_sitemaps:
            
            if len(self.seen_urls)<=200000:
                print(product_sitemap)
                yield scrapy.Request(url=product_sitemap, callback=self.parse_product_links)
            else:
                break
       
    def parse_product_links(self,respose):

        products=re.findall('>(.+-p-\d+.html)<',respose.text)
        for productUrl in products:

            # print(productUrl)
            if productUrl not in self.seen_urls:

                self.seen_urls.append(productUrl)
                yield {"productUrl":productUrl}
                