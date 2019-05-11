from nltk.tokenize import word_tokenize


def preprocess_text(text: str) -> list:
    return word_tokenize(text.lower())


def is_lactose_free(ingredients):
    return not ("milk" in ingredients or\
            "cheese" in ingredients or\
            "butter" in ingredients or\
            "dairy" in ingredients or\
            "yogurt" in ingredients)


def is_sugar_free(ingredients):
    return not ("sugar" in ingredients or\
            "sweet" in ingredients)


def is_alcohol_free(ingredients):
    return not ("alcohol" in ingredients or\
            "wine" in ingredients or\
            "red wine" in ingredients or\
            "beer" in ingredients)


def is_meat_free(ingredients):
    return not ("beef" in ingredients or\
            "chicken" in ingredients or\
            "fish" in ingredients or\
            "lamb" in ingredients or\
            "pork" in ingredients or\
            "mutton" in ingredients or\
            "turkey" in ingredients or\
            "venison" in ingredients or\
            "duck" in ingredients or\
            "boar" in ingredients or\
            "goose" in ingredients or\
            "rabbit" in ingredients or\
            "pheasant" in ingredients or\
            "shrimp" in ingredients or\
            "ham" in ingredients or\
            "crab" in ingredients or\
            "veal" in ingredients)


def is_vegan(ingredients):
    return is_meat_free(ingredients) and is_lactose_free(ingredients) and\
        not ("egg" in ingredients)


def is_matching_with_preference(preferences: dict,
                                recipe: list,
                                preprocessed_recipe_ingredients: list) -> bool:
    if preferences == {}:
        return True

    preprocessed_recipe_categories = []
    _preprocessed_recipe_categories = [preprocess_text(category) for category in recipe["categories"]]
    
    for _pc in _preprocessed_recipe_categories:
        if type(_pc) is list:
            for _pci in _pc:
                preprocessed_recipe_categories.append(_pci)
        else:
            preprocessed_recipe_categories.append(_pc)

    if "lactose_free" in preferences and preferences["lactose_free"]:
        if not (is_lactose_free(preprocessed_recipe_ingredients) and is_lactose_free(preprocessed_recipe_categories)):
            return False

    if "sugar_free" in preferences and preferences["sugar_free"]:
        if not (is_sugar_free(preprocessed_recipe_ingredients) and is_sugar_free(preprocessed_recipe_categories)):
            return False

    if "alcohol_free" in preferences and preferences["alcohol_free"]:
        if not (is_alcohol_free(preprocessed_recipe_ingredients) and is_alcohol_free(preprocessed_recipe_categories)):
            return False

    if "vegetarian" in preferences and preferences["vegetarian"]:
       if not (is_meat_free(preprocessed_recipe_ingredients) and is_meat_free(preprocessed_recipe_categories)):
                return False
    
    if "vegan" in preferences and preferences["vegan"]:
        if not (is_vegan(preprocessed_recipe_ingredients) and is_vegan(preprocessed_recipe_categories)):
            return False

    return True


def check_user_input(user_input: str) -> bool:
    return True if user_input and len(user_input) > 2 else False
