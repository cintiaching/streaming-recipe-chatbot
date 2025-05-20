import os
import time
import logging

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from together import Together
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = Together()
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


def fake_search_recipes(dish: str):
    time.sleep(1.2)
    return None


def fake_get_nutrition(dish: str):
    """Simulate "nutrition analysis" without real APIs"""
    time.sleep(0.5)
    nutrition = {"pasta": "450 kcal | 32g carbs", "salad": "120 kcal | 5g carbs"}.get(
        dish.lower(), "500 kcal | 40g carbs"
    )
    return f"\n📊 Nutrition (approx): {nutrition}\n"


def fake_save_to_db(dish: str, generated_recipe: str):
    time.sleep(2)
    print(f"saved {dish}: {generated_recipe} to db")


@app.get("/recipe/stream/")
def stream_recipe(dish: str):
    def generate():
        # PRE-GENERATION
        search_start = time.time()
        yield f"🧑‍🍳 Scanning 100+ {dish} recipes...\n"
        fake_search_recipes(dish)
        logger.info(f"Searching recipes took {time.time() - search_start:.2f} seconds")

        # LLM STREAMING
        llm_start = time.time()
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": f"Give me a recipe for {dish}",
                }
            ],
            stream=True,
        )

        full_recipe = ""
        for chunk in response:
            if token := chunk.choices[0].delta.content:
                full_recipe += token
                yield token

        logger.info(f"LLM STREAMING took {time.time() - llm_start:.2f} seconds")

        # POST-GENERATION
        post_gen_start = time.time()
        yield fake_get_nutrition(dish)
        logger.info(f"Get nutrition took {time.time() - post_gen_start:.2f} seconds")

        # BACKGROUND TASK
        background_start = time.time()
        fake_save_to_db(dish, full_recipe)
        logger.info(f"BACKGROUND TASK took {time.time() - background_start:.2f} seconds")
        yield "🧑‍🍳 Complete!"

    return StreamingResponse(generate())
