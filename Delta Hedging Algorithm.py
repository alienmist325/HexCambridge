import time
from optibook.synchronous_client import Exchange
from MainFunctions import getBestAsk, printTrades, printOutstanding

e = Exchange()
a = e.connect()
# Assume instrument A has higher liquidilty


# Work out the time lag between Philips A and Philips B
def get_lag():
    return 5
    

#execute 

lowLiq = "PHILIPS_B"
highLiq = "PHILIPS_A"




count_trades=0
while(count_trades<10):
    hLBook = e.get_last_price_book(highLiq)
    bestAsk = getBestAsk(hLBook)
    if (bestAsk is not None):
        e.insert_order(highLiq, price=bestAsk+0.1, volume=5, side='ask', order_type='limit')
        time.sleep(get_lag()-2)
        currentTradeId = e.insert_order(lowLiq, price=bestAsk, volume=5, side='bid', order_type='limit')
        print("Sell to A")
        count_trades = count_trades + 1
        #trades = e.poll_new_trades("PHILIPS_B")
        time.sleep(3)
        if(e.get_outstanding_orders("PHILIPS_B").values()):
            # While there are still outstanding orders
            e.insert_order(highLiq, price=bestAsk, volume=5, side='bid', order_type='limit')
            e.delete_order(currentTradeId, order_id = lowLiq)
        
        print("Buy from B")
    else:
        print("No best ask")
    # noSold = trades[0].volume
    

printTrades(e)