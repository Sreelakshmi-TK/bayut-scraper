import scrapy 

class BayutSpider(scrapy.Spider):
    name = "bayut"
    start_urls = ["https://www.bayut.eg/en/egypt/properties-for-sale/"]

    def parse(self, response):
        print(response.css("title::text").get())