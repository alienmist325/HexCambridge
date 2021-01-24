import time
from optibook.synchronous_client import Exchange
from MainFunctions import getBestBid, getBestAsk
e = Exchange()
a = e.connect()

ABids = []
AAsks = []
BBids = []
BAsks = []



for i in range(300):
    ABook = e.get_last_price_book('PHILIPS_A')
    BBook = e.get_last_price_book('PHILIPS_B')
    
    ABids.append(getBestBid(ABook))
    AAsks.append(getBestAsk(ABook))
    BBids.append(getBestBid(BBook))
    BAsks.append(getBestAsk(BBook))
    time.sleep(1)


f = open("ABids.txt", "a")
for line in ABids:
    f.write(str(line) + "\n")
f.close()

f = open("BBids.txt", "a")
for line in BBids:
    f.write(str(line) + "\n")
f.close()

f = open("AAsks.txt", "a")
for line in AAsks:
    f.write(str(line) + "\n")
f.close()

f = open("BAsks.txt", "a")
for line in BAsks:
    f.write(str(line) + "\n")
f.close()