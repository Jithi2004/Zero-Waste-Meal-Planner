import requests
import spacy
from fuzzywuzzy import process
import datetime

# Load NLP model
nlp = spacy.load("en_core_web_sm")

API_KEY = "04fa1ab34bca4783863f4309782bfdbb"

COMMON_INGREDIENTS = [
    "tomato", "cheese", "onion", "garlic", "milk", "egg", "flour",
    "butter", "carrot", "pepper", "potato", "spinach", "rice",
    "chicken", "beef", "bread", "salt", "sugar", "oil", "vinegar"
]

# Dictionary to track saved waste per user per day
user_waste_tracker = {}

def preprocess_ingredients(raw_ingredients):
    cleaned = []
    doc = nlp(raw_ingredients.lower())
    for token in doc:
        if not token.is_stop and token.is_alpha:
            cleaned.append(token.lemma_)
    return cleaned

def fuzzy_match(ingredient, choices, threshold=80):
    match, score = process.extractOne(ingredient, choices)
    return match if score >= threshold else ingredient

def get_recipes_from_ingredients(ingredients):
    joined_ingredients = ",".join(ingredients)
    url = f"https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": joined_ingredients,
        "number": 5,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def display_recipes(recipes):
    print("\n🍽️ Suggested Recipes:")
    for i, recipe in enumerate(recipes):
        print(f"{i+1}. {recipe['title']} (ID: {recipe['id']})")
        print(f"   Used: {recipe['usedIngredientCount']} | Missing: {recipe['missedIngredientCount']}")
        print(f"   ➤ Image: {recipe['image']}\n")

def display_recipe_details(recipe):
    print(f"\n👩‍🍳 Recipe: {recipe['title']}")
    print(f"Ready in {recipe['readyInMinutes']} minutes | Servings: {recipe['servings']}")
    print(f"\n🛒 Ingredients:")
    for ing in recipe['extendedIngredients']:
        print(f" - {ing['original']}")
    print(f"\n📋 Instructions:\n{recipe.get('instructions', 'Instructions not available.')}")
    print(f"\n🔗 Source: {recipe.get('sourceUrl')}")

def estimate_saved_waste(ingredients):
    return len(ingredients) * 100  # 100g per item as a simple estimate

def track_waste(user_id, ingredients):
    today = datetime.date.today().isoformat()
    grams_saved = estimate_saved_waste(ingredients)

    if user_id not in user_waste_tracker:
        user_waste_tracker[user_id] = {}
    user_waste_tracker[user_id][today] = user_waste_tracker[user_id].get(today, 0) + grams_saved

    print(f"✅ Tracked {grams_saved}g of waste saved for user '{user_id}' on {today}.")
    print(f"🔁 Total today: {user_waste_tracker[user_id][today]}g")

def main():
    print("🧠 Zero Waste Meal Planner (CLI Edition)")
    user_input = input("Enter the ingredients you have (comma-separated): ")
    user_id = input("Enter your user ID: ").strip() or "default_user"

    raw_ingredients = user_input.split(',')
    preprocessed = []
    for ing in raw_ingredients:
        tokens = preprocess_ingredients(ing)
        for t in tokens:
            matched = fuzzy_match(t, COMMON_INGREDIENTS)
            preprocessed.append(matched)

    print("\n🧪 Matched Ingredients:", ', '.join(set(preprocessed)))

    # Track waste saved
    track_waste(user_id, preprocessed)

    # Recipe suggestions
    recipes = get_recipes_from_ingredients(preprocessed)
    if not recipes:
        print("No recipes found.")
        return

    display_recipes(recipes)

    try:
        choice = int(input("Select a recipe by number to view full details: ")) - 1
        if 0 <= choice < len(recipes):
            selected_recipe_id = recipes[choice]['id']
            recipe_info = get_recipe_details(selected_recipe_id)
            if recipe_info:
                display_recipe_details(recipe_info)
            else:
                print("Could not fetch recipe details.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()