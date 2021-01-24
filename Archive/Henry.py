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
            
            
            
    
    
