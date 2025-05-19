import os

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from together import Together
import asyncio
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = Together()


async def fake_search_recipes(dish: str):
    return f"🧑‍🍳 Scanning 100+ {dish} recipes..."


async def fake_get_nutrition(dish: str):
    """Simulate "nutrition analysis" without real APIs"""
    nutrition = {"pasta": "450 kcal | 32g carbs", "salad": "120 kcal | 5g carbs"}.get(
        dish.lower(), "500 kcal | 40g carbs"
    )
    yield f"\n📊 Nutrition (approx): {nutrition}"


async def fake_save_to_db(dish: str, generated_recipe: str):
    await asyncio.sleep(2)
    print(f"saved {dish}: {generated_recipe} to db")


@app.get("/recipe/stream")
async def stream_recipe(dish: str):
    async def generate():
        # PRE-STREAM
        yield "🧑‍🍳 Scanning 100+ recipes..."
        await asyncio.sleep(1.2)

        # LLM STREAMING
        response = await client.chat.completions.create(
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
        async for chunk in response:
            if token := chunk["choices"][0]["delta"].get("content"):
                full_recipe += token
                yield token
                await asyncio.sleep(0.1)

        # POST-STREAM
        yield fake_get_nutrition(dish)
        await asyncio.sleep(0.5)

        # BACKGROUND TASK
        asyncio.create_task(fake_save_to_db(dish, full_recipe))

    return StreamingResponse(generate())
