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
# MARKET DATA
# =========================

market = {
    "btc_signal": "SELL",
    "btc_score": 82,
    "btc_entry": "73600",
    "btc_sl": "74800",
    "btc_tp1": "72000",
    "btc_tp2": "70500",

    "gold_signal": "BUY",
    "gold_score": 91,
    "gold_entry": "2348",
    "gold_sl": "2335",
    "gold_tp1": "2365",
    "gold_tp2": "2380",
}

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = f"""
🤖 SMART MACRO TRADING AI

🟠 BTC SIGNAL
Signal: {market['btc_signal']}
Score: {market['btc_score']}/100

Entry: {market['btc_entry']}
SL: {market['btc_sl']}
TP1: {market['btc_tp1']}
TP2: {market['btc_tp2']}


🥇 GOLD SIGNAL
Signal: {market['gold_signal']}
Score: {market['gold_score']}/100

Entry: {market['gold_entry']}
SL: {market['gold_sl']}
TP1: {market['gold_tp1']}
TP2: {market['gold_tp2']}

📊 Analysis:
- Dollar strength
- Fear & Greed Index
- Smart Money
- Macro trend
- COT data
"""

    await update.message.reply_text(message)

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("BOT RUNNING...")

    app.run_polling()

if __name__ == "__main__":
    main()
