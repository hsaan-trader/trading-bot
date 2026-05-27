from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = "8778919198:AAEYXH-LxbTy1vec-WkIPT9pTfXE6ZvOllw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Gold Apex Bot

الأوامر:

/gold = إشارة ذهب
/cot = تحليل COT
/signal = إشارة تداول
"""

    await update.message.reply_text(text)

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🥇 GOLD SIGNAL

📈 BUY XAUUSD

🎯 Entry: 4515
🛑 SL: 4505

✅ TP1: 4525
✅ TP2: 4535
"""

    await update.message.reply_text(text)

async def cot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📊 COT REPORT

🐳 Commercial Long: 69,520
🐳 Commercial Short: 261,149

📉 النظرة:
Bearish
"""

    await update.message.reply_text(text)

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    direction = random.choice(["BUY", "SELL"])

    text = f"""
📡 LIVE SIGNAL

{direction} XAUUSD
"""

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gold", gold))
app.add_handler(CommandHandler("cot", cot))
app.add_handler(CommandHandler("signal", signal))

print("🔥 Bot Running...")

app.run_polling()
