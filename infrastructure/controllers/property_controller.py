from flask import Blueprint, jsonify, request

from application.property_use_cases import CreateProperty
from infrastructure.adapters.property_repository_notion_adapter import \
    NotionService

bp = Blueprint("property", __name__, url_prefix="/property")
notion_service = NotionService()


@bp.route("/", methods=["GET"])
def get_notion_pages():
    try:
        properties = notion_service.get_properties()
        return jsonify({"properties": properties})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/create-property", methods=["POST"])
def create_property_publication():
    property_data = request.get_json()
    create_property_case = CreateProperty(notion_service)
    created_property = create_property_case.execute(property_data)

    return jsonify(created_property.__dict__), 201
