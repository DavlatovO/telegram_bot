import asyncio
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from oyat import getOyat
from quran import getSurah
from db_saver import save_user
from agent_007 import send_to_admin
import os
from dotenv import load_dotenv
from aiohttp import web  # Required for handling a dummy server

# Load environment variables from the .env file
load_dotenv()

# Get the token
API_TOKEN = os.getenv("bot_token")

# Validate the token
if API_TOKEN is None:
    raise ValueError("bot_token is not set in the .env file.")

def split_into_chunks(input_string, max_length):
    parts = []
    while len(input_string) > max_length:
        # Find the last space within the allowed range
        split_index = input_string[:max_length].rfind(" ")
        if split_index == -1:  # No spaces found, force split at max_length
            split_index = max_length

        # Add the chunk to the list
        parts.append(input_string[:split_index].strip())

        # Remove the processed chunk from the input string
        input_string = input_string[split_index:].strip()

    # Add the remaining part of the string
    if input_string:
        parts.append(input_string)

    return parts

async def main():
    # Initialize the bot and dispatcher
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Command handler for `/start`
    @dp.message(Command(commands=["start"]))
    async def send_welcome(message: Message):
        await message.reply("Hello! This bot is all about Qur'an.\nType any chapter and verse(e.g. 78:8 or 17). \n The bot is running on test.")

    # Command handler for `/help`
    @dp.message(Command(commands=["help"]))
    async def send_help(message: Message):
        await message.answer("Contact: @Bestoftheplayers")

    # Message handler for user inputs
    @dp.message()
    async def handle_message(message: Message):
        user1 = message.from_user
        user_id = user1.id
        is_bot = user1.is_bot
        first_name = user1.first_name
        username = user1.username or "N/A"
        user_type = message.chat.type
        message_text = message.text
        message_id = message.message_id
        try:
            save_user(user_id, is_bot, first_name, username, user_type, message_text, message_id)
            send_to_admin(username, user_id, message_text)
        except:
            pass   
        if re.fullmatch(r"\d+", message.text):  # Matches a single number
            surah_number = int(message.text)
            response = getSurah('uzb-muhammadsodikmu', surah_number)
            post_list = split_into_chunks(response, 4096)
            for i in post_list:
                await message.reply(i or "Could not fetch Ayah.")
        elif re.fullmatch(r"\d+:\d+", message.text):  # Matches "number:number" (e.g., "89:2")
            surah_number, ayah_number = map(int, message.text.split(":"))
            response = getOyat('uzb-muhammadsodikmu', surah_number, ayah_number)
            await message.reply(response or "Could not fetch Ayah.")
        else:
            await message.reply("Invalid input format. Use a single number (e.g. 78) or a colon-separated format (e.g., 78:8).")

    # Start the polling and a dummy web server
    runner = web.AppRunner(web.Application())  # Dummy server to bind a port
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()
    print("Dummy server running on port", os.getenv("PORT", 8080))

    # Start polling updates from Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
