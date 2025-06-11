import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

exchange_list = [
    "binance", "gate", "exmo", "htx", "bybit", "kucoin", "kraken", "okx",
    "whitebit", "bitget", "bitfinex", "bitmart", "poloniex", "lbank",
    "latoken", "xt", "bingx", "tokocrypto"
]

plot_dir = "benford_plots"
os.makedirs(plot_dir, exist_ok=True)

def compute_benford_scores_and_plot(exchange):
    file_name = f"{exchange}_BTC.csv"
    if not os.path.exists(file_name):
        print(f"❌ Dosya bulunamadı: {file_name}")
        return

    df = pd.read_csv(file_name)
    if "quote_value" not in df.columns:
        print(f"❌ Column 'quote_value' eksik: {file_name}")
        return

    digits = df["quote_value"].astype(str).str.replace(".", "", regex=False).str.lstrip("0").str[0]
    digits = digits[digits.isin(list("123456789"))]

    observed = digits.value_counts(normalize=True).sort_index()
    observed = observed.reindex(list("123456789")).fillna(0)

    benford = [np.log10(1 + 1 / d) for d in range(1, 10)]
    benford_arr = np.array(benford)
    observed_arr = observed.values

    score = np.sum(np.abs(observed_arr - benford_arr))
    print(f"{exchange:<12} | Benford Sapma Skoru: {score:.4f}")

    plt.figure(figsize=(8, 5))
    plt.bar(range(1, 10), observed_arr, label="Observed", alpha=0.7)
    plt.plot(range(1, 10), benford_arr, color='red', marker='o', label="Benford", linestyle='--')
    plt.xticks(range(1, 10))
    plt.xlabel("Digit")
    plt.ylabel("Frequency")
    plt.title(f"{exchange} - Benford vs Observed Distribution")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"{plot_dir}/{exchange}_benford.png")
    plt.close()

for exchange in exchange_list:
    compute_benford_scores_and_plot(exchange)