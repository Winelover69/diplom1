class Ingredient:
    def __init__(self, ingredient_type, name, price):
        self.type = ingredient_type
        self.name = name
        self.price = price

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price