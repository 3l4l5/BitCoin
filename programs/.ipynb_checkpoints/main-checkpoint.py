from trade import Trade

if __name__ == '__main__':
    while True:
        input_num = int(input())
        t = Trade(input_num)
        t.buy_or_sell()
