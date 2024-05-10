import requests
import os

PROPERTY_INFORMATION = ["Description", "Pictures", "Price", "Title"]

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
            property = {}
            property_notion_info = result["properties"]
            property["title"] = property_notion_info["Title"]
            property["description"] = property_notion_info["Description"]
            property["price"] = property_notion_info["Price"]
            property["pictures"] = property_notion_info["Pictures"]
            
            property_list.append(property)

        return property_list

    def create_page(self, data: dict):
        url = f"{self.base_url}/pages"
        payload = {"parent": {"database_id": {self.database_id}}, "properties": data}
        response = requests.post(url, headers=self.headers, json=payload)
        
        return response
