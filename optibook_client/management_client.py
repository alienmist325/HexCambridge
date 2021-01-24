# Copyright (c) Optiver I.P. B.V. 2019

import logging
from datetime import datetime
from typing import Dict, Any, Optional
import itertools
from collections import defaultdict, deque
from .base_client import Client
from .common_types import TradeTick, Instrument, InstrumentType, OptionKind
from .type_checking import validate_instrument

from .idl import management_capnp, common_capnp, info_capnp
from .base_client import _default_settings

logger = logging.getLogger('client')

ACTION_BUY = 'buy'
ACTION_SELL = 'sell'
ALL_ACTIONS = [ACTION_BUY, ACTION_SELL]


class ManagementClient(Client):
    def __init__(self, host=None, port=None, max_nr_trade_history=100, admin_info_connection=None):
        if not host:
            host = _default_settings['host']
        if not port:
            port = _default_settings['management_port']

        super().__init__(host=host, port=port)
        self._max_trade_history = max_nr_trade_history
        self._admin_info = admin_info_connection

    def reset_data(self):
        super(ManagementClient, self).reset_data()
        self._mgmt = None

        self._trade_history_last_polled_index = defaultdict(lambda: 0)
        self._trade_history = defaultdict(deque)
        self._instruments = set()

        self._user_positions: Dict[str: Any] = {}
        self._blacklisted_users = set()
        self._connected_users = set()

    async def _on_connected(self):
        self._mgmt_portal = self._client.bootstrap().cast_as(management_capnp.ManagementPortal)

    def _create_initial_user_position(self, username):
        self._user_positions[username] = {iid: {'trade_id': 0, 'cash': 0.0, 'volume': 0} for iid in self._instruments}

    def _add_user_cash_position(self, username, cash_difference):
        if username not in self._user_positions:
            self._create_initial_user_position(username)
        self._user_positions[username]['cash'] += cash_difference

    def _add_user_instrument_position(self, trade_id, username, instrument_id, position_difference, cash_difference):
        if username not in self._user_positions:
            self._create_initial_user_position(username)
        if instrument_id not in self._user_positions[username]:
            self._user_positions[username][instrument_id] = { 'trade_id' : 0, 'cash' : 0.0, 'volume' : 0 }
        if trade_id > self._user_positions[username][instrument_id]['trade_id']:
            self._user_positions[username][instrument_id]['volume'] += position_difference
            self._user_positions[username][instrument_id]['cash'] += cash_difference

    def _on_info_message(self, msg):
        if msg.type == common_capnp.TradeTick.schema.node.id:
            trade = msg.msg.as_struct(common_capnp.TradeTick.schema)
            if not trade.buyer or not trade.seller:
                raise Exception("No buyer or seller field present on TradeTick. Most likely not an admin info-feed is used")

            logger.debug('trade mgmt start %s', trade)

            t = TradeTick()
            t.instrument_id = trade.instrumentId
            t.volume = trade.volume
            t.price = trade.price
            t.aggressor_side = str(trade.aggressorSide)
            t.timestamp = datetime.fromtimestamp(trade.timestamp // 1000000000)
            t.buyer = trade.buyer
            t.seller = trade.seller
            t.trade_nr = trade.tradeId

            inst_hist = self._trade_history[t.instrument_id]
            inst_hist.append(t)
            while len(inst_hist) > self._max_trade_history:
                inst_hist.popleft()
                self._trade_history_last_polled_index[t.instrument_id] = max(
                    self._trade_history_last_polled_index[t.instrument_id] - 1, 0)

            total_traded_price = trade.price * trade.volume
            instrument_id = trade.instrumentId
            buyer = trade.buyer
            seller = trade.seller

            self._add_user_instrument_position(trade.tradeId, buyer, instrument_id, trade.volume, -total_traded_price)
            self._add_user_instrument_position(trade.tradeId, seller, instrument_id, -trade.volume,
                                                     total_traded_price)
        elif msg.type == info_capnp.InstrumentCreated.schema.node.id:
            inst = msg.msg.as_struct(info_capnp.InstrumentCreated.schema)
            for user in self._user_positions:
                self._user_positions[user][inst.instrumentId] = { 'trade_id' : 0, 'cash' : 0.0, 'volume' : 0 }
            self._instruments.add(inst.instrumentId)

    async def authenticate(self, username, password):
        if self._admin_info is not None:
            self._info_handle = self._admin_info.add_message_callback(self._on_info_message)
            self._instruments = set(self._admin_info.get_instruments())

        result = await self._mgmt_portal.login(username, password, self.ManagementSubscription(self)).a_wait()

        self._mgmt = result.management

        self._user_positions = { r.username :
                                     { inst.instrumentId :
                                          { 'trade_id': r.positions.basedOnTradeId, 'cash' : inst.cash, 'volume' : inst.position } for inst in r.positions.positions
                                      } for r in result.positions
                                 }

    async def blacklist(self, username, reason, try_close_positions):
        return (await self._mgmt.blacklist(username, reason, try_close_positions).a_wait()).success

    async def whitelist(self, username):
        return (await self._mgmt.whitelist(username).a_wait()).success

    async def create_instrument(self, instrument: Instrument):
        validate_instrument(instrument)
        await self._mgmt.createInstrument(instrument.instrument_id, instrument.tick_size, Instrument.to_json(instrument)).a_wait()

    async def expire_instrument(self, instrument_id, expiration_value):
        await self._mgmt.expireInstrument(instrument_id, expiration_value).a_wait()

    async def pause_instrument(self, instrument_id):
        await self._mgmt.pauseInstrument(instrument_id).a_wait()

    async def resume_instrument(self, instrument_id):
        await self._mgmt.resumeInstrument(instrument_id).a_wait()

    async def single_sided_booking(self, *, username, instrument_id, price, volume, action):
        assert action in ALL_ACTIONS, f'action must be one of {ALL_ACTIONS}'
        req = self._mgmt.singleSidedBooking_request()
        req.ssb.username = username
        req.ssb.instrumentId = instrument_id
        req.ssb.price = price
        req.ssb.volume = volume
        req.ssb.action = action
        await req.send().a_wait()

    def get_trade_history(self, instrument_id):
        if not self._admin_info:
            raise Exception("Cannot fetch trades from management client that has been instantiated without a management info connection")
        return list(self._trade_history[instrument_id])

    def poll_new_trades(self, instrument_id):
        if not self._admin_info:
            raise Exception("Cannot fetch trades from management client that has been instantiated without a management info connection")
        new_trades = list(
            itertools.islice(self._trade_history[instrument_id], self._trade_history_last_polled_index[instrument_id],
                             len(self._trade_history[instrument_id])))
        self._trade_history_last_polled_index[instrument_id] = len(self._trade_history[instrument_id])
        return new_trades

    def clear_trade_history(self):
        self._trade_history_last_polled_index = defaultdict(lambda: 0)
        self._trade_history = defaultdict(deque)

    def get_user_positions(self, username):
        if not self._admin_info:
            raise Exception("Cannot fetch positions from management client that has been instantiated without a management info connection")
        return self._user_positions[username]

    def get_usernames(self):
        return list(self._user_positions.keys())

    def get_connected_users(self):
        return self._connected_users

    def get_blacklisted_users(self):
        return self._blacklisted_users

    class ManagementSubscription(management_capnp.ManagementPortal.ManagementFeed.Server):
        def __init__(self, management_client):
            self._mgmt = management_client

        def onSingleSidedBooking(self, ssb, **kwargs):
            logger.debug('ssb start %s', ssb)
            username = ssb.username
            action = ssb.action

            if action == ACTION_BUY:
                self._mgmt._add_user_instrument_position(ssb.tradeId, username, ssb.instrumentId,
                                                   ssb.volume,
                                                   -ssb.volume * ssb.price)
            elif action == ACTION_SELL:
                self._mgmt._add_user_instrument_position(ssb.tradeId, username, ssb.instrumentId,
                                                   -ssb.volume,
                                                   ssb.volume * ssb.price)
            else:
                raise Exception(
                    f"Got single sided booking with unknown action {action}. Message: '{str(ssb)}'")
            logger.debug('ssb end %s', ssb)

        def onBlacklisting(self, username, reason, triedClosingPositions, **kwargs):
            self._mgmt._blacklisted_users.add(username)

        def onWhitelisting(self, username, **kwargs):
            self._mgmt._blacklisted_users.remove(username)

        def onUserConnected(self, username, **kwargs):
            if username not in self._mgmt._user_positions:
                self._mgmt._create_initial_user_position(username)
            self._mgmt._connected_users.add(username)

        def onUserDisconnected(self, username, **kwargs):
            self._mgmt._connected_users.remove(username)

        def ping(self, **kwargs):
            pass
