import os
from unittest.mock import Mock, patch

import pytest

from domain.models.property import Property
from infrastructure.adapters.property_repository_notion_adapter import \
    NotionService


class TestNotionService:
    @patch("requests.post")
    def test_get_properties_all_pages(self, mock_post):
        # Setup
        service = NotionService()
        mock_response_page1 = Mock()
        mock_response_page2 = Mock()
        mock_response_page1.json.return_value = {
            "results": [
                {
                    "id": "1",
                    "properties": {
                        "Title": {"title": [{"plain_text": "Title1"}]},
                        "Description": {"rich_text": [{"plain_text": "Description1"}]},
                        "Price": {"rich_text": [{"plain_text": "100"}]},
                        "Pictures": {"files": [{"file": {"url": "url1"}}]},
                    },
                }
            ],
            "has_more": True,
            "next_cursor": "cursor1",
        }
        mock_response_page2.json.return_value = {
            "results": [
                {
                    "id": "2",
                    "properties": {
                        "Title": {"title": [{"plain_text": "Title2"}]},
                        "Description": {"rich_text": [{"plain_text": "Description2"}]},
                        "Price": {"rich_text": [{"plain_text": "200"}]},
                        "Pictures": {"files": [{"file": {"url": "url2"}}]},
                    },
                }
            ],
            "has_more": False,
        }
        mock_post.side_effect = [mock_response_page1, mock_response_page2]

        # Test
        result = service.get_properties()

        # Verify
        assert len(result) == 2
        assert result[0]["title"] == "Title1"
        assert result[1]["title"] == "Title2"
        assert mock_post.call_count == 2

    @patch("requests.post")
    def test_get_properties_limited_pages(self, mock_post):
        # Setup
        service = NotionService()
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "1",
                    "properties": {
                        "Title": {"title": [{"plain_text": "Title1"}]},
                        "Description": {"rich_text": [{"plain_text": "Description1"}]},
                        "Price": {"rich_text": [{"plain_text": "100"}]},
                        "Pictures": {"files": [{"file": {"url": "url1"}}]},
                    },
                }
            ],
            "has_more": False,
        }
        mock_post.return_value = mock_response

        # Test
        result = service.get_properties(num_pages=1)

        # Verify
        assert len(result) == 1
        assert result[0]["title"] == "Title1"
        mock_post.assert_called_once_with(
            f"{service.base_url}/databases/{service.database_id}/query",
            json={"page_size": 1},
            headers=service.headers,
        )

    @patch("requests.post")
    def test_create_property_success(self, mock_post):
        # Setup
        service = NotionService()
        property_data = Property(
            "Test Title", "Test Description", "300", ["pic1", "pic2"]
        )
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Test
        response = service.create_property(property_data)

        # Verify
        assert response.status_code == 200
        mock_post.assert_called_once_with(
            f"{service.base_url}/pages",
            headers=service.headers,
            json={
                "parent": {"database_id": service.database_id},
                "properties": {
                    "Title": {"title": [{"text": {"content": "Test Title"}}]},
                    "Description": {
                        "rich_text": [{"text": {"content": "Test Description"}}]
                    },
                    "Price": {"rich_text": [{"text": {"content": "300"}}]},
                },
            },
        )
