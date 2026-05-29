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

# =========================================
# MARKET DATA
# =========================================

market = {
    "DXY": 1,
    "VIX": 27,
    "FED": "HAWKISH",
    "NEWS_RISK": False,

    "GOLD_PRICE": 2360,
    "GOLD_TREND": "BULLISH",
    "BONDS": "UP",

    "BTC_PRICE": 108000,
    "BTC_WHALES": "ACCUMULATION",
    "BTC_TREND": "BULLISH",

    "GOLD_LOSSES": 1
}

# =========================================
# BTC ENGINE
# =========================================

btc_score = 0

if market["DXY"] == -1:
    btc_score += 25

if market["DXY"] == 1:
    btc_score -= 25

if market["BTC_WHALES"] == "ACCUMULATION":
    btc_score += 30

if market["BTC_TREND"] == "BULLISH":
    btc_score += 20

if market["VIX"] > 25:
    btc_score -= 20

if market["FED"] == "HAWKISH":
    btc_score -= 15

# =========================================
# GOLD ENGINE
# =========================================

gold_score = 0
disable_gold_trading = False

if market["GOLD_LOSSES"] >= 2:
    disable_gold_trading = True

if market["NEWS_RISK"]:
    disable_gold_trading = True

if market["DXY"] == -1:
    gold_score += 30

if market["DXY"] == 1:
    gold_score -= 35

if market["VIX"] > 25:
    gold_score += 20

if market["FED"] == "DOVISH":
    gold_score += 20

if market["FED"] == "HAWKISH":
    gold_score -= 30

if market["BONDS"] == "DOWN":
    gold_score += 20

if market["BONDS"] == "UP":
    gold_score -= 20

if market["GOLD_TREND"] == "BULLISH":
    gold_score += 15

# =========================================
# SIGNAL FUNCTION
# =========================================

def get_signal(score):
    if score >= 80:
        return "🔥 STRONG BUY"

    elif score >= 60:
        return "🟡 MEDIUM BUY"

    elif score <= -80:
        return "🔥 STRONG SELL"

    elif score <= -60:
        return "🟡 MEDIUM SELL"

    else:
        return "🚫 NO TRADE"

# =========================================
# SIGNALS
# =========================================

btc_signal = get_signal(btc_score)
signal = get_signal(gold_score)

btc_entry = market["BTC_PRICE"]
btc_sl = btc_entry - 1800
btc_tp1 = btc_entry + 3000
btc_tp2 = btc_entry + 6000

gold_entry = market["GOLD_PRICE"]
gold_sl = gold_entry - 18
gold_tp1 = gold_entry + 35
gold_tp2 = gold_entry + 60

# =========================================
# TELEGRAM BOT
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = f"""
🤖 SMART MACRO TRADING AI

🟠 BTC SIGNAL
Signal: {btc_signal}
Score: {btc_score}/100

Entry: {btc_entry}
SL: {btc_sl}
TP1: {btc_tp1}
TP2: {btc_tp2}

🥇 GOLD SIGNAL
Signal: {signal}
Score: {gold_score}/100

Entry: {gold_entry}
SL: {gold_sl}
TP1: {gold_tp1}
TP2: {gold_tp2}
"""

    await update.message.reply_text(message)

# =========================================
# MAIN
# =========================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("BOT RUNNING...")

    app.run_polling()

if __name__ == "__main__":
    main()
