"""
Main file responsible for routing and server logic.
"""
import os
from flask import Flask, render_template, request
from src.cook import Cook
from src.utils import check_and_process_user_input


APP = Flask(__name__)
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("IS_HEROKU", False) or False
COOK = Cook()


@APP.route("/")
def home():
    """
    Main route
    """
    return render_template("home.html")


@APP.route("/cook", methods=["POST"])
def cook_route():
    """
    Route for searching and rendering recipes
    """
    ingredients = []

    # max 100 ingredient
    for i in range(1, 100):
        ingredient = check_and_process_user_input(request.form.get("ingredient-" + str(i)))
        if not ingredient:
            break
        ingredients.append(ingredient)

    # remove duplicates
    ingredients = list(set(ingredients))

    # set preferences
    user_preferences = {
        "gluten-free": request.form.get("gluten-free") == "on",
        "sugar-free": request.form.get("sugar-free") == "on",
        "lactose-free": request.form.get("lactose-free") == "on",
        "alcohol-free": request.form.get("alcohol-free") == "on",
        "vegetarian": request.form.get("vegetarian") == "on",
        "vegan": request.form.get("vegan") == "on",
        "kosher": request.form.get("kosher") == "on",
    }

    try:
        search_limit = int(request.form.get("search-limit"))
    except TypeError:
        search_limit = 7

    if DEBUG:
        print()
        print("ingredients:", ingredients)
        print("user_preferences:", user_preferences)
        print()

    # Searching
    found_recipes = COOK.search_with_ingredients(ingredients, user_preferences, search_limit)
    return render_template("cook.html", recipes=found_recipes)


if __name__ == "__main__":
    APP.run(debug=DEBUG, host=HOST, port=PORT, use_reloader=True)
