import requests

def format_amount(value):
    if not value:
        return ""
    try:
        rounded = round(float(value), 1)
        return str(int(rounded)) if rounded == int(rounded) else str(rounded)
    except:
        return str(value)


# =============================================================================
# ABSTRACTION + ENCAPSULATION
# Ingredient is an abstract-style base class that defines the shared interface
# for all ingredient types. It encapsulates common data (name, amount, unit)
# and declares get_display_style() as a method subclasses must override.
# =============================================================================
class Ingredient:
    """Base class representing a generic ingredient."""

    def __init__(self, name, amount="", unit=""):
        # Encapsulation: data and behaviour bundled together
        self._name = name
        self._amount = amount
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    @property
    def unit(self):
        return self._unit

    @property
    def missing(self):
        """Subclasses define whether this ingredient is missing."""
        raise NotImplementedError("Subclasses must implement missing")

    def get_display_style(self):
        """
        Abstraction: defines an interface that all subclasses must implement.
        Returns the CSS class string used to style this ingredient in the UI.
        """
        raise NotImplementedError("Subclasses must implement get_display_style()")

    def __str__(self):
        parts = [p for p in [self._amount, self._unit, self._name] if p]
        return " ".join(parts)


# =============================================================================
# INHERITANCE + POLYMORPHISM
# OwnedIngredient and MissingIngredient both inherit from Ingredient and
# polymorphically override missing and get_display_style() differently.
# =============================================================================
class OwnedIngredient(Ingredient):
    """An ingredient the user already has. Inherits from Ingredient."""

    @property
    def missing(self):
        return False  # Polymorphism: overrides base behaviour

    def get_display_style(self):
        return "have"  # Polymorphism: returns different style to MissingIngredient


class MissingIngredient(Ingredient):
    """An ingredient the user is missing. Inherits from Ingredient."""

    @property
    def missing(self):
        return True  # Polymorphism: overrides base behaviour differently

    def get_display_style(self):
        return "missing"  # Polymorphism: returns different style to OwnedIngredient


# =============================================================================
# ENCAPSULATION
# Recipe bundles all recipe data and behaviour into one cohesive object.
# =============================================================================
class Recipe:
    def __init__(self, name, ingredients, instructions, missed_count, used_count,
                 diet_labels, meal_types, image_url=""):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.missed_count = missed_count
        self.used_count = used_count
        self.diet_labels = diet_labels
        self.meal_types = meal_types
        self.image_url = image_url

    @staticmethod
    def from_spoonacular(data, instructions, diet_labels, meal_types):
        name = data.get("title", "Unknown")
        used_count = data.get("usedIngredientCount", 0)
        missed_count = data.get("missedIngredientCount", 0)

        ingredients = []

        # Use OwnedIngredient subclass for ingredients the user has
        for ing in data.get("usedIngredients", []):
            metric = ing.get("measures", {}).get("metric", {})
            ingredients.append(OwnedIngredient(
                ing.get("name", ""),
                format_amount(metric.get("amount", ing.get("amount", ""))),
                metric.get("unitShort", ing.get("unit", ""))
            ))

        # Use MissingIngredient subclass for ingredients the user lacks
        for ing in data.get("missedIngredients", []):
            metric = ing.get("measures", {}).get("metric", {})
            ingredients.append(MissingIngredient(
                ing.get("name", ""),
                format_amount(metric.get("amount", ing.get("amount", ""))),
                metric.get("unitShort", ing.get("unit", ""))
            ))

        return Recipe(name, ingredients, instructions, missed_count, used_count,
                      diet_labels, meal_types, image_url=data.get("image", ""))


# =============================================================================
# SINGLETON PATTERN
# RecipeFinder uses the Singleton pattern to ensure only one instance is ever
# created. This makes sense because there is only one API key and no reason
# to create multiple finders — every extra instance would be wasteful.
#
# FACADE PATTERN
# RecipeFinder also acts as a Facade: it hides the complexity of multiple
# Spoonacular API calls (findByIngredients + informationBulk), filtering,
# and data mapping behind a single clean method: search_by_ingredients().
# =============================================================================
class RecipeFinder:
    BASE_URL = "https://api.spoonacular.com"
    _instance = None  # Singleton: holds the single shared instance

    def __new__(cls, api_key=None):
        """Singleton pattern: only create a new instance if one doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.api_key = api_key
        return cls._instance

    def __init__(self, api_key=None):
        # __init__ is called every time, but __new__ ensures it's the same object.
        # We only set api_key if it hasn't been set yet.
        if api_key and not hasattr(self, 'api_key'):
            self.api_key = api_key

    def search_by_ingredients(self, ingredients, diet="", meal_type="", number=10):
        """
        Facade: single entry point that coordinates multiple API calls,
        filtering logic, and object construction behind a clean interface.
        """
        ingredients_str = ",".join(ingredients)

        url = f"{self.BASE_URL}/recipes/findByIngredients"
        params = {
            "apiKey": self.api_key,
            "ingredients": ingredients_str,
            "number": number,
            "ranking": 2,
            "ignorePantry": True
        }

        response = requests.get(url, params=params)
        data = response.json()

        if not data or not isinstance(data, list):
            print("Unexpected API response:", data)
            return []

        ids = ",".join(str(r["id"]) for r in data)
        details_map = self.get_bulk_details(ids)

        results = []
        for item in data:
            recipe_id = str(item["id"])
            details = details_map.get(recipe_id, {})

            diet_labels = []
            if details.get("vegan"):
                diet_labels.append("Vegan")
            elif details.get("vegetarian"):
                diet_labels.append("Vegetarian")
            if details.get("glutenFree"):
                diet_labels.append("Gluten free")

            meal_types = details.get("dishTypes", [])

            if diet:
                if diet == "vegan" and not details.get("vegan"):
                    continue
                if diet == "vegetarian" and not details.get("vegetarian"):
                    continue
                if diet == "glutenFree" and not details.get("glutenFree"):
                    continue

            if meal_type and meal_type not in meal_types:
                continue

            analyzed = details.get("analyzedInstructions", [])
            if analyzed and analyzed[0].get("steps"):
                steps = analyzed[0]["steps"]
                instructions = "\n".join(
                    f"Step {s['number']}: {s['step']}" for s in steps
                )
            else:
                instructions = details.get("instructions") or "No instructions available."

            recipe = Recipe.from_spoonacular(item, instructions, diet_labels, meal_types)
            results.append(recipe)

        return results

    def get_bulk_details(self, ids):
        url = f"{self.BASE_URL}/recipes/informationBulk"
        params = {
            "apiKey": self.api_key,
            "ids": ids,
            "includeNutrition": False
        }
        response = requests.get(url, params=params)
        data = response.json()

        details_map = {}
        for recipe in data:
            details_map[str(recipe["id"])] = recipe
        return details_map
