from trade import Trade
from authentication import authentication
from linenotify import send_message
import python_bitbankcc
import sys
import shutil

if __name__ == '__main__':
    terminal_size = shutil.get_terminal_size()
    columns_size = terminal_size.columns
    #send_message("自動取引プログラムを始動しました")
    try:
        print("-"*columns_size)
        # パスワードの認証
        print("起動コマンドを入力")
        password = input()
        #API_KEY, API_SECRET = authentication(int(password))
        API_KEY = "d4861a86-102e-45ab-8565-b5c0568c6228"
        API_SECRET = "35329df1d68f25f93e8ef6a44a691dd31115535873d5ca27c87e279f29ed5dd9"
        print("-"*columns_size)
        while True:
            print("取引を行いたい通貨ペアを入力してください")
            print("1:ETH-JPY")
            print("2:BTC-JPY")
            pare = input()

            pares = {
                "1":"eth_jpy",
                "2":"btc_jpy",
            }
            try:
                pares[pare]
                break
            except:
                print("不正な入力です。もう一度入力してください")

        # 一回での取引枚数の設定
        print("-"*columns_size)
        while True:
            pub = python_bitbankcc.public()
            value = pub.get_ticker(pares[pare])

            print("一回での取引枚数を設定してください")
            print("参考：ただいまの",pares[pare], "の値段は", value['last'],"円/",pares[pare][:3],"です。")

            try:
                amount = float(input())
                break
            except:
                print("不正な入力です。もう一度入力してください")

        print("-"*columns_size)
        while True:
            print("自動価格設定機能を使用しますか？")
            print("Yes:1, No:2")
            auto_buy_ornot = input()

            # 自動価格設定機能を使用する場合の処理
            if auto_buy_ornot=="1":
                print("自動価格設定機能を使用します")
                diff = ""
                break

            # 自動価格設定機能をしない場合の処理
            if auto_buy_ornot=="2":
                print("自動価格設定機能は使用しません")

                # 購入および売却するときに使用する差分の値を入力してもらう処理
                while True:
                    print("購入時にとる現在の値との差分を入力してください")
                    try:
                        diff = float(input())
                        break
                    except:
                        print("値が不正です。正しい値を入力してください。")
                break
            else:
                print("入力が不正です。もう一度入力してください")

        print("-"*columns_size)
        print("これより取引を開始いたします。")
        print("ペア:", pares[pare])
        print("取引量:", amount)
        print("自動価格設定" if auto_buy_ornot=="1" else "手動価格設定値：", diff)

        while True:
            print("購入注文：１　売却注文：２")
            buy_or_sell = int(input())

            if buy_or_sell == 1 or buy_or_sell == 2:
                t = Trade(
                    buy_sell=buy_or_sell,
                    auto=auto_buy_ornot,
                    diff=0,
                    pair=pares[pare],
                    key1=API_KEY,
                    key2=API_SECRET,
                    amount=amount
                    )
                t.buy_or_sell()
            else:
                print("不正な入力です")
            print("-"*columns_size)

    except KeyboardInterrupt:
        print("停止しました")
        #send_message("自動取引プログラムを終了しました")