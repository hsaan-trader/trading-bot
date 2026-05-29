import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 البوت شغال بنجاح\n\n"
        "/gold = تحليل الذهب\n"
        "/btc = تحليل البيتكوين\n"
        "/fear = مؤشر الخوف"
    )

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟡 GOLD ANALYSIS\n\n"
        "الاتجاه الحالي: مراقبة\n"
        "راقب قوة الدولار قبل الدخول."
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "₿ BTC ANALYSIS\n\n"
        "السوق متذبذب حالياً.\n"
        "يفضل انتظار تأكيد الاتجاه."
    )

async def fear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😨 مؤشر الخوف والطمع:\n"
        "السوق حالياً بحالة خوف."
    )

# =========================
# MAIN
# =========================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("fear", fear))

    print("BOT IS RUNNING...")

    app.run_polling()

if __name__ == "__main__":
    main()
