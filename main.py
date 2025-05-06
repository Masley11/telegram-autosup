import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType
from aiogram.utils import executor
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = int(os.getenv("TELEGRAM_CHANNEL_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Stocke les messages suspects pour suppression après 1h
messages_to_delete = []

# Identifiants ou noms des bots indésirables
BANNED_BOTS = [
    "sakura_500bot",
    "Otakubot5k",
    "Franklin Saint",
    "🍀🍀🍀🍀🍀🍀🍀🍀",
]

@dp.channel_post_handler()
async def handle_channel_post(message: types.Message):
    sender = message.from_user
    if sender and (sender.username in BANNED_BOTS or sender.full_name in BANNED_BOTS):
        print(f"Message suspect de {sender.username or sender.full_name} détecté")
        messages_to_delete.append({
            "message_id": message.message_id,
            "date": datetime.utcnow()
        })

async def delete_old_messages():
    while True:
        now = datetime.utcnow()
        to_delete = [m for m in messages_to_delete if now - m["date"] >= timedelta(hours=1)]

        for msg in to_delete:
            try:
                await bot.delete_message(chat_id=CHANNEL_ID, message_id=msg["message_id"])
                print(f"Message {msg['message_id']} supprimé.")
            except Exception as e:
                print(f"Erreur de suppression: {e}")
            messages_to_delete.remove(msg)

        await asyncio.sleep(60)

async def main():
    asyncio.create_task(delete_old_messages())
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
