import asyncio
import httpx
from pyrogram import Client, filters
from pyrogram.types import Message

# --- Configuration ---
API_ID = 28050953  # Replace with your API ID
API_HASH = "d49e36ab23fcc5410ec8f87ac38fe070"
BOT_TOKEN = "8235351743:AAHZBnkoR0XMzbLw-b6gMBb9CeAOLFSwF2Y"

A4F_API_KEY = "ddc-a4f-f4e3b93097424827ae35b1494c5fd557"
MODEL = "provider-4/imagen-4"
API_URL = "https://api.a4f.ai/v1/image/generations" # Ensure this matches your provider's endpoint

app = Client("image_gen_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "Hello! Send me a prompt using `/gen <your prompt>` and I'll create an image for you using Imagen-4."
    )

@app.on_message(filters.command("gen"))
async def generate(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide a prompt. Example: `/gen a futuristic city`.")

    prompt = message.text.split(None, 1)[1]
    status_msg = await message.reply_text("🎨 Generating your image, please wait...")

    headers = {
        "Authorization": f"Bearer {A4F_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    async with httpx.AsyncClient() as httpx_client:
        try:
            response = await httpx_client.post(API_URL, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()
            data = response.json()

            # Assuming the API returns a URL in ['data'][0]['url']
            image_url = data['data'][0]['url']
            
            await message.reply_photo(photo=image_url, caption=f"Prompt: {prompt}")
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
