import os
import ourgroceries
import asyncio
import random


class OurGroceriesClient:
    def __init__(self):
        self.username = os.getenv("OURGROCERIES_USERNAME")
        self.password = os.getenv("OURGROCERIES_PASSWORD")
        self.client = ourgroceries.OurGroceries(
            username=self.username, password=self.password
        )
        asyncio.run(self.client.login())

    def find_or_create_list(self, list_name):
        """
        Finds a shopping list by name or creates it if it doesn't exist.
        """
        try:
            lists = asyncio.run(self.client.get_my_lists()).get("shoppingLists")
            for lst in lists:
                if lst["name"].lower() == list_name.lower():
                    return lst["id"]

            # Create new list if not found
            new_list = asyncio.run(self.client.create_list(list_name))
            return new_list["listId"]
        except Exception as e:
            print(f"Error in finding or creating list: {e}")
            return None

        # def add_recipe(self, recipe_name):
        """
        Adds a recipe to the list
        """
        try:
            asyncio.run(self.client.create_list(name=recipe_name, list_type="RECIPES"))
            return
        except Exception as e:
            print(f"Error when adding recipe: {e}")
            return None

    def add_or_update_item(self, list_id, item_name, quantity, unit, item_category):
        try:
            items = (
                asyncio.run(self.client.get_list_items(list_id))
                .get("list")
                .get("items")
            )
            for item in items:
                if item["value"].lower() == item_name.lower():
                    current_quantity_unit = item["note"]
                    old_quantity_str, old_unit = current_quantity_unit.split(maxsplit=1)

                    # Convert the old quantity to a number
                    try:
                        old_quantity = float(old_quantity_str)
                    except ValueError:
                        # Handle the case where the quantity is not a valid number
                        print(
                            f"Error parsing quantity: {old_quantity_str} is not a number."
                        )
                        return

                    # Update quantity if units match
                    if old_unit == unit:
                        new_quantity = old_quantity + quantity
                        new_quantity_unit = f"{new_quantity} {unit}"
                        asyncio.run(
                            self.client.remove_item_from_list(
                                list_id, item_id=item["id"]
                            )
                        )
                        asyncio.run(
                            self.client.add_item_to_list(
                                list_id,
                                value=item_name,
                                category=item_category,
                                auto_category=False,
                                note=new_quantity_unit,
                            )
                        )
                    return

            # Add new item if not exists
            quantity_unit = f"{quantity} {unit}"
            asyncio.run(
                self.client.add_item_to_list(
                    list_id,
                    value=item_name,
                    category=item_category,
                    auto_category=False,
                    note=quantity_unit,
                )
            )
        except Exception as e:
            print(f"Error in adding or updating item: {e}")


def standardize_ingredient_name(name):
    standardization_map = {
        "onions": "onion",
        "egg": "eggs",
        "black pepper": "pepper",
        # Add more mappings as needed
    }
    return standardization_map.get(name.lower(), name)


def aggregate_ingredients(recipes):
    aggregated_ingredients = {}

    for recipe in recipes:
        for ingredient, details in recipe["ingredients"].items():
            # Standardize the ingredient names
            standardized_ingredient = standardize_ingredient_name(ingredient)

            if standardized_ingredient in aggregated_ingredients:
                # Override the ingredient details with the new one
                # This disregards the unit and updates quantity regardless
                if isinstance(details["quantity"], str):
                    continue
                aggregated_ingredients[standardized_ingredient]["quantity"] += details[
                    "quantity"
                ]
            else:
                aggregated_ingredients[standardized_ingredient] = details

    return aggregated_ingredients


def add_recipes_to_grocery_list(aggregated_ingredients, list_name=None):
    og_client = OurGroceriesClient()

    if list_name is None:
        list_name = f"Grocery List {random.randint(1,10)}"  # Default list name, change if necessary
    list_id = og_client.find_or_create_list(list_name)

    for ingredient, details in aggregated_ingredients.items():
        og_client.add_or_update_item(
            list_id,
            ingredient,
            details["quantity"],
            details["unit"],
            details["category"],
        )
