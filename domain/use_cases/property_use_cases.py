from domain import Property
from domain import PropertyRepository


class CreateProperty:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def execute(self, property_data):
        new_property = Property(**property_data)
        self.repository.create_property(new_property)

        return new_property


class UpdateProperty:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def execute(self, property_data, property_page_id):
        updated_property = self.repository.update_property(
            property_data, property_page_id
        )

        return updated_property


class DeleteProperty:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def execute(self, property_page_id):
        deleted_property = self.repository.delete_property(property_page_id)

        return deleted_property
