# Reference: https://docs.python.org/3/library/asyncio-task.html

import asyncio
import time


async def say_after(delay, what):
    print(f"{what} started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"{what} done at {time.strftime('%X')}")


async def main():
    # asyncio.TaskGroup() - new in Python3.11
    # https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup
    async with asyncio.TaskGroup() as tg:
        tg.create_task(say_after(1, "hello"))

        tg.create_task(say_after(2, "world"))

    # The await is implicit when the context manager exits.


asyncio.run(main())
