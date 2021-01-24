#IMPORT EXCHANGE
from optibook.synchronous_client import Exchange

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

#INSTRUMENT
instrument_id = 'PHILIPS_A'

#CONNECT TO EXCHANGE
e = Exchange()
a = e.connect()


# you can also define host/user/pass yourself
# when not defined, it is taken from ~/.optibook file if it exists
# if that file does not exists, an error is thrown

#e = Exchange(host='host-to-connect-to')
#a = e.connect(username='your-username', password='your-password')

trades = e.poll_new_trades(instrument_id)
for t in trades:
    print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    
positions = e.get_positions()
for p in positions:
    print(p, positions[p])
print("\n")

book = e.get_last_price_book('PHILIPS_A')
book_b = e.get_last_price_book("PHILIPS_B") 

books = (book, book_b)

# print(book.asks)
# print(book.bids)


















