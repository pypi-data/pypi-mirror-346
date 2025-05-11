import asyncio
import time
from functools import partial
from threading import Thread

from aio_process_pool import Executor
from tests.shutdown_test import fib, fib33

async def test_shutdown_parameters(wait, cancel_futures):
    exe = Executor(max_workers=2)
    loop = asyncio.get_event_loop()

    # start "long" running jobs
    futures = [loop.run_in_executor(exe, partial(fib, 33)) for _ in range(5)]

    def shutdown_wrapper(wait, cancel_futures):
        exe.shutdown(wait, cancel_futures=cancel_futures)

    shutdown_thread = Thread(target=shutdown_wrapper, args=(wait, cancel_futures))
    shutdown_thread.start()
    time.sleep(0.2)

    results = await asyncio.gather(*futures, return_exceptions=True)

    if cancel_futures:
        for i in range(5):
            assert isinstance(results[i], asyncio.CancelledError)
    else:
        for i in range(5):
            assert results[i] == fib33

    assert exe.is_shutdown()

async def blub():
    await test_shutdown_parameters(True, True)
    await test_shutdown_parameters(True, False)
    await test_shutdown_parameters(False, True)
    await test_shutdown_parameters(False, False)

asyncio.run(blub())
