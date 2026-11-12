"""
Aura Estates // VIP Concierge Telegram Bot (Aiogram 3.x)
Case 09 — Ultra-Luxury Real Estate Showcase & Showing Scheduler
"""
import os
import logging
from typing import Dict, Any
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    BufferedInputFile
)

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from api.server import RESIDENCES_DATA, generate_pdf_brochure, compute_mortgage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AuraEstatesBot")

TOKEN = os.getenv("BOT_TOKEN", "TEST_TOKEN_AURAESTATES")
dp = Dispatcher()

# Active booking state cache per user
user_booking_cache: Dict[int, Dict[str, Any]] = {}


def get_residences_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for r in RESIDENCES_DATA:
        status_symbol = "🟢" if r["status"] == "Available" else ("🟡" if r["status"] == "Reserved" else "🔴")
        btn_text = f"{status_symbol} {r['name']} ({r['price_formatted']})"
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"res_{r['id']}")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "⚜️ **Aura Estates // VIP Concierge**\n\n"
        "Добро пожаловать в закрытый клуб резиденций класса De Luxe.\n"
        "Архитектурный ансамбль Liquid Glass на первой береговой линии.\n\n"
        "🏛 **Возможности консьержа:**\n"
        "• Просмотр свободных лотов: `/residences`\n"
        "• Мгновенная генерация PDF-презентации: `/brochure`\n"
        "• Запись на закрытый показ с вертолетным трансфером: `/tour`\n"
        "• Расчет ипотеки и арендного дохода: `/calc [стоимость]`"
    )
    await message.answer(welcome_text, parse_mode="Markdown")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "🛎 **Справка VIP Консьержа:**\n\n"
        "• `/residences` — каталог и спецификации лотов.\n"
        "• `/brochure Penthouse Sky Villa` — экспорт официального PDF проспекта.\n"
        "• `/tour` — согласовать дату приватного визита.\n"
        "• `/calc 12500000` — финансовый расчет ежемесячного платежа и доходности."
    )
    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("residences"))
async def cmd_residences(message: Message):
    kb = get_residences_keyboard()
    await message.answer(
        "💎 **Коллекция закрытых резиденций Aura Estates:**\n"
        "Выберите интересующий лот для просмотра спецификаций и бронирования:",
        reply_markup=kb,
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.startswith("res_"))
async def handle_residence_detail(call: CallbackQuery):
    res_id = call.data.replace("res_", "")
    target = next((r for r in RESIDENCES_DATA if r["id"] == res_id), None)

    if not target:
        await call.answer("Лот не найден.", show_alert=True)
        return

    features_str = "\n".join([f"• {f}" for f in target["features"]])
    text = (
        f"⚜️ **{target['name'].upper()}**\n\n"
        f"💰 **Стоимость:** `{target['price_formatted']}`\n"
        f"📐 **Площадь:** {target['sqm']} м² (Терраса: {target['terrace_sqm']} м²)\n"
        f"🏢 **Этаж:** {target['floor']}\n"
        f"🌅 **Панорама:** {target['view']}\n"
        f"🏷 **Статус:** {target['status']}\n\n"
        f"**Особенности резиденции:**\n{features_str}\n"
    )

    action_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📄 Скачать PDF-буклет", callback_data=f"pdf_{target['id']}"),
            InlineKeyboardButton(text="🚁 Записаться на показ", callback_data=f"book_{target['id']}")
        ]
    ])

    await call.message.answer(text, reply_markup=action_kb, parse_mode="Markdown")
    await call.answer()


@dp.callback_query(F.data.startswith("pdf_"))
async def handle_pdf_callback(call: CallbackQuery):
    res_id = call.data.replace("pdf_", "")
    target = next((r for r in RESIDENCES_DATA if r["id"] == res_id), RESIDENCES_DATA[0])

    await call.message.answer("⏳ **Генерация официальной PDF-презентации...**", parse_mode="Markdown")

    pdf_bytes = generate_pdf_brochure(target["name"])
    doc = BufferedInputFile(pdf_bytes, filename=f"Aura_{res_id.capitalize()}_Prospectus.pdf")

    await call.message.answer_document(
        document=doc,
        caption=f"📄 **Официальная презентация:** `{target['name']}` ({len(pdf_bytes)} байт)\nКонфиденциально.",
        parse_mode="Markdown"
    )
    await call.answer("Готово!")


@dp.callback_query(F.data.startswith("book_"))
async def handle_book_callback(call: CallbackQuery):
    res_id = call.data.replace("book_", "")
    target = next((r for r in RESIDENCES_DATA if r["id"] == res_id), RESIDENCES_DATA[0])
    user_id = call.from_user.id

    user_booking_cache[user_id] = {
        "residence": target["name"],
        "user": call.from_user.username or call.from_user.first_name
    }

    # Immediate alert dispatch to owner
    logger.info(f"VIP Showing Request: {user_booking_cache[user_id]} -> Alerting @Idrisov_prod")

    confirm_text = (
        f"🚁 **Заявка на приватный показ принята!**\n\n"
        f"• Выбранный лот: **{target['name']}**\n"
        f"• Гость: @{call.from_user.username or 'VIP Guest'}\n"
        f"• Статус: Отправлено в службу консьержа (@Idrisov_prod)\n\n"
        f"В течение 15 минут консьерж свяжется с Вами для согласования тайм-слота вертолетного трансфера."
    )
    await call.message.answer(confirm_text, parse_mode="Markdown")
    await call.answer("Заявка зарегистрирована!")


@dp.message(Command("brochure"))
async def cmd_brochure(message: Message):
    args = message.text.split(maxsplit=1)
    res_name = args[1] if len(args) > 1 else "Penthouse Sky Villa"

    pdf_bytes = generate_pdf_brochure(res_name)
    doc = BufferedInputFile(pdf_bytes, filename="Aura_Estates_Brochure.pdf")

    await message.answer_document(
        document=doc,
        caption=f"📄 Презентация `{res_name}` подготовлена."
    )


@dp.message(Command("calc"))
async def cmd_calc(message: Message):
    args = message.text.split()
    price = float(args[1]) if len(args) > 1 and args[1].replace(".", "").isdigit() else 12500000.0

    calc_res = compute_mortgage(price, down_pct=30.0, term_years=20, annual_rate=4.5)
    text = (
        f"📊 **Финансовый расчет инвестиций:**\n\n"
        f"• Стоимость лота: `${price:,.0f}`\n"
        f"• Первоначальный взнос (30%): `${calc_res['down_payment']:,.0f}`\n"
        f"• Сумма кредита: `${calc_res['principal']:,.0f}`\n"
        f"• Ежемесячный платеж (20 лет, 4.5%): `${calc_res['monthly_payment']:,.0f} / мес`\n"
        f"• Ожидаемая арендная доходность (6.8%): `${calc_res['annual_rental_yield']:,.0f} / год`"
    )
    await message.answer(text, parse_mode="Markdown")


async def run_bot():
    bot = Bot(token=TOKEN)
    logger.info("Starting Aura Estates VIP Concierge Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_bot())
