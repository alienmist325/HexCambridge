from optibook.synchronous_client import Exchange
from MainFunctions import getBestBid
import time

e = Exchange()
a = e.connect()


instr_ids = ['PHILIPS_A', 'PHILIPS_B']
index = int(input()) # 0 or 1
instr = instr_ids[index] 
book = e.get_last_price_book(instr)

positions = e.get_positions().values()
totalPosition = sum(positions)


if (book.bids[0].volume >= abs(totalPosition)):
    print("Estimated cash by end")
    cash = e.get_cash()
    bestBid = getBestBid(book)
    gain = bestBid * abs(totalPosition)
    print(cash + gain)
    print("Proceed?")
    if (input() == "y"):
        e.insert_order(instr, price=bestBid, volume=abs(totalPosition), side='ask', order_type='ioc')
        time.sleep(5)