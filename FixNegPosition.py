from optibook.synchronous_client import Exchange
from MainFunctions import getBestAsk
import time

e = Exchange()
a = e.connect()


instr_ids = ['PHILIPS_A', 'PHILIPS_B']
index = int(input()) # 0 or 1
instr = instr_ids[index] 
book = e.get_last_price_book(instr)

positions = e.get_positions().values()
totalPosition = sum(positions)


if (book.asks[0].volume >= abs(totalPosition)):
    print("Estimated cash by end")
    cash = e.get_cash()
    bestAsk = getBestAsk(book)
    loss = bestAsk * abs(totalPosition)
    print(cash - loss)
    print("Proceed?")
    if (input() == "y"):
        e.insert_order(instr, price=bestAsk, volume=abs(totalPosition), side='bid', order_type='ioc')
        time.sleep(5)