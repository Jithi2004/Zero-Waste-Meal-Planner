from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy
import requests
from fuzzywuzzy import process
import datetime

app = Flask(__name__)
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

API_KEY = "04fa1ab34bca4783863f4309782bfdbb"

COMMON_INGREDIENTS = [
    "tomato", "cheese", "onion", "garlic", "milk", "egg", "flour",
    "butter", "carrot", "pepper", "potato", "spinach", "rice",
    "chicken", "beef", "bread", "salt", "sugar", "oil", "vinegar"
]

user_waste_tracker = {}

# --- Utility Functions ---
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

def estimate_saved_waste(ingredients):
    estimated_grams_saved = len(ingredients) * 100  # assume 100g per item
    return estimated_grams_saved

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_recipes", methods=["POST"])
def get_recipes():
    data = request.json
    raw_input = data.get("ingredients", "")
    raw_ingredients = raw_input.split(',')
    preprocessed = []
    for ing in raw_ingredients:
        tokens = preprocess_ingredients(ing)
        for t in tokens:
            matched = fuzzy_match(t, COMMON_INGREDIENTS)
            preprocessed.append(matched)
    recipes = get_recipes_from_ingredients(preprocessed)
    return jsonify(recipes)

@app.route("/recipe/<int:recipe_id>")
def recipe_details(recipe_id):
    details = get_recipe_details(recipe_id)
    return jsonify(details)

@app.route("/track_waste", methods=["POST"])
def track_waste():
    data = request.json
    user_id = data.get("user_id", "default_user")
    ingredients = data.get("ingredients", [])

    saved_grams = estimate_saved_waste(ingredients)

    today = datetime.date.today().isoformat()
    if user_id not in user_waste_tracker:
        user_waste_tracker[user_id] = {}
    user_waste_tracker[user_id][today] = user_waste_tracker[user_id].get(today, 0) + saved_grams

    return jsonify({
        "message": "Waste saved tracked successfully.",
        "estimated_grams_saved": saved_grams,
        "total_today": user_waste_tracker[user_id][today]
    })

if __name__ == "__main__":
    app.run(debug=True)