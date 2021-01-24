import time
from optibook.synchronous_client import Exchange
from MainFunctions import getBestAsk, getBestBid, printOrderBook

e = Exchange()
a = e.connect()

def getDifferenceInCurrentAskBidPrices(book_1, book_2):
# Buy from 1 and sell to 2
    bestAsk = getBestAsk(book_1) # How much we would buy for
    bestBid = getBestBid(book_2) # How much we would sell for
    
    #print(bestAsk)
    #print(bestBid)
    if (bestBid is not None and bestAsk is not None):
        return bestBid - bestAsk
    else:
        return -1



def printOutstanding():
    outstanding = e.get_outstanding_orders("PHILIPS_A")
    for o in outstanding.values():
        print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")
    outstanding = e.get_outstanding_orders("PHILIPS_B")
    for o in outstanding.values():
        print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")

def execute_trade(i):
    book_a = e.get_last_price_book("PHILIPS_A")
    book_b = e.get_last_price_book("PHILIPS_B") 
    AA = getDifferenceInCurrentAskBidPrices(book_a, book_a)
    AB = getDifferenceInCurrentAskBidPrices(book_a, book_b)
    BB = getDifferenceInCurrentAskBidPrices(book_b, book_b)
    BA = getDifferenceInCurrentAskBidPrices(book_b, book_a)

    try:
        #Philips A highest bid
        a_bid=book_a.bids[0].price
        a_bid_vol=book_a.bids[0].volume
    except IndexError:
        a_bid=0
        a_bid_vol=0
    try:
        #Philips A lowest ask
        a_ask=book_a.asks[0].price
        a_ask_vol=book_a.asks[0].volume
    except IndexError:
        a_ask = 0
        a_ask_vol = 0
    try:
        #Philips B highest bid
        b_bid=book_b.bids[0].price
        b_bid_vol=book_b.bids[0].volume
    except IndexError:
        b_bid = 0
        b_bid_vol=0
    try:
        #Philips B lowest ask
        b_ask=book_b.asks[0].price
        b_ask_vol=book_b.asks[0].volume
    except IndexError:
        b_ask = 0
        b_ask_vol = 0
   
        
    
    s = " |AA: " + str(round(AA, 2)) + " |AB: " + str(round(AB, 2)) + " |BA: " + str(round(BA, 2)) + " |BB: " + str(round(BB, 2)) + " |Count " + str(i)
    
    if AA > 0:
        print(s)
        vol = min(a_ask_vol, a_bid_vol)
        print(a_ask)
        print(a_bid)
        print(vol)
        
        
        
        e.insert_order("PHILIPS_A", price=a_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_A", price=a_bid, volume=vol, side='ask', order_type='ioc')
        i = i + 1
        
    if AB > 0 or (AB == 0 and e.get_positions()['PHILIPS_A']<0):
        print(s)
        vol = min(a_ask_vol, b_bid_vol)
        print(a_ask)
        print(b_bid)
        print(vol)
        #printOrderBook(book_a)
        #printOrderBook(book_b)
        e.insert_order("PHILIPS_A", price=a_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_B", price=b_bid, volume=vol, side='ask', order_type='limit')
        time.sleep(1)
        i = i + 1
    if BA > 0 or (BA == 0 and e.get_positions()['PHILIPS_B'] < 0):
        print(s)
        vol = min(b_ask_vol, a_bid_vol)
        print(b_ask)
        print(a_bid)
        print(vol)
        
        e.insert_order("PHILIPS_B", price=b_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_A", price=a_bid, volume=vol, side='ask', order_type='limit')
        time.sleep(1)
        i = i + 1
    if BB >0:
        print(s)
        vol = min(b_ask_vol, b_bid_vol)
        print(b_ask)
        print(b_bid)
        print(vol)
        
        e.insert_order("PHILIPS_B", price=b_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_B", price=b_bid, volume=vol, side='ask', order_type='ioc')
        i = i + 1
    
    printOutstanding()
    return i

        
count = 0
i = 0
while(count < 10):
    time.sleep(0.1)
    count = execute_trade(count)
    i += 1
    if (i == 100):
        trades = e.get_trade_history('PHILIPS_A')
        for t in trades:
            print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
        trades = e.get_trade_history('PHILIPS_B')
        for t in trades:
            print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
        printOutstanding()
        i = 0

outstanding = e.get_outstanding_orders("PHILIPS_A")
for o in outstanding.values():
    print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")
outstanding = e.get_outstanding_orders("PHILIPS_B")
for o in outstanding.values():
    print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")

trades = e.get_trade_history('PHILIPS_A')
for t in trades:
    print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
trades = e.get_trade_history('PHILIPS_B')
for t in trades:
    print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    
print(e.get_positions())