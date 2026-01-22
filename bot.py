import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.filters import Command, Text
from yt_dlp import YoutubeDL
import asyncio

logging.basicConfig(level=logging.INFO)

API_TOKEN = "8405076051:AAF2FSoiZymcBKL7rADSQpwnsEUJbu2wPW4"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="verify_sub")]
        ]
    )
    await message.answer(
        "Assalomu alaykum! Botimizga Xush kelibsiz.\n"
        "Siz bot orqali quyidagilarni yuklab olishingiz mumkin:\n"
        "> Instagram - post, stories, reels\n\n"
        "Botdan foydalanish uchun quyidagi kanallarimizga obuna bo'ling!!!\n"
        "1. https://t.me/premium_channel_official\n"
        "2. https://t.me/qaxxorvusa",
        reply_markup=keyboard
    )

@dp.callback_query(Text("verify_sub"))
async def verify_subscription(callback: types.CallbackQuery):
    await callback.message.answer("Obunangiz tasdiqlandi ✅\n\nIltimos, video havolasini yuboring:")
    await callback.answer()

@dp.message()
async def handle_video(message: types.Message):
    url = message.text.strip()
    await message.reply("Yuklanmoqda ⏳, biroz kuting...")

    try:
        ydl_opts = {"outtmpl": "video.%(ext)s"}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = f"video.{info['ext']}"

        await message.reply_video(video=InputFile(video_file))
        os.remove(video_file)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling())
