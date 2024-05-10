from flask import Blueprint, jsonify, request
from infrastructure.adapters.property_repository_notion_adapter import NotionService

bp = Blueprint("notion", __name__)
notion_service = NotionService()

@bp.route("/api/properties", methods=["GET"])
def get_notion_pages():
    try:
        properties = notion_service.get_properties()
        return jsonify({"properties": properties})
    except Exception as e:
        return jsonify({"error": str(e)}), 500