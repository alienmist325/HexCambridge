from Main import e
import sys, time


def init_books(book):
    # Each price has an an associated bid and ask volume
    # e.g prices = {price: [ask, bid]}
    parsed_book = {price_vol.price:[price_vol.volume,0] for price_vol in book.asks}
    
    for bid_vol in book.bids:
        if bid_vol.price in parsed_book:
            parsed_book[bid_vol.price][1] = bid_vol.volume
        else:
            parsed_book[bid_vol.price] = [0, bid_vol.volume]
            
    return parsed_book


def find_profit(parsed_books):
    # (book, bid)
    BEST_BID = 0
    BEST_ASK = sys.maxsize
    
    # Get highest price with a bid (willing)
    for i,book in enumerate(parsed_books):
        best_bid = max([price for price in book if book[price][1]])
        #print("Highest bid ({}): {}".format(i, best_bid))
        BEST_BID = max(BEST_BID, best_bid)
        
    
    # Get lowest ask price
    for i,book in enumerate(parsed_books):
        best_ask = min([price for price in book if book[price][0]])
        #print("Lowest ask ({}): {}".format(i, best_ask))
        BEST_ASK = min(BEST_ASK, best_ask)
    
    # def print_book(book):
    #     print("\nBid      Price     Ask")
    #     for price, value in book.items():
    #         ask, bid = value
    #         print("{:.2f}   | {:.2f}   | {:.2f}".format(bid, price, ask))
    
    # for book in parsed_books:
    #     print_book(book)
    #     print("\n")
    
    return BEST_BID - BEST_ASK


def continual_check():
    book_a = e.get_last_price_book('PHILIPS_A')
    book_b = e.get_last_price_book("PHILIPS_B") 
    books = (book_a, book_b)
    
    # Initialise books
    parsed_books = [init_books(book) for book in books]
    return find_profit(parsed_books)
    

for _ in range(100):
    try:
        change = continual_check()
        print(change)
        if change > 0:
            print("BID!")
    except Exception:
        pass
    time.sleep(0.1)