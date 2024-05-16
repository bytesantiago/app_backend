class Property:
    def __init__(self, title, description, price, pictures, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.pictures = pictures
