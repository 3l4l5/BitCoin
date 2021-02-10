import numpy as np
import pandas as pd
import os, json
# python_bitbankccのパッケージをインポート
import python_bitbankcc

class Trade:
    def __init__(self, buy_sell ,auto, diff, pair, key1, key2, amount):
        api_key = key1
        secret_key = key2

        self.amount = amount
        # APIキー，シークレットの設定
        API_KEY = api_key
        API_SECRET = secret_key

        # APIの取得
        self.pub = python_bitbankcc.public()
        self.prv = python_bitbankcc.private(API_KEY, API_SECRET)

        # 各データの取得
        self.pair = pair
        self.buy_sell = buy_sell
        self.diff = diff
        self.auto = True if auto == 1 else False if auto == 2 else "Error"

    # 購入する値段を決定する関数
    def price_decition_auto(self):
        # asks -> 売り板　基本的に高い値で買いたいので約定することを目的とすると最小値で指定する
        # bids -> 買い板 基本的に安い値で買いたいので約定することを目的とすると最大値で指定する
        depth = self.pub.get_depth(self.pair)
        asks = depth["asks"]
        bids = depth["bids"]
        buy_price = np.array(bids).T[0][0]
        sell_price = np.array(asks).T[0][0]

        return {"buy":buy_price, "sell":sell_price}

    # 手動で値を設定する
    def price_decition_manual(self):

        # 今取引されている値を読み取る
        value = self.pub.get_ticker(self.pair)
        buy = int(value['buy'])
        sell = int(value['sell'])

        # 値を決定する
        buy_price = buy + self.diff
        sell_price = sell - self.diff

        return {"buy":buy_price, "sell":sell_price}

    # 実際に取引を行う関数
    def buy_or_sell(self):
        # self.buy_sellにどちらの数字が入っているか確認する。
        buy_sell = 'buy' if self.buy_sell==1 else 'sell' if self.buy_sell==2 else 'None'
        # 自動もしくは手動で取引金額を設定する
        price = self.price_decition_auto() if self.auto else self.price_decition_manual()
        # とりひきペアを設定
        pair = self.pair


        value = self.prv.order(
            pair, # ペア
            price[buy_sell], # 価格
            self.amount, # 注文枚数
            buy_sell, # 注文サイド
            'market' # 注文タイプ
        )
        print("order id:",value["order_id"])
        print("pair:", value["pair"])
        print("side:",value["side"])
        print("購入量:",value["start_amount"])
        print("購入時刻:", (value["ordered_at"]))

