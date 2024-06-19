from adapters import PropertiesRepository
from domain import CreateProperty, DeleteProperty, UpdateProperty
from flask import Blueprint, jsonify, request

property_controller_blueprint = Blueprint("property", __name__, url_prefix="/property")


@property_controller_blueprint.route("/", methods=["GET"])
def get_properties():
    try:
        properties_repository = PropertiesRepository()
        properties = properties_repository.get_properties()
        return jsonify({"properties": properties})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@property_controller_blueprint.route("/create-property", methods=["POST"])
def create_property_publication():
    property_data = request.get_json()
    properties_repository = PropertiesRepository()
    create_property_case = CreateProperty(properties_repository)
    created_property = create_property_case.execute(property_data)

    return jsonify(created_property.__dict__), 201


@property_controller_blueprint.route("/update-property", methods=["PATCH"])
def update_property_publication():
    property_data = request.get_json()
    properties_repository = PropertiesRepository()
    update_property_case = UpdateProperty(properties_repository)
    updated_property = update_property_case.execute(property_data)

    return jsonify(updated_property.__dict__), 204


@property_controller_blueprint.route("/delete_property", methods=["PATCH"])
def delete_property_publication():
    property_page_id = request.get_json()
    properties_repository = PropertiesRepository()
    delete_property_case = DeleteProperty(properties_repository)
    deleted_property = delete_property_case.execute(property_page_id)

    return jsonify(deleted_property.__dict__), 204
