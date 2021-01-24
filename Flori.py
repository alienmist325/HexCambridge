#from Main import *
#IMPORT EXCHANGE
from optibook.synchronous_client import Exchange
import time

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")
import time
import pandas as pd
import os
import numpy as np

#CONNECT TO EXCHANGE
e = Exchange()
a = e.connect()
instrument_id = 'PHILIPS_A'
book = e.get_last_price_book('PHILIPS_A')
print(book.asks)
print(book.bids)


prices = dict() # empty dict

print([price_vol.price for price_vol in book.asks])
print([price_vol.price for price_vol in book.bids])

instrument_id1 = 'PHILIPS_A'
instrument_id2 = 'PHILIPS_B'
books = e.get_last_price_book(instrument_id)

def print_table(books):
    print("bid | price | ask")
    for ask in books.asks:
        print(f"    | {round(ask.price,1)} | {ask.volume}")
    for bid in books.bids:
        print(f"{bid.volume} | {round(bid.price,1)} |      ")
        
        
print_table(books)
print_table(e.get_last_price_book(instrument_id2))



import heapq

def get_highest_profit(id1,id2):
    # use heaps - max heap for bid price and min heap for ask price 
    # max heap for bid price - accross both books
    book1 = e.get_last_price_book(id1)
    book2 = e.get_last_price_book(id2)
    #bids_heap_max = heapq._heapify_max([bid.price for bid in book1.bids] + [bid2.price for bid2 in book2.bids]) 
    #asks_heap_min = heapq.heapify([ask.price for ask in book1.asks] + [ask2.price for ask2 in book2.asks]) 
    max_profit = max([bid.price for bid in book1.bids] + [bid2.price for bid2 in book2.bids]) - min([ask.price for ask in book1.asks] + [ask2.price for ask2 in book2.asks])
    if max_profit > 0:
        return max_profit
    else:
        return -1 * max_profit

profit = get_highest_profit(instrument_id1, instrument_id2)
print(profit)

print('-------------------------------------functions from New Henry - could not import--------------------------------------------')

def record_market(n):
    
    bestBidsBookA = []
    bestAsksBookB = []
    times = []
    count=0
    
    while(count<n):
        time.sleep(1)
        times.append(count)
        bestBidsBookA.append(e.get_last_price_book('PHILIPS_A').bids[0].price)
        bestAsksBookB.append(e.get_last_price_book('PHILIPS_B').asks[0].price)
        count=count+1
        #time.strftime("%H:%M:%S",time.localtime())
    dict1 = {'Time' : times, 'Best bid in A' : bestBidsBookA, 'Best ask in B' : bestAsksBookB}
    df = pd.DataFrame(dict1)
    return df

df= record_market(10)
#print(df)
print(df['Best bid in A'])
print(df['Best ask in B'])
#print(df['Best bid in A'].corr(df['Best ask in B']))


    
    


    
    
    