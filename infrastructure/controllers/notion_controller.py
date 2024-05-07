from flask import Blueprint, jsonify, request
from application.services.notion_service import NotionService

notion_bp = Blueprint("notion", __name__)
notion_service = NotionService()

@notion_bp.route("/api/notion-pages", methods=["GET"])
def get_notion_pages():
    try:
        num_pages = int(request.args.get("num_pages")) 
        pages = notion_service.get_pages(num_pages)
        return jsonify({"pages": pages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500