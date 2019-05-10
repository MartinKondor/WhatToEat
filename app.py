import os
from flask import Flask, render_template, request
from src.cook import Cook


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
        
        if not ingredient:
            break
            
        ingredients.append(ingredient)
             
    return render_template("cook.html", **{
        "recipes": COOK.search_with_ingredients(ingredients)
    })


if __name__ == "__main__":
    APP.run(debug=DEBUG, host=HOST, port=PORT)
