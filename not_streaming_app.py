import os
import logging
import time

from fastapi import FastAPI
from together import Together
from dotenv import load_dotenv

from streaming_app import fake_search_recipes, fake_get_nutrition, fake_save_to_db

load_dotenv()
app = FastAPI()
client = Together()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


@app.get("/recipe/not_stream/")
def stream_recipe(dish: str):
    start_time = time.time()
    fake_search_recipes(dish)

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

    # BACKGROUND TASK (blocking return)
    fake_save_to_db(dish, full_recipe)
    logger.info(f"Everything took {time.time() - start_time:.2f} seconds")
    return {
        "full_recipe": full_recipe,
        "nutrition": nutrition,
    }
