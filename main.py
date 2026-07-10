import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# .env faylni yuklash
load_dotenv("token.env")

# ===== TOKEN =====
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

dp = Dispatcher(storage=MemoryStorage())

# ==========================
# HOLATLAR
# ==========================
class Audit(StatesGroup):
    korxona = State()
    energiya = State()
    mahsulot = State()


# ==========================
# MENYU
# ==========================
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Energiya hisoblash")],
        [KeyboardButton(text="📖 Formula")],
        [KeyboardButton(text="📘 Qo'llanma")],
        [KeyboardButton(text="👨‍💻 Muallif")]
    ],
    resize_keyboard=True
)


# ==========================
# START
# ==========================
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Energetik Auditor Botiga xush kelibsiz.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang.",
        reply_markup=menu
    )


# ==========================
# HISOBLASH
# ==========================
@dp.message(F.text == "📊 Energiya hisoblash")
async def hisoblash(message: Message, state: FSMContext):
    await state.set_state(Audit.korxona)
    await message.answer("🏭 Korxona nomini kiriting:")


@dp.message(Audit.korxona)
async def korxona(message: Message, state: FSMContext):
    await state.update_data(korxona=message.text)
    await state.set_state(Audit.energiya)
    await message.answer("⚡ Elektr energiyasi (kWh) ni kiriting:")


@dp.message(Audit.energiya)
async def energiya(message: Message, state: FSMContext):
    try:
        qiymat = float(message.text)
    except ValueError:
        await message.answer("❌ Faqat son kiriting!")
        return

    await state.update_data(energiya=qiymat)
    await state.set_state(Audit.mahsulot)
    await message.answer("📦 Mahsulot miqdorini kiriting (kg):")


@dp.message(Audit.mahsulot)
async def mahsulot(message: Message, state: FSMContext):
    try:
        mahsulot = float(message.text)
    except ValueError:
        await message.answer("❌ Faqat son kiriting!")
        return

    data = await state.get_data()

    korxona = data["korxona"]
    energiya = data["energiya"]

    natija = energiya / mahsulot

    if natija <= 0.35:
        holat = "🟢 Yaxshi"
        tavsiya = "Energiya samaradorligi yaxshi."
    elif natija <= 0.50:
        holat = "🟡 O'rtacha"
        tavsiya = "Elektr uskunalarini texnik ko'rikdan o'tkazish tavsiya etiladi."
    else:
        holat = "🔴 Yuqori"
        tavsiya = "Energiya auditi o'tkazish va energiya tejovchi texnologiyalarni joriy etish tavsiya etiladi."

    await message.answer(
        f"""
📊 HISOBOT

🏭 Korxona:
{korxona}

⚡ Elektr energiyasi:
{energiya:.2f} kWh

📦 Mahsulot:
{mahsulot:.2f} kg

📈 Solishtirma energiya sarfi:
{natija:.3f} kWh/kg

{holat}

💡 Tavsiya:
{tavsiya}
""",
        reply_markup=menu
    )

    await state.clear()


# ==========================
# FORMULA
# ==========================
@dp.message(F.text == "📖 Formula")
async def formula(message: Message):
    await message.answer(
        """
📖 Formula

d = W / A

W - elektr energiyasi (kWh)

A - mahsulot (kg)

d - solishtirma energiya sarfi (kWh/kg)
"""
    )


# ==========================
# QO'LLANMA
# ==========================
@dp.message(F.text == "📘 Qo'llanma")
async def qollanma(message: Message):
    await message.answer(
        """
📘 Qo'llanma

1. 📊 Energiya hisoblash tugmasini bosing.

2. Korxona nomini kiriting.

3. Elektr energiyasi qiymatini kiriting.

4. Mahsulot miqdorini kiriting.

5. Bot natijani avtomatik hisoblaydi.
"""
    )


# ==========================
# MUALLIF
# ==========================
@dp.message(F.text == "👨‍💻 Muallif")
async def muallif(message: Message):
    await message.answer(
        """
👨‍💻 Muallif

Xulkaroy Yusupaliyeva

Mini loyiha

Energetik Auditor Telegram boti
2026
"""
    )


# ==========================
# ISHGA TUSHIRISH
# ==========================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())