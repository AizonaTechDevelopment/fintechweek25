import os
import time
import ccxt
from config import  exchange_list,pair_list
import csv


class  data_saver_local():
    trades_files_dic_name="trade_files"
    fieldnames = ["timestamp", "amount", "price", "quote_value"]

    def __init__(self):

        self.exchange_list=exchange_list
        self.pair_list=pair_list
        self.last_update_trade_time={v:{ p :time.time()*1000 for p in self.pair_list} for v in self.exchange_list}



    def create_csv_files(self):

        if self.trades_files_dic_name not in os.listdir():
            os.mkdir(self.trades_files_dic_name)

        for exchange_name in self.exchange_list:
            for pair in self.pair_list:
                print(exchange_name,pair)
                csv_name=f"{self.trades_files_dic_name}/{exchange_name}_{pair.split('/')[0]}.csv"

                if not os.path.isfile(csv_name):
                    print("📁 CSV dosyası bulunamadı, oluşturuluyor...")
                    with open(csv_name, mode='w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                        writer.writeheader()
                else:
                    print("📂 Var olan CSV dosyasına ekleme yapılacak.")


    def build_rest_objects(self):
        self.exchange_rest_dict={}
        for exchange_name in self.exchange_list:
            if exchange_name not in ccxt.exchanges:
                print(f"❌ {exchange_name} desteklenmeyen borsa!")
                continue
            exchange_class = getattr(ccxt, exchange_name)
            self.exchange_rest_dict[exchange_name] = exchange_class()
            # self.exchange_rest_dict[exchange_name].load_markets()
            print(f"✅ {exchange_name} REST objesi oluşturuldu.")

    def get_data(self,exchange_name,pair):
        csv_name = f"{self.trades_files_dic_name}/{exchange_name}_{pair.split('/')[0]}.csv"
        trades = self.exchange_rest_dict[exchange_name].fetch_trades(pair,since=int(self.last_update_trade_time[exchange_name][pair]), limit=1000)



        if len(trades)>0:
            self.last_update_trade_time[exchange_name][pair] = max([t["timestamp"] for t in trades])
            print(exchange_name,pair,len(trades))
            for trade in trades:
                # print(trade)
                data_save={"amount":trade["amount"],"price":trade["price"],"quote_value":round(trade["price"]*trade["amount"],2),"timestamp":trade["timestamp"]}
                with open(csv_name, mode='a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    writer.writerow(data_save)
        else:
            print("no trades in ",exchange_name," for ",pair)


    def collect_data(self):
        for exchange_name in self.exchange_list:
            for pair in self.pair_list:
                try:
                    self.get_data(exchange_name,pair)
                except Exception as e:
                    print(e,exchange_name,pair)




    def run(self):

        self.build_rest_objects()
        self.create_csv_files()


        while True:
            self.collect_data()
            time.sleep(15)


if __name__=="__main__":
    self=data_saver_local()
    # self.run()

    exchange_name="bybit"
    pair="BTC/USDT"