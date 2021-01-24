import logging

from .management_client import ManagementClient
from . import management_client
from .synchronous_wrapper import SynchronousWrapper

logger = logging.getLogger('client')

DEFAULT_HOST = 'opamux0674'
DEFAULT_MGMT_PORT = 9001


class Management:
    def __init__(self,
                 host: str = DEFAULT_HOST,
                 mgmt_port: int = DEFAULT_MGMT_PORT,
                 full_message_logging: bool = False,
                 max_nr_trade_history: int = 100):
        if full_message_logging:
            management_client.logger.setLevel('VERBOSE')
        self._m = ManagementClient(host=host, port=mgmt_port, max_nr_trade_history=max_nr_trade_history)

        self._wrapper = SynchronousWrapper([self._m])

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

    def create_instrument(self, instrument_id, tick_size, extra_info='') -> None:
        assert self.is_connected(), "Cannot call function until connected. Call connect() first"

        return self._wrapper.run_on_loop(
            self._m.create_instrument(instrument_id=instrument_id, tick_size=tick_size, extra_info=extra_info)
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

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
