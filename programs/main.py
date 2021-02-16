from trade import Trade
from authentication import authentication
from linenotify import send_message
import python_bitbankcc
import sys
import shutil
import datetime

if __name__ == '__main__':
    buy_sum = 0
    sell_sum = 0
    terminal_size = shutil.get_terminal_size()
    columns_size = terminal_size.columns
    send_message("プログラム始動")
    try:
        print("-"*columns_size)
        # パスワードの認証
        print("起動コマンドを入力")
        password = input(">>>")
        API_KEY, API_SECRET = authentication(int(password))
        #f = open('../key/apikey.txt', 'r', encoding='UTF-8')
        #API_KEY = f.read()
        #f.close()
        #f = open('../key/secretkey.txt', 'r', encoding='UTF-8')
        #API_SECRET = f.read()
        #f.close()

        print("-"*columns_size)
        while True:
            #btc_jpy, xrp_jpy, ltc_jpy, eth_jpy, mona_jpy, bcc_jpy, xlm_jpy, qtum_jpy
            print("取引を行いたいペアを入力してください")
            print("1:eth_jpy")
            print("2:btc_jpy")
            print("3:xrp_jpy")
            print("4:ltc_jpy")
            print("5:mona_jpy")
            print("6:bcc_jpy")
            print("7:xlm_jpy")
            print("8:qtum_jpy")
            pare = input(">>>")

            pares = {
                "1":"eth_jpy",
                "2":"btc_jpy",
                "3":"xrp_jpy",
                "4":"ltc_jpy",
                "5":"mona_jpy",
                "6":"bcc_jpy",
                "7":"xlm_jpy",
                "8":"qtum_jpy",
            }
            try:
                pares[pare]
                break
            except:
                print("不正な入力です。もう一度入力してください")

        # 一回での取引枚数の設定
        print("-"*columns_size)
        print("取引ペア：",pares[pare])
        while True:
            pub = python_bitbankcc.public()
            value = pub.get_ticker(pares[pare])
            print("一回の取引での取引金額もしくは取引枚数を指定してください")
            print("例1)100円分購入したい場合：y100")
            print("例2)100枚分購入したい場合：c100")
            print("参考：ただいまの",pares[pare], "の値段は", value['last'],"円/",pares[pare][:3],"です。")

            while True:
                buffer = input(">>>")
                yen_or_not = buffer[0]
                if yen_or_not == "y" or yen_or_not == "c":
                    try:
                        yen_or_coin = float(buffer[1:])
                        amount = yen_or_coin if yen_or_not == "c" else yen_or_coin/float(value['last'])
                        break
                    except Exception as e:
                        print("例外args:", e.args)
                        print("不正な入力です。もう一度入力し直してください")
                else:
                    print("不正な入力です。もう一度入力してください!")
            break

        print("-"*columns_size)
        print("取引ペア：",pares[pare],"　取引枚数：",amount)
        while True:
            print("自動価格設定機能を使用しますか？")
            print("Yes:1, No:2")
            auto_buy_ornot = input(">>>")

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
                        diff = float(input(">>>"))
                        break
                    except:
                        print("値が不正です。正しい値を入力してください。")
                break
            else:
                print("入力が不正です。もう一度入力してください")

        print("-"*columns_size)

        print("これより取引を開始いたします。")
        while True:
            print_chr = "| pair:"+pares[pare]+" amount:"+str(amount)+(" Auto mode" if auto_buy_ornot=="1" else "Manual mode( mergin:"+str(diff)+")")+" |"
            status_len = len(print_chr)
            print("|","="*(status_len-4),"|")
            print(print_chr)
            print("|","="*(status_len-4),"|")
            print("購入注文：１　売却注文：２ 取引実績確認：0")
            buy_or_sell = int(input(">>>"))

            if buy_or_sell == 1 or buy_or_sell == 2:
                try:
                    t = Trade(
                        buy_sell=buy_or_sell,
                        auto=auto_buy_ornot,
                        diff=0,
                        pair=pares[pare],
                        key1=API_KEY,
                        key2=API_SECRET,
                        amount=amount
                        )
                    buy_buffer, sell_buffer = t.buy_or_sell()
                    buy_sum += buy_buffer
                    sell_sum += sell_buffer
                except Exception as e:
                    print(e)
            else:
                if buy_or_sell == 0:
                    print("*"*columns_size)
                    print("現在の取引実績")
                    dt_now = datetime.datetime.now()
                    print(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
                    print("購入合計：", buy_sum)
                    print("売却合計：", sell_sum)
                    print("総利益：", sell_sum - buy_sum)
                    print("*"*columns_size)
                else:
                    print("不正な入力です")
            print("-"*columns_size)

    except KeyboardInterrupt:
        print("停止しました")
        print("今回の総利益",sell_sum - buy_sum)
        send_message("今回の利益額は")
        send_message("今回の利益額は"+str(sell_sum - buy_sum)[:5]+"円でした。")
        send_message("自動取引プログラムを終了しました")
