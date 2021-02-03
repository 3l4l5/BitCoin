import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json
# python_bitbankccのパッケージをインポート
import python_bitbankcc 

class Trade:
    def __init__(self, buy_sell, key1, key2):

        api_key = key1
        secret_key = key2

        
        # APIキー，シークレットの設定
        API_KEY = api_key
        API_SECRET = secret_key
        
        # APIの取得
        self.pub = python_bitbankcc.public()
        self.prv = python_bitbankcc.private(API_KEY, API_SECRET)
        
        # 各データの取得
        self.value = self.pub.get_ticker( 'eth_jpy' )
        self.buy = int(self.value['buy'])
        self.sell = int(self.value['sell'])
        self.buy_sell = buy_sell
        
        # 購入する値段を決定
        self.price_decition()

    def price_decition(self):
        self.buy_price = self.buy+ 3000
    
    def buy_or_sell(self, pair='eth_jpy', amount='0.0001'):
        buy_sell = 'buy' if self.buy_sell==1 else 'sell' if self.buy_sell==2 else 'None'
        value = self.prv.order(
           pair, # ペア
           self.buy_price, # 価格
           amount, # 注文枚数
           buy_sell, # 注文サイド
           'market' # 注文タイプ
        )
        print(json.dumps(value))