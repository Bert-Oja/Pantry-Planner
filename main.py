import os
import json
from dotenv import load_dotenv
from gpt_recipe_parser import RecipeParser
from ourgroceries_integration import add_recipe_to_grocery_list

load_dotenv()

parser = RecipeParser(os.getenv("OPENAI_API_KEY"))
recipes = [
    "Swedish Meatballs with Lingonberry Sauce",
    "root vegetable stew",
    "smoked salmon pasta",
    "home made pea soup with frozen peas",
    "korv stroganoff",
]

list = "Bert Shopping List"
for recipe in recipes:
    ingredient_list = parser.get_ingredients(recipe)
    add_recipe_to_grocery_list(ingredient_list, list_name=list)
