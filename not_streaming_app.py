import os
import time

from fastapi import FastAPI
from together import Together
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = Together()


def fake_search_recipes(dish: str):
    time.sleep(1.2)
    return None


def fake_get_nutrition(dish: str):
    """Simulate "nutrition analysis" without real APIs"""
    nutrition = {"pasta": "450 kcal | 32g carbs", "salad": "120 kcal | 5g carbs"}.get(
        dish.lower(), "500 kcal | 40g carbs"
    )
    return f"\n📊 Nutrition (approx): {nutrition}\n"


def fake_save_to_db(dish: str, generated_recipe: str):
    time.sleep(2)
    print(f"saved {dish}: {generated_recipe} to db")


@app.get("/recipe/not_stream/")
def stream_recipe(dish: str):
    fake_search_recipes(dish)
    time.sleep(1.2)

    # LLM NOT STREAMING
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": f"Give me a recipe for {dish}",
            }
        ],
    )
    full_recipe = response.choices[0].message.content

    nutrition = fake_get_nutrition(dish)
    time.sleep(0.5)

    # BACKGROUND TASK (blocking return)
    fake_save_to_db(dish, full_recipe)

    return {
        "full_recipe": full_recipe,
        "nutrition": nutrition,
    }
