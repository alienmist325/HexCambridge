from .common_types import PriceBook


def calculate_pnl(current_valuation: float, position: int, cash_invested: float):
	return cash_invested + (current_valuation * position)


def calculate_vwap(order_book: PriceBook):
	best_bid_price = 0
	best_bid_volume = 0
	if len(order_book.bids) > 0:
		best_bid_price = order_book.bids[0].price
		best_bid_volume = order_book.bids[0].volume

	best_ask_price = 0
	best_ask_volume = 0
	if len(order_book.asks) > 0:
		best_ask_price = order_book.asks[0].price
		best_ask_volume = order_book.asks[0].volume

	return round(((best_bid_price * best_ask_volume) + (best_ask_price * best_bid_volume)) / max(1, best_bid_volume + best_ask_volume), 2)

