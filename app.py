from flask import Flask, render_template, request
from models import RecipeFinder

app = Flask(__name__)
finder = RecipeFinder(api_key="611b7451167449fab485c3bb5ac41e16")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    raw = request.args.get("ingredients", "")
    diet = request.args.get("diet", "")
    meal_type = request.args.get("meal_type", "")
    number = int(request.args.get("number", 10))

    ingredients = [i.strip() for i in raw.split(",") if i.strip()]
    results = []

    if ingredients:
        results = finder.search_by_ingredients(
            ingredients,
            diet=diet,
            meal_type=meal_type,
            number=number
        )

    return render_template("index.html",
        results=results,
        query=raw,
        selected_diet=diet,
        selected_meal_type=meal_type,
        selected_number=number
    )

if __name__ == "__main__":
    app.run(debug=True)
