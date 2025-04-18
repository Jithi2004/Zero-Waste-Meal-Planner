# 🥗 Zero Waste Meal Planner

A smart and sustainable web app that helps users reduce food waste by recommending recipes based on available ingredients. Built with Flask, NLP, and the Spoonacular API, it supports fuzzy ingredient matching and tracks how much food waste is saved.

## 🌱 Features

- 🔍 Ingredient-Based Recipe Suggestions 
   Enter leftover ingredients and get recipe suggestions instantly.

- 🧠 Natural Language Processing (NLP)  
   Uses spaCy to intelligently extract ingredient names from messy or unstructured input.

- 🍽️ Fuzzy Ingredient Matching 
   Misspelled or vague ingredient names are intelligently corrected using FuzzyWuzzy.

- 🧾 Waste Tracking System  
  Tracks how much food waste you’ve saved (in grams) based on ingredient usage.

- 🖼️ Clean UI  
  Simple, responsive web interface for entering ingredients and viewing recipe suggestions.

## 🔧 Technologies Used

- Backend: Python, Flask, spaCy, Requests, FuzzyWuzzy
- Frontend: HTML, CSS, JavaScript
- API: [Spoonacular API](https://spoonacular.com/food-api)

  
## 🚀 Getting Started

#. Clone the Repository
```bash
git clone https://github.com/Jithi2004/Zero-Waste-Meal-Planner.git

# Navigate into the project directory
cd zero-waste-meal-planner

# Install dependencies (if applicable)
pip install -r requirements.txt

# Run the application
python app.py

🙌 Acknowledgements
-Spoonacular API
-spaCy NLP
-FuzzyWuzzy
