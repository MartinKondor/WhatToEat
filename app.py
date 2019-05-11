import os
from flask import Flask, render_template, request
from src.cook import Cook
from src.utils import check_user_input


APP = Flask(__name__)
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", 5000))
DEBUG = False if os.environ.get("IS_HEROKU", False) else True
COOK = Cook()


@APP.route("/")
def home():
    return render_template("home.html")
    
    
@APP.route("/cook", methods=["POST"])
def cookRoute():
    ingredients = []
     
    for i in range(1, 100):
        ingredient = request.form.get("ingredient-" + str(i))
        
        if not check_user_input(ingredient):
            break
            
        ingredients.append(ingredient)
             
    user_preferences = {
        "vegan": request.form.get("vegan") == "on",
        "vegetarian": request.form.get("vegetarian") == "on",
        "sugar-free": request.form.get("sugar-free") == "on",
        "lactose-free": request.form.get("lactose-free") == "on",
        "alcohol-free": request.form.get("alcohol-free") == "on"
    }
    return render_template("cook.html", **{
        "recipes": COOK.search_with_ingredients(ingredients, user_preferences)
    })


if __name__ == "__main__":
    if not os.environ.get("IS_HEROKU", False):
        APP.run(debug=DEBUG, host=HOST, port=PORT, use_reloader=True)
