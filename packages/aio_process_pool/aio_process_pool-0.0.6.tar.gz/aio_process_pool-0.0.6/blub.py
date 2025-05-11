from aio_process_pool import Executor

def fib(n):
    assert n >= 0
    if n == 0: return 0
    if n <= 2: return 1
    return fib(n-1) + fib(n-2)

first_30_fib_numbers = [fib(x) for x in range(30)]

import threading
print(threading.active_count())

def test_map():
    exe = Executor()
    assert exe.map(fib, range(30)) == first_30_fib_numbers
    exe.shutdown()

def test_context_manager():
    with Executor() as exe:
        assert exe.map(fib, range(30)) == first_30_fib_numbers
