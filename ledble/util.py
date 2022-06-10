"""

MIT License

Copyright (c) 2022 Jacob Smith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import inspect
from typing import Any, Union

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError


class BaseDriver():
    _client = None
    _debug = False

    def log(self, *args) -> None:
        if self._debug:
            print(f" {self.__class__.__name__} -> {inspect.currentframe().f_back.f_code.co_name}: ", *args)

    def __init__(self):
        pass

    async def connect_to_addr(self, mac_address: str, timeout: float = 3.0, adapter: Union[str, None] = None) -> None:
        """
        Finds BLE by mac_address, then sets self._client to the BleakClient found.

        """
        kwargs = {}
        if adapter is not None:
            kwargs['adapter'] = adapter

        device = await BleakScanner.find_device_by_address(mac_address, timeout=timeout, **kwargs)

        if not device:
            raise BleakError(f'A device with address {mac_address} could not be found')

        self._client = BleakClient(device, disconnected_callback=self._handle_disconnect)

    async def disconnect(self) -> None:
        """
        Close connection to device.
        """
        if self._client.is_connected:
            await self._client.disconnect()

    def _handle_disconnect(self, client: BleakClient) -> None:
        self.log(f"{client=}")


def BLE_UUID(uuid: int):
    if uuid <= 0xffff:
        uuid = (uuid << 96) | 0x1000800000805f9b34fb
    text = f"{uuid:032x}"
    return '-'.join((text[:8], text[8:12], text[12:16], text[16:20], text[20:]))


def clamp_byte(value: int, minimum: int = 0, maximum: int = 255) -> int:
    return int(max(minimum, min(value, maximum)))

