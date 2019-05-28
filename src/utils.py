"""
Utilities for cook.py.
"""
from nltk.tokenize import word_tokenize


def preprocess_text(text):
    """
    :param text: str
    :return: list
    """
    return word_tokenize(text.strip().lower())


def is_lactose_free(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return not ("milk" in ingredients or
                "cheese" in ingredients or
                "butter" in ingredients or
                "dairy" in ingredients or
                "yogurt" in ingredients or
                "buttermilk" in ingredients or
                "milk/cream" in ingredients or
                "milk / cream" in ingredients or
                "parmesan" in ingredients or
                "goat cheese" in ingredients)


def is_sugar_free(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return not ("sugar" in ingredients or
                "sweet" in ingredients) or \
               "no sugar added" in ingredients or \
               "sugar conscious" in ingredients


def is_alcohol_free(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return not ("alcohol" in ingredients or
                "wine" in ingredients or
                "red wine" in ingredients or
                "beer" in ingredients)


def is_meat_free(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return not ("beef" in ingredients or
                "chicken" in ingredients or
                "fish" in ingredients or
                "lamb" in ingredients or
                "pork" in ingredients or
                "mutton" in ingredients or
                "turkey" in ingredients or
                "venison" in ingredients or
                "duck" in ingredients or
                "boar" in ingredients or
                "goose" in ingredients or
                "rabbit" in ingredients or
                "pheasant" in ingredients or
                "shrimp" in ingredients or
                "ham" in ingredients or
                "crab" in ingredients or
                "veal" in ingredients or
                "sausage" in ingredients or
                "shellfish" in ingredients or
                "lobster" in ingredients or
                "bacon" in ingredients)


def is_vegan(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return is_meat_free(ingredients) and is_lactose_free(ingredients) and \
           not ("egg" in ingredients or "eggplant" in ingredients)


def is_kosher(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return "kosher" in ingredients


def is_gluten_free(ingredients):
    """
    :param ingredients: list
    :return: bool
    """
    return "wheat/gluten-free" in ingredients or "gluten-free" in ingredients


def is_matching_with_preference(preferences, recipe, preprocessed_recipe_ingredients):
    """
    :param preferences: dict with user preferences
    :param recipe: list the recipe we try to match with
    :param preprocessed_recipe_ingredients: recpie ingredients preprocessed
    :return: bool
    """
    if preferences == {}:
        return True

    preprocessed_recipe_categories = []
    _preprocessed_recipe_categories = [preprocess_text(category) for category in recipe["categories"]]
    
    for _pc in _preprocessed_recipe_categories:
        if isinstance(_pc, list):
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

    if "kosher" in preferences and preferences["kosher"]:
        if not is_kosher(preprocessed_recipe_categories):
            return False

    if "gluten-free" in preferences and preferences["gluten-free"]:
        if not is_gluten_free(preprocessed_recipe_categories):
            return False

    return True


def check_and_process_user_input(user_input):
    """
    :param user_input: str
    :return: False if str is not accepted else returns the processed user_input
    """
    if not isinstance(user_input, str):
        return False

    _input = user_input.lower().strip()

    if _input and len(_input) > 2:
        return _input

    return False
