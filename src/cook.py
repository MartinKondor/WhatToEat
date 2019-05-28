"""
Responsible for searching and filtering recipes.
"""
import json
import time
import random
import numpy as np
try:
    from src.utils import preprocess_text, is_matching_with_preference
except ImportError:
    # in case of runing from the main direcory
    from utils import preprocess_text, is_matching_with_preference


class Cook:
    """
    :attr: self.recipes - Containing all the recipes from "data/full_format_recipes.json".
    """

    def __init__(self):
        self.recipes = []
        with open("data/full_format_recipes.json", "r") as recipes_file:
            self.recipes = json.load(recipes_file)

    def random_choice(self, preferences, n_of_recipes):
        """
        Choose N random recipes according to the given preferences.

        :param preferences: dict with the user's preferences
        :param n_of_recipes: int of random recipes
        :return: list of random recipes
        """
        found_recipes = {}

        for _ in range(n_of_recipes):

            while True:  # choosing random recipes until one is matching with preference
                random_choice = random.choice(self.recipes)

                try:
                    preprocessed_ingredients = np.array([
                        preprocess_text(_) for _ in random_choice["ingredients"]
                    ])
                except KeyError:
                    continue

                if is_matching_with_preference(preferences, random_choice, preprocessed_ingredients):
                    found_recipes[random_choice["title"]] = random_choice
                    break

        return found_recipes

    def search_with_ingredients(self, ingredients, preferences=None, search_limit=7):
        """
        Searching for a food from self.recipes with the given list of ingredients.

        ## Performance
        Data: ingredients = ['broccoli'], preferences = {'alcohol-free': true}, search_limit = 7
        v1.0 search speed: 1.293074131011963
        v0.9 search speed: 1.677095890045166

        :param ingredients: list user input preprocessed
        :param preferences: dict with the user's preferences
        :param search_limit: int how many recipes this function needs to find before stoping
        :return: dict returns the found recipes in a dict where the title is the key.
        """
        if not preferences:
            preferences = {}

        if not ingredients:  # random choice in this case
            return self.random_choice(preferences, search_limit)

        found_recipes = {}
        start_time = time.time()  # measure runtime

        for recipe in self.recipes:
            try:
                if not recipe["ingredients"]:
                    continue
            except KeyError:
                continue

            # remove one ingredient if it takes more than X seconds
            if time.time() - start_time > 20:
                return self.search_with_ingredients(ingredients[:-1], preferences, search_limit)

            # flattening matrix to one dimension
            recipe_ingredients = np.concatenate([preprocess_text(_) for _ in recipe["ingredients"]])
            is_user_ingredients_found = True

            for user_ingredient in ingredients:
                if user_ingredient not in recipe_ingredients:
                    is_user_ingredients_found = False
                    break

            if is_user_ingredients_found and is_matching_with_preference(preferences, recipe, recipe_ingredients):
                found_recipes[recipe["title"]] = recipe

            if len(found_recipes.keys()) >= search_limit:
                break

        return found_recipes


if __name__ == "__main__":
    test_cook = Cook()
    search_start_time = time.time()

    test_ingredients_you_want = [
        "potato",
        "parsnip",
        "broccoli"
    ]
    test_preferences = {
        "sugar_free": True,
        "alcohol_free": True,
        "vegetarian": True,
    }

    test_found = test_cook.search_with_ingredients(test_ingredients_you_want, test_preferences, 3)

    print("Search finished in:", time.time() - search_start_time)
    print()
    print("Found recipes:")

    for test_recipe in test_found:
        print(test_recipe)
