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
# SMART MACRO TRADING AI v3
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
btc_reasons = []

if market["DXY"] == -1:
    btc_score += 25
    btc_reasons.append("Weak Dollar")

if market["DXY"] == 1:
    btc_score -= 25
    btc_reasons.append("Strong Dollar")

if market["BTC_WHALES"] == "ACCUMULATION":
    btc_score += 30
    btc_reasons.append("Whale Accumulation")

if market["BTC_WHALES"] == "DISTRIBUTION":
    btc_score -= 30
    btc_reasons.append("Whale Distribution")

if market["BTC_TREND"] == "BULLISH":
    btc_score += 20
    btc_reasons.append("Bullish Trend")

if market["BTC_TREND"] == "BEARISH":
    btc_score -= 20
    btc_reasons.append("Bearish Trend")

if market["VIX"] < 20:
    btc_score += 15
    btc_reasons.append("Low VIX")

if market["VIX"] > 25:
    btc_score -= 20
    btc_reasons.append("High VIX")

if market["FED"] == "DOVISH":
    btc_score += 10
    btc_reasons.append("Dovish Fed")

if market["FED"] == "HAWKISH":
    btc_score -= 15
    btc_reasons.append("Hawkish Fed")

# =========================================
# GOLD ENGINE
# =========================================

gold_score = 0
gold_reasons = []

disable_gold_trading = False

if market["GOLD_LOSSES"] >= 2:
    disable_gold_trading = True

if market["NEWS_RISK"]:
    disable_gold_trading = True

if market["DXY"] == -1:
    gold_score += 30
    gold_reasons.append("Weak Dollar")

if market["DXY"] == 1:
    gold_score -= 35
    gold_reasons.append("Strong Dollar")

if market["VIX"] > 25:
    gold_score += 20
    gold_reasons.append("Fear In Market")

if market["VIX"] < 18:
    gold_score -= 10
    gold_reasons.append("Risk On Market")

if market["FED"] == "DOVISH":
    gold_score += 20
    gold_reasons.append("Dovish Fed")

if market["FED"] == "HAWKISH":
    gold_score -= 30
    gold_reasons.append("Hawkish Fed")

if market["BONDS"] == "DOWN":
    gold_score += 20
    gold_reasons.append("Bond Yields Falling")

if market["BONDS"] == "UP":
    gold_score -= 20
    gold_reasons.append("Bond Yields Rising")

if market["GOLD_TREND"] == "BULLISH":
    gold_score += 15
    gold_reasons.append("Bullish Trend")

if market["GOLD_TREND"] == "BEARISH":
    gold_score -= 15
    gold_reasons.append("Bearish Trend")

# =========================================
# FILTERS
# =========================================

macro_conflict = False

if market["DXY"] == 1 and market["FED"] == "HAWKISH":
    macro_conflict = True

if market["BONDS"] == "UP" and market["DXY"] == 1:
    macro_conflict = True

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
# RESULTS
# =========================================

btc_signal = get_signal(btc_score)

btc_entry = market["BTC_PRICE"]
btc_sl = btc_entry - 1800
btc_tp1 = btc_entry + 3000
btc_tp2 = btc_entry + 6000

signal = "🚫 NO TRADE"

if disable_gold_trading:
    signal = "🚫 GOLD DISABLED"

elif macro_conflict:
    signal = "🚫 GOLD FILTER ACTIVE"

else:
    signal = get_signal(gold_score)

gold_entry = market["GOLD_PRICE"]
gold_sl = gold_entry - 18
gold_tp1 = gold_entry + 35
gold_tp2 = gold_entry + 60

# =========================================
# MESSAGE
# =========================================

report = f"""
===================================
SMART MACRO TRADING AI
===================================

🟠 BTC ANALYSIS
----------------------------
Signal : {btc_signal}
Score  : {btc_score}/100

Entry : {btc_entry}
SL    : {btc_sl}
TP1   : {btc_tp1}
TP2   : {btc_tp2}

===================================

🥇 GOLD ANALYSIS
----------------------------
Signal : {signal}
Score  : {gold_score}/100

Entry : {gold_entry}
SL    : {gold_sl}
TP1   : {gold_tp1}
TP2   : {gold_tp2}

===================================
"""

# =========================================
# TELEGRAM COMMAND
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ SMART MACRO BOT ONLINE\n\nاستخدم /signal"
    )

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(report)

# =========================================
# MAIN
# =========================================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal_command))

    print("BOT RUNNING...")

    app.run_polling()

if __name__ == "__main__":
    main() 
