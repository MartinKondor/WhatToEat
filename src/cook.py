import json
import random
import numpy as np
from time import time
try:
    from src.utils import (
        preprocess_text,
        is_matching_with_preference
    )
except ImportError:
    from utils import (
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

        with open("data/full_format_recipes.json", "r") as recipes_file:
            self.recipes = json.load(recipes_file)

    def search_with_ingredients(self,
                                ingredients: list,
                                preferences: dict={},
                                search_limit: int=5) -> dict:
        """
        Searching for a food from self.recipes with the given list of ingredients.
        :return: Returns the found recipes in a dict where the title is the key.
        """
        start_time = time()
        preprocessed_user_ingredients = []
        found_recipes = {}
        
        # random choice in this case
        if ingredients == []:
            for i in range(search_limit):
                random_choice = random.choice(self.recipes)
                preprocessed_ingredients = np.array(preprocess_text(ri) for ri in random_choice["ingredients"])

                while not is_matching_with_preference(preferences, random_choice, preprocessed_ingredients):
                    random_choice = random.choice(self.recipes)
                    preprocessed_ingredients = np.array(preprocess_text(ri) for ri in random_choice["ingredients"])

                found_recipes[random_choice["title"]] = random_choice
            return found_recipes

        for ingredient in ingredients:
            prep = preprocess_text(ingredient)
            if type(prep) is list:
                prep = ' '.join(prep)
            preprocessed_user_ingredients.append(prep)

        preprocessed_user_ingredients = np.array(preprocessed_user_ingredients)

        for i in range(len(self.recipes)):
            try:
                recipe_ingredients = self.recipes[i]["ingredients"]
            except KeyError:
                continue

            if time() - start_time > 4:
                return self.search_with_ingredients(ingredients[:-1], preferences)

            for recipe_ingredient in recipe_ingredients:         
                preprocessed_recipe_ingredients = np.array(preprocess_text(recipe_ingredient))

                is_user_ingredients_found = True

                for user_ingredient in preprocessed_user_ingredients:
                    if user_ingredient not in preprocessed_recipe_ingredients:
                        is_user_ingredients_found = False
                        break

                if is_user_ingredients_found and\
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
