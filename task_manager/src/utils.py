import asyncio
from threading import Thread, Lock


func_mapped = {'CreateUser': 0,
               'CreateTask': 1,
               'UpdateTask': 2,
               'DeleteTask': 3,
               'GetTask': 4,
               'ListTasks': 5}
thread_return = [None for _ in range(len(func_mapped.keys()))]
thread_lock = [Lock() for _ in range(len(func_mapped.keys()))]


def thread_async_wrapper(func, *args):
    '''
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(func(*args))
    loop.close()
    '''
    asyncio.run(func(*args))


def thread_func(func, *args):
    thread = Thread(target=thread_async_wrapper, args=(func, *args,))
    thread.start()
    thread.join()


def run_and_return(function, func_name: str, *args):
    thread_func(function, *args)
    with thread_lock[func_mapped[func_name]]:
        result = thread_return[func_mapped[func_name]]
    return result
