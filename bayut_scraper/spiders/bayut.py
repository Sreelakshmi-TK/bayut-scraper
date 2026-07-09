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
        
        property_id = response.url.split("details-")[1].split(".html")[0]
        item["id"] = property_id

        broker_display_name = response.xpath('//h3[@aria-label="Agency name"]/text()').get()
        if broker_display_name:
            broker_display_name = broker_display_name.strip()
        item["broker_display_name"] = broker_display_name

        title = response.xpath('//div[@aria-label="Property overview"]//h1/text()').get()
        if title:
            title = title.strip()
        item["title"] = title

        property_type = response.xpath('//span[@aria-label="Type"]/text()').get()
        if property_type:
            property_type = property_type.strip()
        item["property_type"] = property_type

        description = response.xpath('//div[@aria-label="Property description"]//span/text()').get()
        if description:
            description = description.strip()
        item["description"] = description

        yield item        
        
