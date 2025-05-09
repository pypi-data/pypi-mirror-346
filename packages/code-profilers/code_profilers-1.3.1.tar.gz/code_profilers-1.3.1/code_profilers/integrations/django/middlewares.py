from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class DjangoMiddlewareIntegration(MiddlewareMixin):
    def process_request(self, request):
        try:
            settings.MAIN_PROFILER.start()
        except Exception as e:
            pass

    def process_response(self, request, response):
        try:
            settings.MAIN_PROFILER.stop()
            settings.MAIN_PROFILER.report()
        except Exception as e:
            pass
        return response
