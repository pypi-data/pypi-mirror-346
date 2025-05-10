import asyncio
from functools import partial
import pytest
import time
from aio_process_pool import Executor
# from concurrent.futures import ProcessPoolExecutor as Executor

# exe = Executor()

def fib(n):
    if n <= 2: return 1
    return fib(n-1) + fib(n-2)

first_30_fib_numbers = []

def fib_wrapper(n):
    print(f"fib({n}) = .....")
    result = fib(n)
    print(f"fib({n}) = {result}")


def get_range():
    return list(range(20, 30)) * 5

# async def watch_htop_and_output_while_execution():
#     exe = Executor()
#     await exe.map_async(fib_wrapper, get_range())
#     exe.shutdown()
#
# asyncio.run(watch_htop_and_output_while_execution())


# list(exe.map(fib_wrapper, get_range()))
# list(map(fib_wrapper, get_range()))

async def test_shutdown():
    exe = Executor(max_workers=2)
    loop = asyncio.get_event_loop()

    # start long running jobs
    futures = [loop.run_in_executor(exe, partial(fib, 33)) for _ in range(5)]
    futures += [exe.shutdown_async(wait=True, cancel_futures=True)]

    results = await asyncio.gather(*futures, return_exceptions=True)

    fib33 = 3524578 # fib(33)
    assert results[0] == fib33
    assert results[1] == fib33
    assert isinstance(results[2], asyncio.CancelledError)
    assert isinstance(results[3], asyncio.CancelledError)
    assert isinstance(results[4], asyncio.CancelledError)
    assert results[5] is None

# exe = Executor()
# print(exe.map(fib, range(10)))
# exe.shutdown()

asyncio.run(test_shutdown())
