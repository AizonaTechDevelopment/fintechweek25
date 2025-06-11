import os
import time
import numpy as np
import ccxt
from config import  exchange_list,pair_list
import csv
import pandas as pd
import matplotlib.pyplot as plt

class  data_reader():
    trades_files_dic_name="trade_files"
    fieldnames = ["timestamp", "amount", "price", "quote_value"]
    round_numbers = [10 ** i for i in range(1, 6)]

    def __init__(self):

        self.exchange_list=exchange_list
        self.pair_list=pair_list


    def read_data_from_csv(self,exchange_name,pair):
        csv_name = f"{self.trades_files_dic_name}/{exchange_name}_{pair.split('/')[0]}.csv"
        if not os.path.exists(csv_name):
            print(f"❌ Dosya bulunamadı: {csv_name}")
            return pd.DataFrame()  # Boş DataFrame döndür
        else:
            df = pd.read_csv(csv_name)

            # timestamp'ı datetime'e çevir
            df['time'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Verileri sırala
            df.sort_values('time', inplace=True)

            # print(f"✅ {exchange_name} - {pair} için {len(df)} trade yüklendi.")

            return df

    def is_round_number(self,x):
        for round_num in self.round_numbers:
            if abs(x - round_num) / round_num < 0.1:
                return True
        return False


    def make_round_number_check(self,exchange_name,pair):
        df=self.read_data_from_csv(exchange_name,pair)

        is_round=df["quote_value"].apply(self.is_round_number)
        try:
            round_num=is_round.value_counts()[True]
        except Exception as e:
            print(e)
            round_num=0

        ratio=round((round_num/len(is_round))*100,2)
        print(f"📊 ROUND NUMBER Ratio | Borsa: {exchange_name:<10} | Parite: {pair:<10} | Oran Skoru: {ratio:.4f}")

        return ratio

    def round_volume_share(self,exchange_name,pair):
        df=self.read_data_from_csv(exchange_name,pair)
        is_round=df["quote_value"].apply(self.is_round_number)
        df["is_round"]=is_round

        round_volume=df[df["is_round"]==True]["quote_value"].sum()
        total_volume=df["quote_value"].sum()
        ratio = round((round_volume / total_volume) * 100, 2)
        print(f"📊 ROUND Number Volume Ratio | Borsa: {exchange_name:<10} | Parite: {pair:<10} | Oran Skoru: {ratio:.4f}")
        return ratio






    def benford_test(self,exchange_name,pair, col="quote_value", title="Benford Testi "):
        df=self.read_data_from_csv(exchange_name,pair)
        # Sayıyı stringe çevir, . ve 0'ları at, ilk anlamlı rakamı al
        digits = df[col].astype(str).str.replace(".", "").str.lstrip("0").str[0]

        # Geçerli 1–9 rakamları filtrele
        digits = digits[digits.isin(list("123456789"))]

        # Gözlenen oranları hesapla
        observed = digits.value_counts(normalize=True).sort_index()

        # Eksik olan rakamları 0 ile doldur
        observed = observed.reindex(list("123456789")).fillna(0)

        # Benford oranları
        benford = [np.log10(1 + 1 / d) for d in range(1, 10)]

        # Grafik
        # plt.figure(figsize=(8, 5))
        # plt.bar(range(1, 10), observed.values, label="Gözlenen", alpha=0.7)
        # plt.plot(range(1, 10), benford, color='red', marker='o', label="Benford")
        # plt.xticks(range(1, 10))
        # plt.xlabel("İlk Rakam")
        # plt.ylabel("Oran")
        # plt.title(title+exchange_name)
        # plt.legend()
        # plt.grid(True)
        # plt.show()

        # Farkı döndürmek istersen:
        score = np.sum(np.abs(observed.values - np.array(benford)))
        print(f"📊 Benford Skoru | Borsa: {exchange_name:<10} | Parite: {pair:<10} | Sapma Skoru: {score:.4f}")
        return score

    def make_round_test_all(self):
        for exchange_name in self.exchange_list:
            for pair in self.pair_list:
                exchange_pair_result=self.make_round_number_check(exchange_name,pair)
                exchange_pair_result=self.round_volume_share(exchange_name,pair)


    def make_benford_test_all(self):
        for exchange_name in self.exchange_list:
            for pair in self.pair_list:
                benrford_score=self.benford_test(exchange_name,pair)


    def make_all(self):
        for exchange_name in self.exchange_list:
            for pair in self.pair_list:
                print("*"*100)
                print(exchange_name,pair)
                self.make_round_number_check(exchange_name,pair)
                self.round_volume_share(exchange_name,pair)
                self.benford_test(exchange_name,pair)
                print("*"*100)


if __name__=="__main__":
    self=data_reader()
    # self.start()a

    exchange_name="bybit"
    pair="BTC/USDT"