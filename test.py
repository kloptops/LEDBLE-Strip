import asyncio
from bleak import BleakScanner

import ledble


async def main():
    driver = ledble.LedbleDriver()

    """
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"{d.address}: {d.name}")
    """

    ADDRESS = "C0:00:00:00:02:37"
    print(f"Connecting to {ADDRESS}")

    await driver.connect_to_addr(ADDRESS)
    print("Connected")

    # await driver.set_rgb_sort('GRB')
    # await driver.set_rgb(0, 0, 225)
    await driver.set_dynamic(131)
    # await driver.set_brightness(10)
    await driver.set_speed(50)

    """
    Not working....
    await driver.set_diy(
        'Gradient',
        [
            [255,   0,   0],
            [  0, 255,   0],
            [  0,   0, 255],
            ])
    await asyncio.sleep(0.1)
    await driver.set_speed(50)
    """


    await driver.disconnect()
    print("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())

