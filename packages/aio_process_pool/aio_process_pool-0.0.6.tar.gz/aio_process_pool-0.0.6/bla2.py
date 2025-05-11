import asyncio
from functools import partial
from aio_process_pool import AsyncProcessPool

def foo(x):
    return x+1

pp = AsyncProcessPool()
