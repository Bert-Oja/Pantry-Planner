import os
import ourgroceries
import asyncio


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

    def add_recipe(self, recipe_name):
        """
        Adds a recipe to the list
        """
        try:
            asyncio.run(self.client.create_list(name=recipe_name, list_type="RECIPES"))
            return
        except Exception as e:
            print(f"Error when adding recipe: {e}")
            return None

    def add_or_update_item(self, list_id, item_name, quantity, unit):
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
                                category=None,
                                auto_category=True,
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
                    category=None,
                    auto_category=True,
                    note=quantity_unit,
                )
            )
        except Exception as e:
            print(f"Error in adding or updating item: {e}")


def add_recipe_to_grocery_list(recipe_json, list_name=None):
    og_client = OurGroceriesClient()
    if list_name is None:
        list_name = recipe_json["recipe"]
    list_id = og_client.find_or_create_list(list_name)

    for ingredient, details in recipe_json["ingredients"].items():
        og_client.add_or_update_item(
            list_id, ingredient, details["quantity"], details["unit"]
        )
    og_client.add_recipe(recipe_name=recipe_json["recipe"])
