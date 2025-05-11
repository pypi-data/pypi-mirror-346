import asyncio
from aio_process_pool import ProcessPool

p = ProcessPool(3)

def foo(x):
    return x+1


async def blub():
    r = await p.map(foo, [1, 2, 3])
    print(r)

asyncio.run(blub())
