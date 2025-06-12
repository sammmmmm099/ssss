import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("SessionGenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text(
        "**👋 Welcome to Session Generator Bot!**\n\n"
        "Use /genuser to generate a session string for your Telegram user account.\n\n"
        "**⚠️ 2FA is not supported in this version.**"
    )


@bot.on_message(filters.command("genuser"))
async def genuser(_, message: Message):
    await message.reply("📲 Send your phone number with country code (e.g., +919876543210):")
    phone_msg = await bot.listen(message.chat.id)
    phone = phone_msg.text

    user = Client(name="usergen", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await user.connect()

    try:
        code = await user.send_code(phone)
        await message.reply("📩 OTP sent to your Telegram. Please reply with the OTP:")
        otp_msg = await bot.listen(message.chat.id)
        otp_code = otp_msg.text.strip()

        await user.sign_in(phone_number=phone, phone_code_hash=code.phone_code_hash, phone_code=otp_code)

        string_session = await user.export_session_string()
        await user.disconnect()

        await message.reply(
            f"✅ **Session Generated Successfully!**\n\n"
            f"`{string_session}`\n\n"
            "⚠️ **Keep it safe & do not share it publicly!**"
        )
    except Exception as e:
        await message.reply(f"❌ Error: `{str(e)}`")
        await user.disconnect()


bot.run()
