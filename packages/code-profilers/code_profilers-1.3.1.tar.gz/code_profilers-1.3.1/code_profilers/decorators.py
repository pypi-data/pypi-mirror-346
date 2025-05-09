from code_profilers.main_profiler import MainProfiler
from code_profilers.profilers.base.profiler import BaseProfiler


def profile_code_decorator(main_profiler: MainProfiler | BaseProfiler):
    def inner(func):
        def wrapper(*args, **kwargs):
            main_profiler.start()
            try:
                res = func(*args, **kwargs)

                main_profiler.stop()
                main_profiler.report()

                return res
            except Exception as e:
                main_profiler.stop()
                main_profiler.report()

                raise e

        return wrapper
    return inner
