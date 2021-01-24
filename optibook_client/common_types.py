from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import copy
import json


class SingleSidedBooking:
    def __init__(self):
        self.username: str = ''
        self.instrument_id: str = ''
        self.price: float = 0.0
        self.volume: int = 0
        self.action: str = ''


class TradeTick:
    """
    A public trade.

    A public trade is a trade between any two parties,
    i.e. a trade in which you might not have been involved.

    Attributes
    ----------
    timestamp: datetime.datetime
        The time of the trade.

    instrument_id: str
        The id of the traded instrument.

    price: float
        The price at which the instrument traded.

    volume: int
        The volume that was traded.

    aggressor_side: 'bid' or 'ask'
        The side of the aggressive party.
        If 'bid' then the initiator (aggressor) of the trade bought.
        If 'ask' then the initiator (aggressor) of the trade sold.

    buyer: str
        Name of buyer.

    seller: str
        Name of seller.

    trade_nr: int
        Id of the trade
    """
    def __init__(self, *, timestamp=None, instrument_id=None, price=None, volume=None, aggressor_side=None, buyer=None, seller=None, trade_nr=None):
        self.timestamp: datetime = datetime(1970, 1, 1) if not timestamp else timestamp
        self.instrument_id: str = '' if not instrument_id else instrument_id
        self.price: float = 0.0 if not price else price
        self.volume: int = 0 if not volume else volume
        self.aggressor_side: str = '' if not aggressor_side else aggressor_side
        self.buyer: str = '' if not buyer else buyer
        self.seller: str = '' if not seller else seller
        self.trade_nr: int = -1 if not trade_nr else trade_nr


class PriceVolume:
    """
    Bundles a price and a volume

    Attributes
    ----------
    price: float

    volume: int
    """
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"[price_volume] price={str(self.price)}, volume={str(self.volume)}"

    def __eq__(self, other):
        if not isinstance(other, PriceVolume):
            return NotImplemented
        return self.price == other.price and self.volume == other.volume


class PriceBook:
    """
    An order book at a specific point in time.

    Attributes
    ----------
    timestamp: datetime.datetime
        The time of the snapshot.

    instrument_id: str
        The id of the instrument the book is on.

    bids: List[PriceVolume]
        List of price points and volumes representing all bid orders.
        Sorted from highest price to lowest price (i.e. from best to worst).

    asks: List[PriceVolume]
        List of price points and volumes representing all ask orders.
        Sorted from lowest price to highest price (i.e. from best to worst).
    """
    def __init__(self, *, timestamp=None, instrument_id=None, bids=None, asks=None):
        self.timestamp: datetime = datetime(1970, 1, 1) if not timestamp else timestamp
        self.instrument_id: str = '' if not instrument_id else instrument_id
        self.bids: List[PriceVolume] = [] if not bids else bids
        self.asks: List[PriceVolume] = [] if not asks else asks

    def __eq__(self, other):
        if not isinstance(other, PriceBook):
            return NotImplemented
        return self.instrument_id == other.instrument_id and self.bids == other.bids and self.asks == other.asks


class Trade:
    """
    A private trade.

    A private trade is a trade in which you were involved,
    i.e. a trade in which you were either a buyer or a seller.

    Attributes
    ----------
    order_id: int
        The id of the order that traded.

    instrument_id: str
        The id of the traded instrument.

    price: float
        The price at which the instrument traded.

    volume: int
        The volume that was traded.

    side: 'bid' or 'ask'
        If 'bid' you bought.
        If 'ask' you sold.
    """
    def __init__(self):
        self.order_id: int = 0
        self.instrument_id: str = ''
        self.price: float = 0.0
        self.volume: int = 0
        self.side: str = ''


class OrderStatus:
    """
    Summary of an order.

    Attributes
    ----------
    order_id: int
        The id of the order.

    instrument_id: str
        The id of the traded instrument.

    price: float
        The price at which the instrument traded.

    volume: int
        The volume that was traded.

    side: 'bid' or 'ask'
        If 'bid' this is a bid order.
        If 'ask' this is an ask order.
    """
    def __init__(self):
        self.order_id: int = 0
        self.instrument_id: str = ''
        self.price: float = 0.0
        self.volume: int = 0
        self.side: str = ''


class InstrumentType(Enum):
    SPOT = 1
    OPTION = 2


class OptionKind(Enum):
    PUT = 1
    CALL = 2


class Instrument:
    @staticmethod
    def from_dict(dict_data: Dict) -> "Instrument":
        instrument = Instrument(None, None, None)
        for k, v in dict_data.items():
            setattr(instrument, k, v)

        if instrument.instrument_type:
            instrument.instrument_type = InstrumentType[instrument.instrument_type]
        if instrument.expiry:
            instrument.expiry = datetime.strptime(instrument.expiry, '%Y-%m-%d %H:%M:%S')
        if instrument.option_kind:
            instrument.option_kind = OptionKind[instrument.option_kind]

        return instrument

    @staticmethod
    def from_json(json_data: str) -> "Instrument":
        return Instrument.from_dict(json.loads(json_data))

    @staticmethod
    def to_json(instrument) -> str:
        instr_copy = copy.deepcopy(instrument)

        if instr_copy.instrument_type:
            instr_copy.instrument_type = instr_copy.instrument_type.name
        if instr_copy.expiry:
            instr_copy.expiry = datetime.strftime(instr_copy.expiry, '%Y-%m-%d %H:%M:%S')
        if instr_copy.option_kind:
            instr_copy.option_kind = instr_copy.option_kind.name

        return json.dumps(instr_copy.__dict__)

    def __init__(self,
                 instrument_id: str,
                 tick_size: float,
                 instrument_type: Optional[InstrumentType] = None,
                 base_instrument_id: Optional[str] = None,
                 expiry: Optional[datetime] = None,
                 option_kind: Optional[OptionKind] = None,
                 strike: Optional[float] = None):
        self.instrument_id: str = instrument_id
        self.tick_size: float = tick_size
        self.instrument_type: Optional[InstrumentType] = instrument_type

        # option definition
        self.base_instrument_id: Optional[str] = base_instrument_id
        self.expiry: Optional[datetime] = expiry
        self.option_kind: Optional[OptionKind] = option_kind
        self.strike: Optional[float] = strike

        # miscellaneous
        self.paused: bool = False
