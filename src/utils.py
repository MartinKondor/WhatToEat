from nltk.tokenize import word_tokenize


def preprocess_text(text: str) -> list:
    return word_tokenize(text.lower())


def is_matching_with_preference(preferences: dict,
                                recipe: list,
                                preprocessed_recipe_ingredients: list) -> bool:
    if preferences == {}:
        return True

    if "lactose_free" in preferences and preferences["lactose_free"] or\
        "vegan" in preferences and preferences["vegan"]:
        if "milk" in preprocessed_recipe_ingredients or\
            "cheese" in preprocessed_recipe_ingredients or\
            "butter" in preprocessed_recipe_ingredients or\
            "dairy" in preprocessed_recipe_ingredients or\
            "yogurt" in preprocessed_recipe_ingredients:
            return False

    if "sugar_free" in preferences and preferences["sugar_free"]:
        if "sugar" in preprocessed_recipe_ingredients or\
            "sweet" in preprocessed_recipe_ingredients:
            return False

    if "alcohol_free" in preferences and preferences["alcohol_free"]:
        if "alcohol" in preprocessed_recipe_ingredients or\
            "wine" in preprocessed_recipe_ingredients or\
            "beer" in preprocessed_recipe_ingredients:
            return False

    if "vegan" in preferences and preferences["vegan"] or\
       "vegetarian" in preferences and preferences["vegetarian"]:
       if "beef" in preprocessed_recipe_ingredients or\
            "chicken" in preprocessed_recipe_ingredients or\
            "fish" in preprocessed_recipe_ingredients or\
            "lamb" in preprocessed_recipe_ingredients or\
            "pork" in preprocessed_recipe_ingredients or\
            "mutton" in preprocessed_recipe_ingredients or\
            "turkey" in preprocessed_recipe_ingredients or\
            "venison" in preprocessed_recipe_ingredients or\
            "duck" in preprocessed_recipe_ingredients or\
            "boar" in preprocessed_recipe_ingredients or\
            "goose" in preprocessed_recipe_ingredients or\
            "rabbit" in preprocessed_recipe_ingredients or\
            "pheasant" in preprocessed_recipe_ingredients or\
            "shrimp" in preprocessed_recipe_ingredients or\
            "ham" in preprocessed_recipe_ingredients:
                return False
    
    if "vegan" in preferences and preferences["vegan"]:
        if "egg" in preprocessed_recipe_ingredients:
            return False

    return True
