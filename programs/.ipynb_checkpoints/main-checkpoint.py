from trade import Trade
from authentication import authentication
from linenotify import send_message
import python_bitbankcc 
import sys

if __name__ == '__main__':
    #send_message("自動取引プログラムを始動しました")
    try:

        # パスワードの認証
        print("起動コマンドを入力")
        password = input()
        API_KEY, API_SECRET = authentication(int(password))

        print("取引を行いたい通貨ペアを入力してください")
        print("1:ETH-JPY")
        print("2:まだ入力しないで")
        pare = input()
        
        pares = {
            "1":"ETH-JPY",
            "2":"BTC-JPY",
        }

        try :
            print(pares[pare],"で取引を開始いたします")
        except:
            print("error:予期されない数字が入力されました。もう一度初めから行ってください")
            sys.exit( )


        while True:
            print("購入注文：１　売却注文：２")
            buy_or_sell = int(input())
            t = Trade(buy_or_sell, key1=API_KEY, key2=API_SECRET)
            t.buy_or_sell()








    except KeyboardInterrupt:
        print("停止しました")
        #send_message("自動取引プログラムを終了しました")