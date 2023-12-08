import os
import json
import sys
from datetime import date
from dotenv import load_dotenv
from gpt_recipe_parser import RecipeParser
from ourgroceries_integration import add_recipes_to_grocery_list, aggregate_ingredients
from simplenote_integration import SimpleNoteClient
import argparse

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug", action="store_true", help="Store the GPT output in a debug file"
)
parser.add_argument(
    "-c", "--create", action="store_true", help="Create a note for the current week"
)
args = parser.parse_args()

load_dotenv()

week_number = date.today().isocalendar()[1]

# Bunch of code to deal with creating and retrieving the recipe lists
sn_client = SimpleNoteClient()
notes, status = sn_client.get_note_list(tags=[f"recipes_{week_number}"])

# Check if the create flag is used
if args.create:
    if len(notes) == 0:
        note, status = sn_client.create_note(
            f"Recipes for week {week_number}", tags=[f"recipes_{week_number}"]
        )
        note_key = note["key"]
    sys.exit()
else:
    note_key = notes[0]["key"]

# Get all the recipes for this week
note, status = sn_client.get_note(note_key)
note_content = note["content"]
content_list = note_content.split("\n")
content_list = content_list[1:]
# Stop if the list is empty
if len(content_list) == 0:
    sys.exit()

# store the GPT output when the argument --debug has been used
dir_path = os.path.dirname(os.path.realpath(__file__))
dump_file = os.path.join(dir_path, "dump_file.json")

if args.debug and os.path.exists(dump_file):
    with open(dump_file, "r") as file:
        recipe_list = json.load(file)
else:
    parser = RecipeParser()
    recipe_list = parser.parse_multiple_recipes(content_list)
    if args.debug:
        try:
            with open(dump_file, "w") as file:
                json.dump(recipe_list, file, indent=4)
        except IOError as e:
            print(f"Error writing to file: {e}")
            sys.exit()

# Now, for each recipe we will create a new note with a valid tag
# And we will add all ingredients to the shopping list
# For that, we can be smarter and update the quantities already before adding them to the list

list = f"Shopping List Week {week_number}"
# Assuming recipe_list contains multiple recipes
aggregated_ingredients = aggregate_ingredients(recipe_list)
add_recipes_to_grocery_list(aggregated_ingredients, list_name=list)

for item in recipe_list:
    recipe = item.get("recipe", "No Recipe Name")
    instructions = item.get("instructions", "No Instructions")
    ingredients_dict = item.get("ingredients", {})
    # Constructing the ingredients list in the desired format
    ingredients_list = ["Ingredients:"]
    for ingredient, details in ingredients_dict.items():
        quantity = details.get("quantity", "No Quantity")
        unit = details.get("unit", "unit")
        ingredients_list.append(f"- {ingredient} ({quantity} {unit})")
    # Joining the ingredients list into a single string
    ingredients_str = "\n".join(ingredients_list)

    sn_client.create_note(
        f"{recipe}\n{instructions}\n\n{ingredients_str}", tags=["recipes"]
    )
