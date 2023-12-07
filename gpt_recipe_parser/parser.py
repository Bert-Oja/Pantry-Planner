import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from openai import OpenAI

class RecipeParser:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    @staticmethod
    def is_url(input_string):
        try:
            result = urlparse(input_string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def fetch_recipe_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            recipe_text = ' '.join([para.get_text() for para in paragraphs])
            return recipe_text
        except requests.RequestException as e:
            print(f"Error fetching the recipe: {e}")
            return None

    def _get_system_prompt(self, file_name):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            prompt_file_path = os.path.join(dir_path, file_name)
            with open(prompt_file_path, 'r') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading the prompt file: {e}")
            return None

    def _call_gpt(self, text, file_name):
        system_prompt = self._get_system_prompt(file_name)
        if system_prompt is None:
            return None

        completion = self.client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            temperature=0.1,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )

        output_string = completion.choices[0].message.content
        return json.loads(output_string)

    def extract_ingredients_with_gpt(self, recipe_text):
        return self._call_gpt(recipe_text, 'extract_prompt.txt')

    def create_ingredient_list_with_gpt(self, dish):
        return self._call_gpt(dish, 'create_prompt.txt')

    def get_ingredients(self, input_string):
        if self.is_url(input_string):
            recipe_text = self.fetch_recipe_from_url(input_string)
            if recipe_text:
                return self.extract_ingredients_with_gpt(recipe_text)
        else:
            return self.create_ingredient_list_with_gpt(input_string)

