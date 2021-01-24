import time
from optibook.synchronous_client import Exchange
e = Exchange()
a = e.connect()
instrument_id = 'PHILIPS_A'
# Returns all current positions
positions = e.get_positions()
for p in positions:
    print(p, positions[p])

book = e.get_last_price_book(instrument_id)
print(book.bids[0].price)
print(book.asks)

#problem 1


positions = e.get_positions()
for p in positions:
    print(p, positions[p])

#Problem 6
print("bid | price | ask")
for i in book.asks:
    print(" | "+str(i.price)+" | "+str(i.volume))
    
for i in book.bids:
    print(str(i.volume)+" | "+str(i.price)+" | ")


def whether_to_trade():
    
    book_a = e.get_last_price_book("PHILIPS_A")
    book_b = e.get_last_price_book("PHILIPS_B") 
    
    #Philips A highest bid
    a_bid=book_a.bids[0].price
    #Philips A lowest ask
    a_ask=book_a.asks[0].price
    #Philips B highest bid
    b_bid=book_b.bids[0].price
    #Philips B lowest ask
    b_ask=book_b.asks[0].price
    
    if a_bid>b_bid:
        if a_bid-b_ask>=0:
            return True
        elif a_bid-a_ask>=0:
            return True
        else:
            return False
    else:
        if b_bid-a_ask>=0:
            return True
        elif b_bid-b_ask>=0:
            return True
        else:
            return False
            
print(whether_to_trade())

def trade():
    
    book_a = e.get_last_price_book("PHILIPS_A")
    book_b = e.get_last_price_book("PHILIPS_B") 
    
    #Philips A highest bid
    a_bid=book_a.bids[0].price
    #Philips A lowest ask
    a_ask=book_a.asks[0].price
    #Philips B highest bid
    b_bid=book_b.bids[0].price
    #Philips B lowest ask
    b_ask=book_b.asks[0].price
    
    #A bid higher than B bid
    if a_bid>b_bid:
        #A bid higher that A ask 
        if a_ask<a_bid:
            e.insert_order("PHILIPS_A", price=a_ask.price, volume=a_ask.volume, side='bid', order_type='ioc')
            
            
            
def getDifferenceInCurrentAskBidPrices(id_1, id_2):
# Buy from 1 and sell to 2
    book_1 = e.get_last_price_book(id_1)
    book_2 = e.get_last_price_book(id_2)
    
    try:
        bestAsk = book_1.asks[0].price # How much we would buy for
        bestBid = book_2.bids[0].price # How much we would sell for
    except IndexError:
        return -1
    
    #print(bestAsk)
    #print(bestBid)
    return bestBid - bestAsk

print("\n")

AB = getDifferenceInCurrentAskBidPrices('PHILIPS_A','PHILIPS_B')
BA = getDifferenceInCurrentAskBidPrices('PHILIPS_B', 'PHILIPS_A')

def printOrderBook(ingredient_id):
    book = e.get_last_price_book(ingredient_id)
    bids = {a.price: a.volume for a in book.asks}
    asks = {b.price: b.volume for b in book.bids}
    
    #print("Bids: " + str(bids))
    #print("Asks: " + str(asks))
    
    def checkIfVolumeExistsAtPrice(p, volumes):
        try:
            return volumes[p]
        except KeyError:
            return 0
            
    combinedPrices = [*bids.keys(), *asks.keys()]
    combinedPrices.sort()
    combinedPrices.reverse()
    
    printable_book = {p : [checkIfVolumeExistsAtPrice(p, bids),checkIfVolumeExistsAtPrice(p,asks)] for p in combinedPrices}
    
    formatted_book = [str(printable_book[price][1]) + "   |   " + str(price) + "   |   " + str(printable_book[price][0]) for price in printable_book]
    print("Bids | Price | Asks")
    for line in formatted_book:
        print (line)

def printOutstanding():
    outstanding = e.get_outstanding_orders("PHILIPS_A")
    for o in outstanding.values():
        print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")
    outstanding = e.get_outstanding_orders("PHILIPS_B")
    for o in outstanding.values():
        print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")

def execute_trade(i):
    
    AA = getDifferenceInCurrentAskBidPrices('PHILIPS_A','PHILIPS_A')
    AB = getDifferenceInCurrentAskBidPrices('PHILIPS_A','PHILIPS_B')
    BB = getDifferenceInCurrentAskBidPrices('PHILIPS_B','PHILIPS_B')
    BA = getDifferenceInCurrentAskBidPrices('PHILIPS_B','PHILIPS_A')
    
    #
    book_a = e.get_last_price_book("PHILIPS_A")
    book_b = e.get_last_price_book("PHILIPS_B") 
    
    #debug
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
   
        
    
    print(" |AA: " + str(round(AA, 2)) + " |AB: " + str(round(AB, 2)) + " |BA: " + str(round(BA, 2)) + " |BB: " + str(round(BB, 2)) + " |Count " + str(i))
    
    if AA > 0:
        vol = min(a_ask_vol, a_bid_vol)
        print(a_ask)
        print(a_bid)
        print(vol)
        
        
        e.insert_order("PHILIPS_A", price=a_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_A", price=a_bid, volume=vol, side='ask', order_type='ioc')
        i = i + 1
        
    if AB > 0:
        vol = min(a_ask_vol, b_bid_vol)
        print(a_ask)
        print(b_bid)
        print(vol)
        printOrderBook('PHILIPS_A')
        printOrderBook('PHILIPS_B')
        e.insert_order("PHILIPS_A", price=a_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_B", price=b_bid, volume=vol, side='ask', order_type='limit')
        time.sleep(1)
        i = i + 1
    if BA > 0 or (BA == 0 and e.get_positions()['PHILIPS_B'] < 0):
        vol = min(b_ask_vol, a_bid_vol)
        print(b_ask)
        print(a_bid)
        print(vol)
        
        e.insert_order("PHILIPS_B", price=b_ask, volume=vol, side='bid', order_type='ioc')
        e.insert_order("PHILIPS_A", price=a_bid, volume=vol, side='ask', order_type='limit')
        i = i + 1
    if BB >0:
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
while(count < 10):
    time.sleep(0.1)
    count = execute_trade(count)
    trades = e.get_trade_history('PHILIPS_A')
    for t in trades:
        print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    trades = e.get_trade_history('PHILIPS_B')
    for t in trades:
        print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    printOutstanding()

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
    
    
