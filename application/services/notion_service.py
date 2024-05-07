import requests
import os

class NotionService:
    def __init__(self):
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.database_id = os.getenv("DATABASE_ID")
        self.base_url = "https://api.notion.com/v1"

    def get_pages(self, num_pages=None):
        url = f"{self.base_url}/databases/{self.database_id}/query"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            results.extend(data["results"])

        return results