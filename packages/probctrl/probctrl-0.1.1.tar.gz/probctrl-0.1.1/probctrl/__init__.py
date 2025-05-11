
import random
import time
import threading
from functools import wraps
from collections import deque
from datetime import datetime, timedelta


def p(prob, verbose=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            triggered = random.random() < prob
            if verbose:
                print(f"[probctrl:p={prob}] Triggered: {triggered}")
            if triggered:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def delay(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def delayed():
                time.sleep(seconds)
                func(*args, **kwargs)
            threading.Thread(target=delayed).start()
        return wrapper
    return decorator


def throttle(calls_per_second):
    interval = 1.0 / calls_per_second
    last_called = deque()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            while last_called and (now - last_called[0]).total_seconds() > 1:
                last_called.popleft()

            if len(last_called) < calls_per_second:
                last_called.append(now)
                return func(*args, **kwargs)
            else:
                def delayed():
                    while True:
                        time.sleep(interval)
                        now2 = datetime.now()
                        while last_called and (now2 - last_called[0]).total_seconds() > 1:
                            last_called.popleft()
                        if len(last_called) < calls_per_second:
                            last_called.append(datetime.now())
                            func(*args, **kwargs)
                            break
                threading.Thread(target=delayed).start()
        return wrapper
    return decorator
