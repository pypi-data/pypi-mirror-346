import threading
import time
import traceback

class DynamicThread(threading.Thread):
    def __init__(self, target, args=(), kwargs=None, timeout=None, switch_on_exception=False):
        super().__init__(target=self.wrapper)
        self._target_func = target
        self._args = args
        self._kwargs = kwargs or {}
        self._timeout = timeout
        self._switch_on_exception = switch_on_exception
        self.exception_occurred = False

    def wrapper(self, *args, **kwargs):
        start = time.time()
        try:
            self._target_func(*self._args, **self._kwargs)
        except Exception:
            self.exception_occurred = True
            traceback.print_exc()
        finally:
            end = time.time()
            if self._timeout and (end - start) > self._timeout:
                print(f"[INFO] Timeout exceeded ({self._timeout}s), changing to daemon.")
                self.daemon = True
            elif self._switch_on_exception and self.exception_occurred:
                print("[INFO] Exception occurred, switching to daemon.")
                self.daemon = True

    def run(self):
        self.wrapper()

def create_thread(target, args=(), kwargs=None, daemon=False, timeout=None, switch_on_exception=False):
    thread = DynamicThread(
        target=target,
        args=args,
        kwargs=kwargs,
        timeout=timeout,
        switch_on_exception=switch_on_exception
    )
    thread.daemon = daemon
    return thread
