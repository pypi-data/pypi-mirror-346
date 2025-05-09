import asyncio
from aio_process_pool import Executor

def fib(n):
    if n <= 2: return 1
    return fib(n-1) + fib(n-2)

def fib_wrapper(n):
    print(f"fib({n}) = .....")
    result = fib(n)
    print(f"fib({n}) = {result}")


async def watch_htop_and_output_while_execution():
    pool = Executor()
    await pool.map_async(fib_wrapper, range(45))

asyncio.run(watch_htop_and_output_while_execution())
