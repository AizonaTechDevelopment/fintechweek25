import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

exchange_list = [
    "binance", "gate", "exmo", "htx", "bybit", "kucoin", "kraken", "okx",
    "whitebit", "bitget", "bitfinex", "bitmart", "poloniex", "lbank",
    "latoken", "xt", "bingx", "tokocrypto"
]

round_numbers = [10 ** i for i in range(-4, 6)]
tolerance = 0.1

def is_round(x):
    for r in round_numbers:
        if abs(x - r) / r < tolerance:
            return True
    return False

plot_dir = "round_plots"
os.makedirs(plot_dir, exist_ok=True)

w_quote = 0.7
w_amount = 0.3

score_list = []

for exchange in exchange_list:
    file = f"{exchange}_BTC.csv"
    if not os.path.exists(file):
        print(f"❌ {file} eksik")
        continue

    df = pd.read_csv(file)
    if not {"amount", "quote_value"}.issubset(df.columns):
        print(f"❌ Gerekli kolonlar eksik: {exchange}")
        continue

    df = df.dropna(subset=["amount", "quote_value"])

    df["is_round_qv"] = df["quote_value"].apply(is_round)
    df["is_round_amt"] = df["amount"].apply(is_round)

    qv_round_ratio = (
        df[df["is_round_qv"]]["quote_value"].sum() / df["quote_value"].sum()
    ) * 100
    amt_round_ratio = (
        df[df["is_round_amt"]]["quote_value"].sum() / df["quote_value"].sum()
    ) * 100

    combined_score = round(w_quote * qv_round_ratio + w_amount * amt_round_ratio, 2)

    score_list.append((exchange, combined_score, qv_round_ratio, amt_round_ratio))

    plt.figure(figsize=(6, 4))
    plt.bar(["Quote Value", "Amount"], [qv_round_ratio, amt_round_ratio], color=["blue", "gray"])
    plt.title(f"{exchange} - Weighted Round Score: {combined_score:.2f}")
    plt.ylabel("Volume Share (%)")
    plt.tight_layout()
    plt.savefig(f"{plot_dir}/{exchange}_round_combined.png")
    plt.close()

score_list.sort(key=lambda x: x[1])

print("\n📊 Combined Round Number Score (Sorted):\n")
print(f"{'Rank':<5} {'Exchange':<12} {'Score':<7} {'QV%':<7} {'Amt%'}")
for i, (ex, score, qv, amt) in enumerate(score_list, 1):
    print(f"{i:<5} {ex:<12} {score:<7.2f} {qv:<7.2f} {amt:.2f}")