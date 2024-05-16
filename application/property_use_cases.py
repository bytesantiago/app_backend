from domain.models.property import Property
from domain.ports.property_repository import PropertyRepository


class CreateProperty:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def execute(self, property_data):
        new_property = Property(**property_data)
        self.repository.create_property(new_property)

        return new_property
