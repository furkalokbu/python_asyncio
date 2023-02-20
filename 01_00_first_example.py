import time
from measure_time import async_measure_time
import asyncio


async def tick():
    print('Tick')
    await asyncio.sleep(1)
    print('Tock')


@async_measure_time
async def main():
    # for _ in range(3):
        # tick()
    await asyncio.gather(tick(), tick(), tick())


if __name__ == '__main__':
    asyncio.run(main())
