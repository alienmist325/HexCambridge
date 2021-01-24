from Main import e
import time

# Print the Order Book nicely
def printOrderBook(ingredient_id):
    book = e.get_last_price_book(ingredient_id)
    bids = {a.price: a.volume for a in book.asks}
    asks = {b.price: b.volume for b in book.bids}
    
    print("Bids: " + str(bids))
    print("Asks: " + str(asks))
    
    def checkIfVolumeExistsAtPrice(p, volumes):
        try:
            return volumes[p]
        except KeyError:
            return 0
            
    combinedPrices = [*bids.keys(), *asks.keys()]
    combinedPrices.sort()
    
    printable_book = {p : [checkIfVolumeExistsAtPrice(p, bids),checkIfVolumeExistsAtPrice(p,asks)] for p in combinedPrices}
    
    formatted_book = [str(printable_book[price][0]) + "   |   " + str(price) + "   |   " + str(printable_book[price][1]) for price in printable_book]
    print("Bids | Price | Asks")
    for line in formatted_book:
        print (line)
        
p
printOrderBook('PHILIPS_A')
print("\n PHILIPS_B")


    


    
    
#result = e.insert_order('PHILIPS_A', price=[*bids.keys()][0], volume=1, side='ask', order_type='limit')
#print(f"Order Id: {result}")    

#result = e.insert_order('PHILIPS_A', price=70, volume=1, side='bid', order_type='limit')
#print(f"Order Id: {result}")
    
#outstanding = e.get_outstanding_orders('PHILIPS_A')
#for o in outstanding.values():
#    print(f"Outstanding order: order_id({o.order_id}), instrument_id({o.instrument_id}), price({o.price}), volume({o.volume}), side({o.side})")
    
#time.sleep(60)