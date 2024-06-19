class PropertyRepository:
    def create_property(self, property_data):
        raise NotImplementedError

    def update_property(self, property_date, property_page_id):
        raise NotImplementedError

    def delete_property(self, property_page_id):
        raise NotImplementedError
