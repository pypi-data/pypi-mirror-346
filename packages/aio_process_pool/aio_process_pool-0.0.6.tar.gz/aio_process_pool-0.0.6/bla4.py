import asyncio

from aio_process_pool.process_pool import EventInterrupter

async def task1(e):
    async with EventInterrupter(e):
        print("1")
        await asyncio.sleep(10)
        print("2")

async def task2(e):
    await asyncio.sleep(1)
    print("killer awaking")
    e.set()

async def bla():
    e = asyncio.Event()

    t1 = asyncio.create_task(task1(e))
    t2 = asyncio.create_task(task2(e))

    await asyncio.gather(t1, t2)



asyncio.run(bla())
