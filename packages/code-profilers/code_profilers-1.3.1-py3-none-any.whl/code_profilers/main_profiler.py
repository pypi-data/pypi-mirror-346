from code_profilers.logger import profiler_logger

from code_profilers.profilers.base.profiler import BaseProfiler
from code_profilers.settings import DEFAULT_SETTINGS


class MainProfiler:
    def __init__(self, **kwargs) -> None:
        self.__settings = {**DEFAULT_SETTINGS}
        self.__settings.update(**kwargs)

        self.__sub_profilers: list[BaseProfiler] = []

    def register_profiler(self, sub_profiler: BaseProfiler):
        sub_profiler.patch(**self.__settings)
        self.__sub_profilers.append(sub_profiler)

    def start(self):
        for sub_profiler in self.__sub_profilers:
            try:
                sub_profiler.start()
            except Exception as e:
                profiler_logger.exception(e)

    def stop(self):
        for sub_profiler in self.__sub_profilers:
            try:
                sub_profiler.stop()
            except Exception as e:
                profiler_logger.exception(e)

    def report(self):
        self.__report_start_info()
        for sub_profiler in self.__sub_profilers:
            try:
                sub_profiler.report()
                self.__after_sub_profile_report()
            except Exception as e:
                profiler_logger.exception(e)
        self.__report_end_info()

    def __report_start_info(self):
        print("Code Profilers Report:")
        for setting_key, setting_value in self.__settings.items():
            print(f" {setting_key.upper()}: {setting_value}")
        print()

    def __after_sub_profile_report(self):
        print()

    def __report_end_info(self):
        print()
