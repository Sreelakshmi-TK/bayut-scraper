import sqlite3
import json
from scrapy.exceptions import DropItem


class DeduplicationPipeline:
    def open_spider(self, spider):
        self.seen_ids = set()

    def process_item(self, item, spider):
        property_id = item["id"]

        if property_id in self.seen_ids:
            raise DropItem(f"Duplicate property found: {property_id}")

        self.seen_ids.add(property_id)
        return item

class BayutScraperPipeline:
    def process_item(self, item, spider):
        return item


class SQLitePipeline:
    def open_spider(self, spider):
        spider.logger.info("Opening SQLite database")

        self.connection = sqlite3.connect("bayut.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            create table if not exists properties (
                id text primary key,
                url text,
                reference_number text,
                broker_display_name text,
                title text,
                property_type text,
                description text,
                location text,
                price text,
                currency text,
                bedrooms text,
                bathrooms text,
                furnished text,
                amenities text,
                details text,
                agent_name text,
                property_image_urls text,
                completion_status text,
                ownership text
            )
        """)

        self.connection.commit()
        spider.logger.info("SQLite database ready.")


    def process_item(self, item, spider):
        spider.logger.info("Processing property %s", item["id"])
        spider.logger.info("%s", dict(item))

        self.cursor.execute("""
            insert or replace into properties (
                id,
                url,
                reference_number,
                broker_display_name,
                title,
                property_type,
                description,
                location,
                price,
                currency,
                bedrooms,
                bathrooms,
                furnished,
                amenities,
                details,
                agent_name,
                property_image_urls,
                completion_status,
                ownership
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"],
            item["url"],
            item["reference_number"],
            item["broker_display_name"],
            item["title"],
            item["property_type"],
            item["description"],
            item["location"],
            item["price"],
            item["currency"],
            item["bedrooms"],
            item["bathrooms"],
            item["furnished"],
            item["amenities"],
            item["details"],
            item["agent_name"],
            json.dumps(item["property_image_urls"]),
            item["completion_status"],
            item["ownership"]
        ))

        self.connection.commit()
        spider.logger.info("Inserted property %s into SQLite.", item["id"])
        return item

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("SQLite connection closed.")