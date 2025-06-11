import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

round_scores = {
    'whitebit': 3.81, 'latoken': 4.86, 'kucoin': 6.05, 'poloniex': 6.17, 'exmo': 6.28,
    'bitget': 6.39, 'xt': 8.30, 'gate': 8.41, 'bingx': 9.11, 'bitmart': 10.13,
    'htx': 10.42, 'okx': 10.50, 'binance': 11.20, 'tokocrypto': 11.96, 'lbank': 12.20,
    'bitfinex': 12.28, 'kraken': 17.59, 'bybit': 24.09
}

round_details = {
    'whitebit': (3.67, 4.13), 'latoken': (4.99, 4.55), 'kucoin': (6.26, 5.57), 'poloniex': (5.83, 6.97),
    'exmo': (6.72, 5.25), 'bitget': (6.25, 6.71), 'xt': (8.02, 8.97), 'gate': (4.39, 17.77),
    'bingx': (9.02, 9.31), 'bitmart': (11.32, 7.34), 'htx': (10.01, 11.38), 'okx': (10.25, 11.10),
    'binance': (10.79, 12.17), 'tokocrypto': (12.22, 11.36), 'lbank': (15.47, 4.58),
    'bitfinex': (12.24, 12.35), 'kraken': (18.76, 14.86), 'bybit': (25.21, 21.49)
}

benford_scores = {
    'binance': 0.2708, 'gate': 0.3117, 'exmo': 0.4046, 'htx': 0.8591, 'bybit': 0.2981,
    'kucoin': 0.2116, 'kraken': 0.2460, 'okx': 0.3025, 'whitebit': 0.2643, 'bitget': 0.1833,
    'bitfinex': 0.9433, 'bitmart': 0.3128, 'poloniex': 0.7714, 'lbank': 0.5006,
    'latoken': 0.4271, 'xt': 0.0976, 'bingx': 0.0454, 'tokocrypto': 0.9787
}

max_round = max(round_scores.values())
max_benford = max(benford_scores.values())

volume_estimates = []
for ex in round_scores:
    qv_pct, amt_pct = round_details[ex]
    round_score = (qv_pct + amt_pct) / 2
    benford_score = benford_scores[ex]

    organic_score = (round_score / max_round)
    wash_score = (1 - organic_score) * 0.5 + (benford_score / max_benford) * 0.5

    brut_volume = 100
    net_volume = brut_volume * (1 - wash_score)
    ratio = net_volume / brut_volume

    volume_estimates.append({
        "Exchange": ex.capitalize(),
        "Brut": brut_volume,
        "Net": net_volume,
        "Ratio": ratio
    })

df = pd.DataFrame(volume_estimates)
df = df.sort_values(by="Ratio", ascending=False)

print(df)

plt.figure(figsize=(12, 6))
plt.bar(df["Exchange"], df["Ratio"], color='teal')
plt.xticks(rotation=45, ha="right")
plt.title("Brüt / Net Hacim Oranı (Potansiyel Wash Trade Çıkarıldıktan Sonra)")
plt.ylabel("Net / Brüt Oranı")
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig("brut_vs_net_volume_ratio_updated.png")
plt.show() 