# Pantry Planner
![Logo](https://github.com/spongy83/my-groceries/blob/main/pantryplanner_logo1.jpg )
## Overview

This application is designed to streamline the process of managing and preparing recipes and shopping lists. It integrates SimpleNote for storing and sharing recipes, ChatGPT for parsing and processing recipe information, and OurGroceries for maintaining a shopping list. The application automates the conversion of recipes into structured formats and ensures that all necessary ingredients are included in a shopping list.

## Prerequisites

- [OpenAI API key](https://platform.openai.com/account/api-keys)
  - The preset value for the model is `gpt-3.5-turbo` to keep costs down, though better results could be had using `gpt-4-1106-preview`
- A free account with [OurGroceries](https://www.ourgroceries.com)
- A free account with [SimpleNote](https://simplenote.com)

## Key Features

1. **Integration with SimpleNote**: Utilizes SimpleNote notes for storing and sharing recipes among users.
2. **Recipe Parsing with ChatGPT**: Parses recipes from SimpleNote, either from direct descriptions or URLs, using ChatGPT.
3. **Recipe Description and Steps Generation**: ChatGPT creates a detailed description of the recipe along with cooking steps.
4. **Ingredient List Extraction**: Extracts a list of ingredients required for the recipe.
5. **Storage of Recipes in SimpleNote**: Stores the complete recipe in a separate SimpleNote note for future reference.
6. **Automatic Shopping List Update**: Adds the list of ingredients to a shopping list in OurGroceries.
7. **Weekly Note Initialization**: At the start of each new week, a new empty SimpleNote is created for adding new recipes.

## Workflow

1. **Recipe Input**:

   - Users input recipes into a shared SimpleNote note.
   - Recipes can be input either as descriptions or as URLs.

2. **Fetching and Parsing**:

   - The application fetches the note contents.
   - ChatGPT parses the note to identify and process recipes.

3. **Recipe Processing**:

   - For each recipe, ChatGPT generates a comprehensive description, including cooking steps.
   - ChatGPT extracts a list of required ingredients.

4. **Storing Processed Recipes**:

   - The complete recipe, along with the description and steps, is stored in a separate SimpleNote note.

5. **Updating Shopping List**:

   - The ingredients list is automatically added to the user's shopping list in OurGroceries.

6. **Weekly Initialization**:
   - At the beginning of each new week, the application creates a new empty SimpleNote note for adding new recipes.

## Usage Guidelines

### Running the Docker container

- Copy the `.env.example` to a new file called `.env` and update it with your credentials
- Build the Docker container `docker build -t pantryplanner .`
- Run the Docker container with `docker run -v $(pwd)/.env:/app/.env pantryplanner`

### How to automate your shopping list

- A new, empty, SimpleNote note will be created every Sunday for the next week.
- Ensure that the SimpleNote note for recipe input is shared with all relevant users.
- Now add your dishes by description, as generic or specific as you want. Or, add whole recipe URLs to the list. One dish/recipe per line
- The shopping list will be generated in OurGroceries on the Friday following
- Recipe descriptions will be added to your SimpleNote vault

## Support and Feedback

For any support queries or feedback, please create an issue here on GitHub.

---

Documentation Version: 1.0
Last Updated: 2023-12-08
