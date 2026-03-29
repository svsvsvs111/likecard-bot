import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from config import BOT_TOKEN
from likecard_api import get_products, check_balance
from database import add_subscription, get_subscriptions
from scheduler import checker

cached_products = {}

# 🟢 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 المنتجات", callback_data="products")],
        [InlineKeyboardButton("💰 الرصيد", callback_data="balance")],
        [InlineKeyboardButton("📋 طلباتي", callback_data="orders")]
    ]

    await update.message.reply_text(
        "👋 مرحباً بك\nاختر:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 📦 عرض المنتجات
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = get_products()
    keyboard = []
    cached_products.clear()

    for p in data.get("data", [])[:10]:
        cached_products[str(p["id"])] = p["name"]

        keyboard.append([
            InlineKeyboardButton(p["name"], callback_data=f"buy_{p['id']}")
        ])

    await query.edit_message_text(
        "📦 اختر منتج:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🛒 اختيار منتج
async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = query.data.split("_")[1]
    name = cached_products.get(product_id, "منتج")

    user_id = query.from_user.id

    success = add_subscription(user_id, int(product_id), name)

    if not success:
        await query.edit_message_text("⚠️ مضاف مسبقاً")
        return

    await query.edit_message_text(f"✅ تم التفعيل: {name}")

# 💰 الرصيد
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = check_balance()
    balance = data.get("data", {}).get("balance", 0)

    await query.edit_message_text(f"💰 الرصيد: {balance}")

# 📋 الطلبات
async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subs = get_subscriptions()
    user_id = query.from_user.id

    text = "📋 طلباتك:\n\n"

    for s in subs:
        if s[1] == user_id:
            text += f"- {s[3]}\n"

    if text == "📋 طلباتك:\n\n":
        text = "❌ لا يوجد طلبات"

    await query.edit_message_text(text)

# 🎯 التحكم في الأزرار
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    if data == "products":
        await show_products(update, context)
    elif data == "balance":
        await balance(update, context)
    elif data == "orders":
        await orders(update, context)
    elif data.startswith("buy_"):
        await choose(update, context)

# 🚀 التشغيل الصحيح (مهم جداً)
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handler))

    print("Bot running...")

    # تشغيل الفحص بالخلفية
    asyncio.create_task(checker(app.bot))

    # تشغيل البوت
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
