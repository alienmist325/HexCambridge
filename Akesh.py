from Main import e
import time
from MainFunctions import getBestAsk

# Print the Order Book nicely
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
        
print("\nPHILIPS_A")
printOrderBook('PHILIPS_A')
print("\nPHILIPS_B")
printOrderBook('PHILIPS_B')



def getDifferenceInCurrentAskBidPrices(id_1, id_2):
# Buy from 1 and sell to 2
    book_1 = e.get_last_price_book(id_1)
    book_2 = e.get_last_price_book(id_2)
    
    try:
        bestAsk = book_1.asks[0].price # How much we would buy for
        bestBid = book_2.bids[0].price # How much we would sell for
    except IndexError:
        return 0
    print(bestAsk)
    print(bestBid)
    return bestBid - bestAsk

print("\n")
AB = 0
BA = 0

#while(AB <= 0 and BA <= 0):
time.sleep(0.5)
AB = getDifferenceInCurrentAskBidPrices('PHILIPS_A','PHILIPS_B')
BA = getDifferenceInCurrentAskBidPrices('PHILIPS_B', 'PHILIPS_A')
print("A => B:" + str(round(AB,2)))
print("B => A:" + str(round(BA,2)))
    

#printOrderBook('PHILIPS_A')
#printOrderBook('PHILIPS_B')
    
#result = e.insert_order('PHILIPS_A', price=[*bids.keys()][0], volume=1, side='ask', order_type='limit')
#print(f"Order Id: {result}")    

#result = e.insert_order('PHILIPS_A', price=70, volume=1, side='bid', order_type='limit')
#print(f"Order Id: {result}")
    
#outstanding = e.get_outstanding_orders('PHILIPS_A')
#for o in outstanding.values():
#    print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")
    
#time.sleep(60)


e.insert_order("PHILIPS_A", price=getBestAsk(e.get_last_price_book('PHILIPS_A')), volume=1, side='bid', order_type='ioc')
print("trade made")
time.sleep(20)
#print(e.get_trade_history('PHILIPS_A'))
#print(e.get_trade_history('PHILIPS_B'))
#print(e.get_trade_tick_history('PHILIPS_A'))