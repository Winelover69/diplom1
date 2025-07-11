from src.ingredient import Ingredient
from src.database import Database

class Burger:
    def __init__(self):
        self.buns = []
        self.ingredients = []

    def set_buns(self, bun):
        self.buns = [bun, bun]

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, ingredient_index):
        self.ingredients.pop(ingredient_index)

    def move_ingredient(self, from_index, to_index):
        ingredient = self.ingredients.pop(from_index)
        self.ingredients.insert(to_index, ingredient)

    def get_price(self):
        total_price = 0
        if self.buns:
            total_price += self.buns[0].get_price() * 2 # Цена за две булки
        for ingredient in self.ingredients:
            total_price += ingredient.get_price()
        return total_price

    def get_receipt(self):
        receipt = "(булка " + self.buns[0].get_name() + ")\n"
        for ingredient in self.ingredients:
            receipt += "(котлета " if ingredient.get_type() == "filling" else "(соус "
            receipt += ingredient.get_name() + ")\n"
        receipt += "(булка " + self.buns[0].get_name() + ")"
        return receipt