from trade import Trade
from authentication import authentication

import python_bitbankcc 

if __name__ == '__main__':
    # パスワードの認証
    password = input()
    API_KEY, API_SECRET = authentication(int(password))

    while True:
        input_num = int(input())
        t = Trade(input_num, API_KEY, API_SECRET)
        t.buy_or_sell()
