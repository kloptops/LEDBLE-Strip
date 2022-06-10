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

import asyncio
import datetime
import inspect

from typing import Any, Union
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

from .util import BaseDriver, BLE_UUID, clamp_byte



class LedbleDriver(BaseDriver):
    CHARACTERISTIC = BLE_UUID(0xFFE1)

    RGB_MODE = {
        "Static red":           128,
        "Static blue":          129,
        "Static green":         130,
        "Static cyan":          131,
        "Static yellow":        132,
        "Static purple":        133,
        "Static white":         134,
        "Tricolor jump":        135,
        "Seven-color jump":     136,
        "Tricolor gradient":    137,
        "Seven-color gradient": 138,
        "Red gradient":         139,
        "Green gradient":       140,
        "Blue gradient":        141,
        "Yellow gradient":      142,
        "Cyan gradient":        143,
        "Purple gradient":      144,
        "White gradient":       145,
        "Red-Green gradient":   146,
        "Red-Blue gradient":    147,
        "Green-Blue gradient":  148,
        "Seven-color flash":    149,
        "Red flash":            150,
        "Green flash":          151,
        "Blue flash":           152,
        "Yellow flash":         153,
        "Cyan flash":           154,
        "Purple flash":         155,
        "White flash":          156,
        }

    ST_DYNAMIC = {
        "Breathe":              128,
        "Gradient":             129,
        "Jump":                 130,
        "Strobe":               131,
        }

    CT_MODE = {
        "Warm 0% Cool 100%":    128,
        "Warm 10% Cool 90%":    129,
        "Warm 20% Cool 80%":    130,
        "Warm 30% Cool 70%":    131,
        "Warm 40% Cool 60%":    132,
        "Warm 50% Cool 50%":    133,
        "Warm 60% Cool 40%":    134,
        "Warm 70% Cool 30%":    135,
        "Warm 80% Cool 20%":    136,
        "Warm 90% Cool 10%":    137,
        "Warm 100% Cool 0%":    138,
        }

    TIMER_MODEL = {
        "Static red":            0,
        "Static blue":           1,
        "Static green":          2,
        "Static cyan":           3,
        "Static yellow":         4,
        "Static purple":         5,
        "Static white":          6,
        "Tricolor jump":         7,
        "Seven-color jump":      8,
        "Tricolor gradient":     9,
        "Seven-color gradient": 10,
        "Warm 0% Cool 100%":    11,
        "Warm 10% Cool 90%":    12,
        "Warm 20% Cool 80%":    13,
        "Warm 30% Cool 70%":    14,
        "Warm 40% Cool 60%":    15,
        "Warm 50% Cool 50%":    16,
        "Warm 60% Cool 40%":    17,
        "Warm 70% Cool 30%":    18,
        "Warm 80% Cool 20%":    19,
        "Warm 90% Cool 10%":    20,
        "Warm 100% Cool 0%":    21,
        }

    DM_MODE = {
        "0%":    128,
        "10%":   129,
        "20%":   130,
        "30%":   131,
        "40%":   132,
        "50%":   133,
        "60%":   134,
        "70%":   135,
        "80%":   136,
        "90%":   137,
        "100%":  138,
        }

    RGB_MODEL = {
        "RGB": 1,
        "RBG": 2,
        "GRB": 3,
        "GBR": 4,
        "BRG": 5,
        "BGR": 6,
        }

    LIGHT_BANNER = {
        "LPD6803":   1,
        "TM1803":    2,
        "UCS1903":   3,
        "WS2811":    4,
        "TM1812":    5,
        "TM1809":    6,
        "WS2801":    7,
        "TLS3001":   8,
        "TLS3008":   9,
        "P9813":    10,
        "UCS8806":  11,
        "TM1829":   12,
        "TM1909":   13,
        }

    DIY_STYLE = {
        "Jump":     0,
        "Breathe":  1,
        "Flash":    2,
        "Gradient": 3,
        }

    def __init__(self):
        """Initialize object."""
        pass

    def compatible_name(self, name: str) -> bool:
        """
        Returns true if this driver is compatible with the selected BLE device
        """
        if name.upper().startswith("LEDBLE"):
            return True

        return False

    async def connect_to_addr(self, mac_address: str, timeout: float = 2.0, adapter: Union[str, None] = None) -> None:
        await super().connect_to_addr(mac_address, timeout, adapter)

        await self._client.connect()
        self.log("connect")


    async def _write_gatt(self, data: bytes) -> None:
        self.log(f'{data=}')
        await self._client.write_gatt_char(self.CHARACTERISTIC, data)


    async def set_on(self) -> None:
        """
        Turn the LED's on
        """
        self.log('on')

        await self._write_gatt(bytes([126, 4, 4, 1, 255, 255, 255, 0, 239]))


    async def set_off(self) -> None:
        """
        Turn the LED's off
        """
        self.log(f'off')

        await self._write_gatt(bytes([126, 4, 4, 0, 255, 255, 255, 0, 239]))


    async def set_rgb_sort(self, rgb_sort: Union[int, str]) -> None:
        """
        Set the RGB sort from RGB_MODEL

        If your colours are showing up wrong when you set them, change them to the correct mapping.
        """
        self.log(f'{rgb_sort=}')

        if isinstance(rgb_sort, str):
            rgb_sort = self.RGB_MODEL[rgb_sort]
        else:
            rgb_sort = clamp_byte(rgb_sort, 1, 6)

        await self._write_gatt(bytes([126, 4, 8, rgb_sort, 255, 255, 255, 0, 239]))


    async def set_rgb(self, r: int, g: int, b: int) -> None:
        """
        Set the RGB color
        """
        self.log(f'{r=},{g=},{b=}')

        await self._write_gatt(bytes([126, 7, 5, 3, clamp_byte(r), clamp_byte(g), clamp_byte(b), 0, 239]))


    async def set_rgb_mode(self, mode: Union[int, str]) -> None:
        """
        Set the RGB mode from RGB_MODE. These are preprogrammed sequences.
        """
        self.log(f'{mode=}')

        if isinstance(mode, str):
            mode = self.RGB_MODE[mode]
        else:
            mode = clamp_byte(mode, 128, 156)

        await self._write_gatt(bytes([126, 5, 3, mode, 3, 255, 255, 0, 239]))


    async def set_speed(self, speed: int) -> None:
        """
        Set the speed of animations
        """
        self.log(f'{speed=}')

        await self._write_gatt(bytes([126, 4, 2, clamp_byte(speed, 0, 100), 255, 255, 255, 0, 239]))


    async def set_brightness(self, brightness: int) -> None:
        """
        Set the brightness.

        Doesnt do much I dont believe.
        """
        self.log(f'{brightness=}')

        await self._write_gatt(bytes([126, 4, 1, clamp_byte(brightness, 0, 100), 255, 255, 255, 0, 239]))


    async def set_diy(self, style: Union[int, str], colors: list[list[int, int, int]]) -> None:
        """
        Set a custom color sequence, with style from DIY_STYLE

        Seems kinda pointless, from what i can tell it is not stored on device... there is no way to replay it
        """
        self.log(f'{style=}. {colors=}')

        if isinstance(style, str):
            style = self.DIY_STYLE[style]
        else:
            style = clamp_byte(style, 0, 3)

        # Begin DIY
        await self._write_gatt(bytes([126, 5, 14, style, 3, 255, 255, 0, 239]))
        await asyncio.sleep(0.1)

        for (r, g, b) in colors:
            # Set colors
            await self._write_gatt(bytes([126, 7, 16, 3, clamp_byte(r), clamp_byte(g), clamp_byte(b), 0, 239]))
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.2)
        await self._write_gatt(bytes([126, 5, 15, style, 3, 255, 255, 0, 239]))


    async def set_music(self, brightness: int, r: int = 0, g: int = 0, b: int = 0) -> None:
        """
        I uh... dunno...
        """
        self.log(f"{brightness=}, ({r=}, {g=}, {b=})")

        await self._write_gatt(bytes([126, 7, 6, clamp_byte(brightness, 0, 100), 0, 0, 0, 0, 239]))


    async def set_dynamic_diy(self, style: Union[int, str], colors: list[list[int, int, int]]) -> None:
        """
        Set a custom color sequence, with style from DIY_STYLE

        Seems kinda pointless, from what i can tell it is not stored on device... there is no way to replay it
        """
        self.log(f'{style=}. {colors=}')

        if isinstance(style, str):
            style = self.DIY_STYLE[style]
        else:
            style = clamp_byte(style, 0, 3)

        # Begin DIY
        await self._write_gatt(bytes([126, 5, 10, style, 3, 255, 255, 0, 239]))
        await asyncio.sleep(0.1)

        for (r, g, b) in colors:
            # Set colors
            await self._write_gatt(bytes([126, 7, 11, 3, clamp_byte(r), clamp_byte(g), clamp_byte(b), 0, 239]))
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.2)
        await self._write_gatt(bytes([126, 5, 12, style, 3, 255, 255, 0, 239]))


    async def set_sensitivity(self, speed: int) -> None:
        """
        Set the speed / sensitivity. It seems to be paired with the dynamic_diy.

        Doesnt appear to do anything.
        """
        self.log(f'{speed=}')

        await self._write_gatt(bytes([126, 4, 7, clamp_byte(speed, 0, 100), 255, 255, 255, 0, 239]))


    def _time_to_seconds(self, hour: int, minute: int) -> int:
        """
        Calculate how many seconds from now hour:minute is from our current time, if that makes sense...

        The led strip does not have a clock, it just sets an on/off timer in the future
        """
        time_now = datetime.datetime.now()

        want_seconds = (((hour * 60) + minute) * 60)
        now_seconds = (((time_now.hour * 60) + time_now.minute) * 60) + time_now.second

        seconds = want_seconds - now_seconds

        if seconds < 0:
            # time is in the past, add a whole day
            seconds += 86400

        self.log(f"{hour}:{minute} -> {seconds}")

        return seconds


    async def set_on_timer(self, hour: int, minute: int, model: Union[int, str] = 1) -> None:
        """
        Sets a timer to turn on the strip at hour:minutes, model from TIMER_MODEL.
        """
        self.log(f'{hour=}, {minute=}, {model=}')

        hour = clamp_byte(hour, 0, 23)
        minute = clamp_byte(minute, 0, 59)

        seconds = self._time_to_seconds(hour, minute)
        minutes = seconds // 60

        await self._write_gatt(bytes([126, 1, 13,  clamp_byte(minutes >> 8), clamp_byte(minutes), 1, model, seconds % 60, 239]))


    async def set_off_timer(self, hour: int, minute: int) -> None:
        """
        Sets a timer to turn off the strip at hour:minutes.
        """
        self.log(f'{hour=}, {minute=}')

        hour = clamp_byte(hour, 0, 23)
        minute = clamp_byte(minute, 0, 59)

        seconds = self._time_to_seconds(hour, minute)
        minutes = seconds // 60

        await self._write_gatt(bytes([126, 1, 13, clamp_byte(minutes >> 8), clamp_byte(minutes), 0, 255, seconds % 60, 239]))


    async def enable_timer(self, on_or_off: int):
        """
        Enable the on or off timer, on = 1, off = 0
        """
        self.log(f'{on_or_off=}')

        await self._write_gatt(bytes([126, clamp_byte(on_or_off, 0, 1), 13, 255, 255, 1, 255, 255, 239]))


    async def disable_timer(self, on_or_off: int):
        """
        Disable the on or off timer, on = 1, off = 0
        """
        self.log(f'{on_or_off=}')

        await self._write_gatt(bytes([126, clamp_byte(on_or_off, 0, 1), 13, 255, 255, 0, 255, 255, 239]))


    async def set_dim(self, dim: int) -> None:
        """
        Set the dim ... or brightness ? 0 to 100
        """
        self.log(f'{dim=}')

        ## This is only 8 bytes, most commands seem to be 9 bytes
        await self._write_gatt(bytes([126, 5, 5, 1, clamp_byte(dim, 0, 100), 255, 255, 8, 239]))


    async def set_color_warm(self, warm: int, cool: [int, None] = None) -> None:
        """
        Set the color warm ...

        From the app you can go from 0-100 on warm, and it sets the cool to (100 - warm)
        """
        self.log(f'{warm=}, {cool=}')

        warm = clamp_byte(warm, 0, 100)
        if cool is None:
            cool = 100 - warm

        await self._write_gatt(bytes([126, 6, 5, 2, warm, cool, 255, 8, 239]))


    async def set_color_warm_model(self, model:  Union[int, str]) -> None:
        """
        Set color model from CT_MODE

        Doesnt seem to work, even on the app...
        """
        self.log(f'{model=}')

        if isinstance(model, str):
            model = self.CT_MODE[model]
        else:
            model = clamp_byte(model, 128, 138)

        await self._write_gatt(bytes([126, 5, 3, model, 2, 255, 255, 0, 239]))


    async def set_dim_model(self, model:  Union[int, str]) -> None:
        """
        Set color model from DM_MODE

        Doesnt seem to work, even on the app...
        """
        self.log(f'{model=}')

        if isinstance(model, str):
            model = self.DM_MODE[rgb_sort]
        else:
            model = clamp_byte(model, 128, 138)

        await self._write_gatt(bytes([126, 5, 3, model, 1, 255, 255, 0, 239]))


    async def set_dynamic(self, model:  Union[int, str]) -> None:
        """
        Set dynamic... looks to be preprogrammed sequences, from ST_DYNAMIC
        """
        self.log(f'{model=}')

        if isinstance(model, str):
            model = self.ST_DYNAMIC[model]
        else:
            model = clamp_byte(model, 128, 131)

        await self._write_gatt(bytes([126, 5, 3, model, 4, 255, 255, 0, 239]))

