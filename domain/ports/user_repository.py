class UserRepository:
    def create_user(self, user_data):
        raise NotImplementedError

    def update_user(self, user_id, user_data):
        raise NotImplementedError

    def find_user(self, search_criteria):
        raise NotImplementedError

    def delete_user(self, user_id):
        raise NotImplementedError
