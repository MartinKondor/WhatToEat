import json
import time
import random
import numpy as np
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

    def __init__(self):
        """
        attr:self.recipes - Containing all the recipes from "data/full_format_recipes.json".
        """
        self.recipes = []
        with open("data/full_format_recipes.json", "r") as recipes_file:
            self.recipes = json.load(recipes_file)

    def search_with_ingredients(self, ingredients, preferences={}, search_limit=5):
        """
        Searching for a food from self.recipes with the given list of ingredients.

        :param ingredients: list
        :param preferences: dict with the user's preferences
        :param search_limit: int how many recipes this function needs to find before stoping
        :return: dict returns the found recipes in a dict where the title is the key.
        """
        start_time = time.time()  # measure runtime
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

            # stop if it takes more than 20 seconds
            if time.time() - start_time > 20:
                return self.search_with_ingredients(ingredients[:-1], preferences)

            for recipe_ingredient in recipe_ingredients:         
                preprocessed_recipe_ingredients = np.array(preprocess_text(recipe_ingredient))

                is_user_ingredients_found = True

                for user_ingredient in preprocessed_user_ingredients:
                    if user_ingredient not in preprocessed_recipe_ingredients:
                        is_user_ingredients_found = False
                        break

                if is_user_ingredients_found and \
                   is_matching_with_preference(preferences, self.recipes[i], preprocessed_recipe_ingredients):

                    # set the title of the recipe as the key
                    found_recipes[self.recipes[i]["title"]] = self.recipes[i]

                    if len(found_recipes.keys()) >= search_limit:
                        return found_recipes

        return found_recipes


if __name__ == "__main__":
    cook = Cook()
    start_time = time.time()

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

    print("Search finished in:", time.time() - start_time)
    print()
    print("Found recipes:")
    
    for recipe in found:
        print(recipe)
