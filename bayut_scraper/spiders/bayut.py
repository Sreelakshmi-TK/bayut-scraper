import scrapy 
from bayut_scraper.items import BayutScraperItem

class BayutSpider(scrapy.Spider):
    name = "bayut"
    start_urls = ["https://www.bayut.eg/en/egypt/properties-for-sale/"]

    def parse(self, response):
        property_cards = response.xpath("//li[@role='article']")
        print(f"found {len(property_cards)} property cards")
        
        for card in property_cards:
            link = card.xpath(".//a/@href").get()
            
            yield response.follow(
                url=link,
                callback = self.parse_property
            )

    
    def parse_property(self,response):
        item = BayutScraperItem()

        item["url"] = response.url
        
        reference_number = response.xpath('//span[@aria-label="Reference"]/text()').get()
        if reference_number:
            reference_number = reference_number.strip()
        item["reference_number"] = reference_number
        
        yield item
        