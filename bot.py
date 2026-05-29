# ==================================================
# SMART MACRO TRADING AI v5
# INSTITUTIONAL + COT + GOLD PROTECTION
# ==================================================

# ==================================================
# MARKET DATA
# ==================================================

market = {

    # ======================================
    # MACRO
    # ======================================

    "DXY": -1,                 # -1 weak / 1 strong
    "VIX": 19,
    "FED": "DOVISH",           # DOVISH / HAWKISH
    "NEWS_RISK": False,

    # ======================================
    # COT DATA
    # ======================================

    "COT_GOLD": "BULLISH",
    "COT_BTC": "BULLISH",

    # ======================================
    # GOLD
    # ======================================

    "GOLD_PRICE": 2360,

    # Multi Timeframe
    "GOLD_DAILY": "BULLISH",
    "GOLD_4H": "BULLISH",
    "GOLD_1H": "BULLISH",

    "BONDS": "DOWN",

    # Risk Protection
    "GOLD_LOSSES": 0,

    # ======================================
    # BTC
    # ======================================

    "BTC_PRICE": 108000,

    # Multi Timeframe
    "BTC_DAILY": "BULLISH",
    "BTC_4H": "BULLISH",
    "BTC_1H": "BULLISH",

    "BTC_WHALES": "ACCUMULATION"
}

# ==================================================
# SIGNAL FUNCTION
# ==================================================

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

# ==================================================
# MULTI TIMEFRAME CONFIRMATION
# ==================================================

def timeframe_confirmation(daily, h4, h1):

    # BUY
    if (
        daily == "BULLISH"
        and h4 == "BULLISH"
        and h1 == "BULLISH"
    ):
        return "BULLISH"

    # SELL
    if (
        daily == "BEARISH"
        and h4 == "BEARISH"
        and h1 == "BEARISH"
    ):
        return "BEARISH"

    return "MIXED"

# ==================================================
# BTC ENGINE
# ==================================================

btc_score = 0
btc_reasons = []

btc_tf = timeframe_confirmation(
    market["BTC_DAILY"],
    market["BTC_4H"],
    market["BTC_1H"]
)

# --------------------------------------
# DXY
# --------------------------------------

if market["DXY"] == -1:

    btc_score += 25
    btc_reasons.append("Weak Dollar")

if market["DXY"] == 1:

    btc_score -= 25
    btc_reasons.append("Strong Dollar")

# --------------------------------------
# WHALES
# --------------------------------------

if market["BTC_WHALES"] == "ACCUMULATION":

    btc_score += 30
    btc_reasons.append("Whale Accumulation")

if market["BTC_WHALES"] == "DISTRIBUTION":

    btc_score -= 30
    btc_reasons.append("Whale Distribution")

# --------------------------------------
# VIX
# --------------------------------------

if market["VIX"] < 20:

    btc_score += 15
    btc_reasons.append("Low VIX")

if market["VIX"] > 25:

    btc_score -= 20
    btc_reasons.append("High VIX")

# --------------------------------------
# FED
# --------------------------------------

if market["FED"] == "DOVISH":

    btc_score += 15
    btc_reasons.append("Dovish Fed")

if market["FED"] == "HAWKISH":

    btc_score -= 20
    btc_reasons.append("Hawkish Fed")

# --------------------------------------
# MULTI TIMEFRAME
# --------------------------------------

if btc_tf == "BULLISH":

    btc_score += 25
    btc_reasons.append("Bullish Multi Timeframe")

if btc_tf == "BEARISH":

    btc_score -= 25
    btc_reasons.append("Bearish Multi Timeframe")

# --------------------------------------
# BTC COT FILTER
# --------------------------------------

if market["COT_BTC"] == "BULLISH":

    btc_score += 10
    btc_reasons.append("Bullish Institutional Positioning")

if market["COT_BTC"] == "BEARISH":

    btc_score -= 10
    btc_reasons.append("Bearish Institutional Positioning")

# ==================================================
# GOLD ENGINE
# ==================================================

gold_score = 0
gold_reasons = []

disable_gold = False

gold_tf = timeframe_confirmation(
    market["GOLD_DAILY"],
    market["GOLD_4H"],
    market["GOLD_1H"]
)

# ==================================================
# GOLD SAFETY FILTERS
# ==================================================

# --------------------------------------
# Revenge Protection
# --------------------------------------

if market["GOLD_LOSSES"] >= 2:

    disable_gold = True

# --------------------------------------
# High Impact News
# --------------------------------------

if market["NEWS_RISK"]:

    disable_gold = True

# --------------------------------------
# DXY
# --------------------------------------

if market["DXY"] == -1:

    gold_score += 30
    gold_reasons.append("Weak Dollar")

if market["DXY"] == 1:

    gold_score -= 35
    gold_reasons.append("Strong Dollar")

# --------------------------------------
# VIX
# --------------------------------------

if market["VIX"] > 25:

    gold_score += 20
    gold_reasons.append("Fear In Market")

if market["VIX"] < 18:

    gold_score -= 10
    gold_reasons.append("Risk On Market")

# --------------------------------------
# FED
# --------------------------------------

if market["FED"] == "DOVISH":

    gold_score += 20
    gold_reasons.append("Dovish Fed")

if market["FED"] == "HAWKISH":

    gold_score -= 30
    gold_reasons.append("Hawkish Fed")

# --------------------------------------
# BONDS
# --------------------------------------

if market["BONDS"] == "DOWN":

    gold_score += 20
    gold_reasons.append("Bond Yields Falling")

if market["BONDS"] == "UP":

    gold_score -= 20
    gold_reasons.append("Bond Yields Rising")

# --------------------------------------
# MULTI TIMEFRAME
# --------------------------------------

if gold_tf == "BULLISH":

    gold_score += 25
    gold_reasons.append("Bullish Multi Timeframe")

if gold_tf == "BEARISH":

    gold_score -= 25
    gold_reasons.append("Bearish Multi Timeframe")

# --------------------------------------
# GOLD COT FILTER
# --------------------------------------

if market["COT_GOLD"] == "BULLISH":

    gold_score += 15
    gold_reasons.append("Bullish COT Positioning")

if market["COT_GOLD"] == "BEARISH":

    gold_score -= 15
    gold_reasons.append("Bearish COT Positioning")

# ==================================================
# GOLD MACRO FILTER
# ==================================================

macro_conflict = False

# Strong Dollar + Hawkish Fed
if market["DXY"] == 1 and market["FED"] == "HAWKISH":

    macro_conflict = True

# Strong Dollar + Rising Bonds
if market["DXY"] == 1 and market["BONDS"] == "UP":

    macro_conflict = True

# ==================================================
# FINAL SIGNALS
# ==================================================

btc_signal = get_signal(btc_score)

# GOLD
gold_signal = "🚫 NO TRADE"

if disable_gold:

    gold_signal = "🚫 GOLD DISABLED"

elif macro_conflict:

    gold_signal = "🚫 GOLD FILTER ACTIVE"

else:

    gold_signal = get_signal(gold_score)

# ==================================================
# RISK MANAGEMENT
# ==================================================

# BTC
btc_entry = market["BTC_PRICE"]
btc_sl = btc_entry - 1800
btc_tp1 = btc_entry + 3000
btc_tp2 = btc_entry + 6000

# GOLD
gold_entry = market["GOLD_PRICE"]
gold_sl = gold_entry - 18
gold_tp1 = gold_entry + 35
gold_tp2 = gold_entry + 60

# ==================================================
# OUTPUT
# ==================================================

print("\n======================================")
print(" SMART MACRO TRADING AI v5 ")
print("======================================\n")

# ======================================
# BTC OUTPUT
# ======================================

print("🟠 BTC ANALYSIS")
print("--------------------------------------")

print(f"Signal : {btc_signal}")
print(f"Score  : {btc_score}/100")
print(f"Trend  : {btc_tf}\n")

print("Reasons:")

for r in btc_reasons:
    print(f"✅ {r}")

print("\nTrade Setup:")
print(f"Entry : {btc_entry}")
print(f"SL    : {btc_sl}")
print(f"TP1   : {btc_tp1}")
print(f"TP2   : {btc_tp2}")

# ======================================
# GOLD OUTPUT
# ======================================

print("\n======================================\n")

print("🥇 GOLD ANALYSIS")
print("--------------------------------------")

print(f"Signal : {gold_signal}")
print(f"Score  : {gold_score}/100")
print(f"Trend  : {gold_tf}\n")

print("Reasons:")

for r in gold_reasons:
    print(f"✅ {r}")

print("\nTrade Setup:")
print(f"Entry : {gold_entry}")
print(f"SL    : {gold_sl}")
print(f"TP1   : {gold_tp1}")
print(f"TP2   : {gold_tp2}")

print("\n======================================\n")
