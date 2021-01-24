def getBestBid(book):
    try:
        return book.bids[0].price
    except IndexError:
        return None

def getBestAsk(book):
    try:
        return book.asks[0].price
    except IndexError:
        return None
        
def printOrderBook(book):
    bids = {a.price: a.volume for a in book.asks}
    asks = {b.price: b.volume for b in book.bids}
    
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
        
def printTrades(e):
    trades = e.get_trade_history('PHILIPS_A')
    for t in trades:
        print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    trades = e.get_trade_history('PHILIPS_B')
    for t in trades:
        print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
        
def printOutstanding(e):
    outstanding = e.get_outstanding_orders("PHILIPS_A")
    for o in outstanding.values():
        print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")
    outstanding = e.get_outstanding_orders("PHILIPS_B")
    for o in outstanding.values():
        print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")