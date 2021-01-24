import logging
import time
from typing import Optional
from datetime import datetime

from .common_types import InstrumentType, OptionKind, Instrument
from .management_client import ManagementClient
from .exchange_client import InfoClient
from . import management_client
from .synchronous_wrapper import SynchronousWrapper

logger = logging.getLogger('client')

DEFAULT_MGMT_PORT = 9001
DEFAULT_INFO_PORT = 7001


class Management:
    def __init__(self,
                 admin_info_password,
                 host: str = None,
                 mgmt_port: int = DEFAULT_MGMT_PORT,
                 info_port: int = DEFAULT_INFO_PORT,
                 full_message_logging: bool = False,
                 max_nr_trade_history: int = 100):
        if full_message_logging:
            management_client.logger.setLevel('VERBOSE')

        self._i = InfoClient(host=host,
                             port=info_port,
                             max_nr_trade_history=max_nr_trade_history,
                             admin_password=admin_info_password)

        self._m = ManagementClient(host=host,
                                   port=mgmt_port,
                                   max_nr_trade_history=max_nr_trade_history,
                                   admin_info_connection=self._i)

        self._wrapper = SynchronousWrapper([self._m, self._i])

    def is_connected(self) -> bool:
        return self._wrapper.is_connected()

    def connect(self, username, password) -> None:
        self._wrapper.connect()

        return self._wrapper.run_on_loop(
            self._m.authenticate(username, password)
        )

    def disconnect(self) -> None:
        self._wrapper.disconnect()

    def blacklist(self, username, reason, try_close_positions) -> bool:
        assert self.is_connected(), "Cannot call function until connected. Call connect() first"

        return self._wrapper.run_on_loop(
            self._m.blacklist(username=username, reason=reason, try_close_positions=try_close_positions)
        )

    def whitelist(self, username) -> bool:
        assert self.is_connected(), "Cannot call function until connected. Call connect() first"

        return self._wrapper.run_on_loop(
            self._m.whitelist(username=username)
        )

    def create_instrument(self, instrument: Instrument):
        assert self.is_connected(), "Cannot call function until connected. Call connect() first"

        return self._wrapper.run_on_loop(
            self._m.create_instrument(instrument)
        )

    def expire_instrument(self, instrument_id, expiration_value) -> None:
        assert self.is_connected(), "Cannot call function until connected. Call connect() first"

        return self._wrapper.run_on_loop(
            self._m.expire_instrument(instrument_id=instrument_id, expiration_value=expiration_value)
        )

    def single_sided_booking(self, *, username, instrument_id, price, volume, action) -> None:
        assert self.is_connected(), "Cannot call function until connected. Call connect() first"

        return self._wrapper.run_on_loop(
            self._m.single_sided_booking(username=username, instrument_id=instrument_id, price=price, volume=volume, action=action)
        )

    def get_trade_history(self, instrument_id):
        return self._m.get_trade_history(instrument_id)

    def poll_new_trades(self, instrument_id):
        return self._m.poll_new_trades(instrument_id)

    def clear_trade_history(self):
        return self._m.clear_trade_history()

    def get_user_positions(self, username):
        return self._m.get_user_positions(username)

    def get_usernames(self):
        return self._m.get_usernames()

    def reset_position(self, username, instrument_id):
        pos = self.get_user_positions(username)[instrument_id]
        logger.info(f"[{username}-{instrument_id}] Position before reset: {pos}")

        if pos['volume'] > 0:
            self.single_sided_booking(username=username, instrument_id=instrument_id, price=0.0, volume=pos['volume'], action='sell')
        elif pos['volume'] < 0:
            self.single_sided_booking(username=username, instrument_id=instrument_id, price=0.0, volume=-pos['volume'], action='buy')

        time.sleep(0.25)

        pos = self.get_user_positions(username)[instrument_id]
        if pos['cash'] > 0:
            self.single_sided_booking(username=username, instrument_id=instrument_id, price=pos['cash'], volume=1, action='buy')
            self.single_sided_booking(username=username, instrument_id=instrument_id, price=0.0, volume=1, action='sell')
        elif pos['cash'] < 0:
            self.single_sided_booking(username=username, instrument_id=instrument_id, price=-pos['cash'], volume=1, action='sell')
            self.single_sided_booking(username=username, instrument_id=instrument_id, price=0.0, volume=1, action='buy')

        time.sleep(0.25)

        pos = self.get_user_positions(username)[instrument_id]
        logger.info(f"[{username}-{instrument_id}] Position after reset: {pos}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
