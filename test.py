import asyncio
import colorsys
import platform

from bleak import BleakScanner

import ledble
from ledble.util import clamp_byte


def hsv_to_rgb(hsv):
    """
    HSV to RGB, uses colorsys module, converts it to bytes suitable for the LedbleDriver
    """
    rgb = colorsys.hsv_to_rgb(*hsv)

    return [
        clamp_byte(rgb[0] * 255, 0, 255),
        clamp_byte(rgb[1] * 255, 0, 255),
        clamp_byte(rgb[2] * 255, 0, 255)]


def hsv_gradient_rgb(start: list[float, float, float], end: list[float, float, float], steps) -> list[int, int, int]:
    """
    Does a gradient between HSV `start` and HSV `end` in `step` steps.

    """

    diff = (
        (end[0] - start[0]) / float(steps),
        (end[1] - start[1]) / float(steps),
        (end[2] - start[2]) / float(steps))

    print("Gradient -> ")
    print(f"   {start=}")
    print(f"   {end=}")
    print(f"   {diff=}, {steps=}")

    yield hsv_to_rgb(start)
    for i in range(steps-1):
        start[0] += diff[0]
        start[1] += diff[1]
        start[2] += diff[2]
        yield hsv_to_rgb(start)


async def rainbow_gradient(driver, brightness: int=100, saturation: int=100):
    """

    A simple rainbow cycle animations

    """

    brightness = clamp_byte(brightness, 0, 100) / 100.
    saturation = clamp_byte(saturation, 0, 100) / 100.

    for i, color in enumerate(hsv_gradient_rgb([0, saturation, brightness], [1, saturation, brightness], 100)):
        await driver.set_rgb(*color)
        await asyncio.sleep(0.1)


async def main():
    driver = ledble.LedbleDriver()
    ADDRESS = None
    # ADDRESS = "C0:00:00:00:02:37"
    adapter = None

    if platform.system() == 'Linux':
        # hci1
        adapter='hci1'

    if ADDRESS is None:
        print("Finding a compatible device")
        # devices = await BleakScanner.discover(adapter=adapter)
        devices = await BleakScanner.discover()

        for d in devices:
            if driver.compatible_name(d.name):
                ADDRESS = d.address
                break

        else:
            print("Unable to find any compatible devices")
            return

    print(f"Connecting to {ADDRESS}")

    await driver.connect_to_addr(ADDRESS, adapter=adapter)
    print("Connected")

    # await driver.set_on()
    # await driver.set_rgb_sort('GRB')
    # await driver.set_rgb(0, 0, 225)
    # await driver.set_dynamic(131)
    # await driver.set_brightness(10)
    # await driver.set_speed(50)

    await rainbow_gradient(driver, 50)

    await driver.disconnect()
    print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())

