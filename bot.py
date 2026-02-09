
import asyncio
import httpx
from pyrogram import Client, filters
from pyrogram.types import Message

# --- Configuration ---
API_ID = 28050953  # Replace with your API ID
API_HASH = "d49e36ab23fcc5410ec8f87ac38fe070"
BOT_TOKEN = "8235351743:AAHZBnkoR0XMzbLw-b6gMBb9CeAOLFSwF2Y"

# Your provided credentials
A4F_API_KEY = "ddc-a4f-f4e3b93097424827ae35b1494c5fd557"
MODEL = "provider-4/z-image-turbo"
# Official A4F OpenAI-compatible endpoint
API_URL = "https://api.a4f.co/v1/images/generations"

app = Client("image_gen_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "✨ **A4F Imagen-4 Bot Ready**\n\nSend me a prompt: `/gen a cyberpunk cat`"
    )

@app.on_message(filters.command("gen"))
async def generate(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Please provide a prompt.")

    prompt = message.text.split(None, 1)[1]
    status_msg = await message.reply_text("⏳ `Generating image via A4F...`")

    headers = {
        "Authorization": f"Bearer {A4F_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # A4F follows OpenAI format
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    async with httpx.AsyncClient() as httpx_client:
        try:
            # Increased timeout as image generation can take 15-30 seconds
            response = await httpx_client.post(API_URL, json=payload, headers=headers, timeout=60.0)
            
            if response.status_code != 200:
                return await status_msg.edit(f"❌ **API Error:** {response.status_code}\n`{response.text}`")

            data = response.json()
            image_url = data['data'][0]['url']
            
            await message.reply_photo(photo=image_url, caption=f"✅ **Model:** {MODEL}\n📝 **Prompt:** {prompt}")
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"❌ **System Error:** `{type(e).__name__}`\n{str(e)}")

if __name__ == "__main__":
    app.run()
