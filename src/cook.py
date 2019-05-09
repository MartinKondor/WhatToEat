import json
import numpy as np
from pandas import read_csv
from src.utils import (
    preprocess_text,
    is_matching_with_preference
)


class Cook(object):
    """
    attr:self.recipes - Containing all the recipes from "data/full_format_recipes.json".
    
    attr:self.infos - One i-th element of it is containing all meta information about "self.recipes[i]".
    
    attr:self.infos_columns -
        Column names of "self.infos".
        Index(['title', 'rating', 'calories', 'protein', 'fat', 'sodium', '#cakeweek',
            '#wasteless', '22-minute meals', '3-ingredient recipes',
            ...
            'yellow squash', 'yogurt', 'yonkers', 'yuca', 'zucchini', 'cookbooks',
            'leftovers', 'snack', 'snack week', 'turkey'],
            dtype='object', length=680)
    """
    def __init__(self):
        self.recipes = []
        self.infos = []
        self.infos_columns = []

        with open("data/full_format_recipes.json", "r") as recipes_file:
            self.recipes = json.load(recipes_file)

        _ = read_csv("data/epi_r.csv")
        self.infos = _.values
        self.infos_columns = _.columns


    def search_with_ingredients(self,
                                ingredients: list,
                                preferences: dict={},
                                search_limit: int=5) -> dict:
        """
        Searching for a food from self.recipes with the given list of ingredients.
        :return: Returns the found recipes in a dict where the title is the key.
        """
        preprocessed_ingredients = np.array([preprocess_text(ingredient) for ingredient in ingredients])
        found_recipes = {}

        for i in range(len(self.recipes)):
            try:
                recipe_ingredients = self.recipes[i]["ingredients"]
            except KeyError:
                continue

            for recipe_ingredient in recipe_ingredients:         
                preprocessed_recipe_ingredients = np.array(preprocess_text(recipe_ingredient))

                if np.any(preprocessed_ingredients == preprocessed_recipe_ingredients) and\
                    is_matching_with_preference(preferences, self.recipes[i], preprocessed_recipe_ingredients):

                    # set the title of the recipe as the key
                    found_recipes[self.recipes[i]["title"]] = self.recipes[i]

                    if len(found_recipes.keys()) >= search_limit:
                        return found_recipes

        return found_recipes


if __name__ == "__main__":
    from time import time

    cook = Cook()
    start_time = time()

    ingredients_you_want = [
        "potato",
        "parsnip",
        "broccoli"
    ]
    preferences = {
        "sugar_free": True,
        "alcohol_free": True,
        "vegetarian": True,
    }

    found = cook.search_with_ingredients(ingredients_you_want, preferences, search_limit=3)

    print("Search finished in:", time() - start_time)
    print()
    print("Found recipes:")
    
    for recipe in found:
        print(recipe)
