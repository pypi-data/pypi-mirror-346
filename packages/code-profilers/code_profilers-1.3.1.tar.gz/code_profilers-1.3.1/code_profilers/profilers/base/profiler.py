class BaseProfiler:

    def __init__(self, **settings) -> None:
        self.settings = settings
        self.main_settings = {}

    def patch(self, **kwargs):
        self.main_settings = kwargs

    def start(self):
        pass

    def stop(self):
        pass

    def report(self):
        pass
