from Main import e
import numpy as np
import time 

marketData = []

# Record the volume of the trades being made on the market within 9 minutes
def record_volume(instrument_id):
    last_book = e.get_last_price_book(instrument_id)
    bidVolumes = [bid.volume for bid in last_book.bids]
    askVolumes = [ask.volume for ask in last_book.asks]
        
    return sum(askVolumes) + sum(bidVolumes)

    
# Compare and return the instrument that has the higher liquidity
def get_higher_liquid(instrument_id_1,instrument_id_2):
    if record_volume(instrument_id_1)>record_volume(instrument_id_2):
        return instrument_id_1
    else:
        return instrument_id_2
        
# Compare and return the instrument that has the lower liquidity
def get_lower_liquid(instrument_id_1,instrument_id_2):
    if record_volume(instrument_id_1)<record_volume(instrument_id_2):
        return instrument_id_1
    else:
        return instrument_id_2
      

# record the best bid with its corresponding time within 3 minutes
def updateMarketData(instrument_id):
    try:
        marketData.append(e.get_last_price_book(instrument_id).bids[0].price)
    except Exception:
        pass
        #print(_, e.get_last_price_book(instrument_id).bids[0].price)
        #time.strftime("%H:%M:%S",time.localtime())
    
    

def init_record_market(instrument_id):
    print("Doing initial data collection. Please wait 3 minutes")
    bestBids = []
    RECORD_TIME = 180
    
    for _ in range(RECORD_TIME):
        time.sleep(1)
        try:
            bestBids.append(e.get_last_price_book(instrument_id).bids[0].price)
        except Exception:
            pass
    marketData = bestBids
        
# Polynomial regression
def predict_price(instrument_id, predictions=1, degree=3):
    y = marketData
    x = np.arange(0, len(y))
    
    poly_est = np.polyfit(x, np.array(y), degree)
    poly = np.poly1d(poly_est)
    
    return [poly(future) for future in range(predictions)]
    


    
# Place a limit order
def delta_neutral(low_liquid_id,high_liquid_id, currentTradeId):
    
    #put limit order on instrument of low liquidity
    e.delete_order(lowLiq, order_id=currentTradeId)
    currentTradeId = e.insert_order(lowLiq, price=predict_price(highLiq)[0]+0.0000003, volume=20, side='ask', order_type='limit')

# Place a IOC order
def place_ioc(low_liquid_id,high_liquid_id, vol):
    #put a market order on the instrument of high liquidity
    e.insert_order(low_liquid_id, price=predict_price(high_liquid_id)[0], volume=vol, side='bid', order_type='ioc')
    

lowLiq = get_lower_liquid("PHILIPS_A","PHILIPS_B")
highLiq = get_higher_liquid("PHILIPS_A","PHILIPS_B")
init_record_market(highLiq)    
print("c")
currentTradeId = e.insert_order(lowLiq, price=predict_price(highLiq)[0]+0.0000003, volume=20, side='ask', order_type='limit')
print("b")

for i in range (0,100):
    print("a")
    # Assuming <= 20 sold
    #noSold = [order.volume for order in e.get_outstanding_orders(lowLiq).values() if order.order_id == currentTradeId][0]
    trades = e.poll_new_trades(lowLiq)
    noSold = trades[0].volume
    if (noSold != 0):
        place_ioc(lowLiq,highLiq,noSold)
    delta_neutral(lowLiq, highLiq, currentTradeId)
    # Collect and cull the marketData object
    updateMarketData(highLiq)
    time.sleep(1)

