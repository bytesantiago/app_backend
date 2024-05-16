import os

import requests

from domain.models.property import Property


class NotionService:
    def __init__(self):
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.database_id = os.getenv("DATABASE_ID")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def get_properties(self, num_pages=None):
        url = f"{self.base_url}/databases/{self.database_id}/query"
        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.headers)

        data = response.json()
        results = data["results"]

        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            response = requests.post(url, json=payload, headers=self.headers)
            data = response.json()
            results.extend(data["results"])

        property_list = []
        for result in results:
            property_notion_info = result["properties"]
            property = Property(
                id=result["id"],
                title=self.parse_title_content(property_notion_info["Title"]),
                description=self.parse_description_content(
                    property_notion_info["Description"]
                ),
                price=self.parse_price_content(property_notion_info["Price"]),
                pictures=self.parse_pictures_content(property_notion_info["Pictures"]),
            )
            property_list.append(property.__dict__)

        return property_list

    def parse_title_content(self, title_content: dict):
        title = None
        for item in title_content["title"]:
            title = item["plain_text"]

        return title

    def parse_description_content(self, description_content: dict):
        description = None
        for item in description_content["rich_text"]:
            description = item["plain_text"]

        return description

    def parse_price_content(self, price_content: dict):
        price = None
        for item in price_content["rich_text"]:
            price = item["plain_text"]

        return price

    def parse_pictures_content(self, pictures_content: dict):
        files = []
        for item in pictures_content["files"]:
            files.append(item["file"]["url"])

        return files

    def create_property(self, property_data: Property):
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": self.parse_create_property_payload(property_data),
        }
        response = requests.post(url, headers=self.headers, json=payload)

        return response

    def parse_create_property_payload(self, property_data: Property):
        return {
            "Title": {"title": [{"text": {"content": property_data.title}}]},
            "Description": {
                "rich_text": [{"text": {"content": property_data.description}}]
            },
            "Price": {"rich_text": [{"text": {"content": property_data.price}}]},
        }
