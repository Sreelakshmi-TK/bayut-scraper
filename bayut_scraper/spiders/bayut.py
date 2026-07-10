import scrapy 
from bayut_scraper.items import BayutScraperItem

class BayutSpider(scrapy.Spider):
    name = "bayut"
    
    start_urls = ["https://www.bayut.eg/en/egypt/properties-for-sale/"]

    @staticmethod
    def clean_text(value):
        return " ".join(value.split()) if value else None

    def parse(self, response):
        property_cards = response.xpath("//li[@role='article']")
        self.logger.info("Found %d property cards", len(property_cards))
        
        for card in property_cards:
            link = card.xpath(".//a/@href").get()
            
            if link:
                yield response.follow(
                    url=link,
                    callback=self.parse_property
                )

    
    def parse_property(self, response):
        item = BayutScraperItem()

        # URL
        item["url"] = response.url

        # Reference Number
        item["reference_number"] = self.clean_text(
            response.xpath( '//span[@aria-label="Reference"]/text()').get()
        )

        # Property ID
        property_id = None
        if "details-" in response.url:
            property_id = response.url.split("details-")[1].split(".html")[0]
        item["id"] = property_id

        # Broker Display Name
        item["broker_display_name"] = self.clean_text(
            response.xpath('//h3[@aria-label="Agency name"]/text()').get()
        )

        # Title
        item["title"] = self.clean_text(
            response.xpath('//div[@aria-label="Property overview"]//h1/text()').get()
        )

        # Property Type
        item["property_type"] = self.clean_text(
            response.xpath('//span[@aria-label="Type"]/text()').get()
        )

        # Description
        description = response.xpath( '//div[@aria-label="Property description"]//text()[not(parent::button)]').getall()

        item["description"] = self.clean_text(
            " ".join(description)
        )

        #  location   
        item["location"] = self.clean_text(
            response.xpath('//div[@aria-label="Property header"]/text()').get()
        )
        # Price
        item["price"] = self.clean_text(
            response.xpath('//span[@aria-label="Price"]/text()').get()
        )

        #Currency
        item["currency"] = self.clean_text(
            response.xpath('//span[@aria-label="Currency"]/text()').get()
        )

        # Bedrooms
        bedrooms = self.clean_text(
            response.xpath('//span[@aria-label="Beds"]/span/text()').get()
        )

        if bedrooms:
            bedrooms = bedrooms.split()[0]

        item["bedrooms"] = bedrooms

        # Bathrooms
        bathrooms = self.clean_text(
            response.xpath('//span[@aria-label="Bath"]/span/text()').get()
        )

        if bathrooms:
            bathrooms = bathrooms.split()[0]

        item["bathrooms"] = bathrooms

        # Furnished
        item["furnished"] = self.clean_text(
            response.xpath('//span[@aria-label="Furnishing"]/text()').get()
        )

        # Amenities
        amenities = [
            self.clean_text(text)
            for text in response.xpath('//div[@id="property-amenity-dialog"]//span[@class="c0327f5b"]/text()').getall()
        ]
        item["amenities"] = " | ".join(
            amenity for amenity in amenities if amenity
        )

        # Details
        item["details"] = self.clean_text(
            response.xpath('//span[@aria-label="Area"]//text()').get()
        )

        #Agent name
        item["agent_name"] = self.clean_text(
            response.xpath('//a[@aria-label="Agent name"]/h2/text()').get()
        )

        # property_image_urls
        item["property_image_urls"] = response.xpath(
            '//div[@aria-label="Gallery dialog hidden"]'
            '//div[@aria-label="Gallery dialog photo grid"]'
            '//img/@src').getall()
        
        #Completion_status
        item["completion_status"] = self.clean_text(
            response.xpath('//span[@aria-label="Completion status"]/text()').get()
        )

        #ownership
        item["ownership"] = self.clean_text(
            response.xpath('//span[@aria-label="Ownership"]/text()').get()
        )

        yield item      
        
