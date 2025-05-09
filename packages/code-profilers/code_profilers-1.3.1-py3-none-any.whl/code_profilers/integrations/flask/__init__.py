from flask import Flask

from code_profilers.main_profiler import MainProfiler


class FlaskIntegration:

    def __init__(self, app: Flask, profiler: MainProfiler) -> None:
        self.app = app
        self.profiler = profiler

        self.__patch_wsgi_app()

    def __patch_wsgi_app(self):
        wsgi_app = self.app.wsgi_app

        def mock_wsgi_app(*args, **kwargs):
            self.profiler.start()

            try:
                response = wsgi_app(*args, **kwargs)

                self.profiler.stop()
                self.profiler.report()

            except Exception as e:
                self.profiler.stop()
                self.profiler.report()

                raise e

            return response

        self.app.wsgi_app = mock_wsgi_app
