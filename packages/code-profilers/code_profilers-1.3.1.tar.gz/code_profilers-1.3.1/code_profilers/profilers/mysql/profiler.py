import time

from code_profilers.profilers.base.profiler import BaseProfiler
from code_profilers.profilers.mysql.reporter import MySQLTerminalReporter
from code_profilers.profilers.mysql.settings import DEFAULT_SETTINGS


try:
    from mysql.connector.cursor import MySQLCursor
    from mysql.connector import MySQLConnection
except Exception as e:
    raise Exception("MySQLProfiler Will not work without mysql installed.")


class MySQLProfiler(BaseProfiler):

    def __init__(self, **settings) -> None:
        super().__init__(**{**DEFAULT_SETTINGS, **settings})

        self.__queries: list[dict] = []
        self.__dict_queries = {}

        self.reporter = MySQLTerminalReporter()

    def patch(self, **kwargs):
        super(MySQLProfiler, self).patch(**kwargs)

        self.__patch_MySQLConnection()

    def __patch_MySQLConnection(self):
        def mock_cursor(*args, **kwargs):
            cursor: MySQLCursor = real_cursor(*args, **kwargs)
            self.__patch_cursor(cursor)
            return cursor

        real_cursor = MySQLConnection.cursor
        MySQLConnection.cursor = mock_cursor

    def __patch_cursor(self, cursor):
        self.__patch_MySQLCursor_execute(cursor)
        self.__patch_MySQLCursor_executemany(cursor)

    def __patch_MySQLCursor_execute(self, cursor: MySQLCursor):

        def mock_execute(operation, *args, **kwargs):
            query = {
                'is_broken': False
            }

            query['sql'] = operation

            if self.settings.get('profile_queries_params'):
                params = args[0] if len(args) > 0 else None
                params = params if params else kwargs.get('params')

                query['params'] = params if params else None

            start = time.monotonic()

            try:
                res = real_execute(operation, *args, **kwargs)

                end = time.monotonic()
                if self.settings.get('profile_queries_time'):
                    query['timespan'] = {
                        'start': start,
                        'end': end,
                        'diff': end - start
                    }
            except Exception as e:
                end = time.monotonic()
                if self.settings.get('profile_queries_time'):
                    query['timespan'] = {
                        'start': start,
                        'end': end,
                        'diff': end - start
                    }

                if self.settings.get('report_broken_queries'):
                    query['is_broken'] = True

                if not self.settings.get('combine_duplicated_queries'):
                    self.__queries.append(query)
                else:
                    if query['sql'] not in self.__dict_queries:
                        self.__dict_queries[query['sql']] = [query]
                    else:
                        self.__dict_queries[query['sql']].append(query)

                raise e

            if not self.settings.get('combine_duplicated_queries'):
                self.__queries.append(query)
            else:
                if query['sql'] not in self.__dict_queries:
                    self.__dict_queries[query['sql']] = [query]
                else:
                    self.__dict_queries[query['sql']].append(query)

            return res

        real_execute = cursor.execute
        cursor.execute = mock_execute

    def __patch_MySQLCursor_executemany(self, cursor: MySQLCursor):

        def mock_executemany(operation, seq_params, *args, **kwargs):
            query = {
                'is_broken': False
            }

            query['sql'] = operation

            if self.settings.get('profile_queries_params'):
                params = args[0] if len(args) > 0 else None
                params = params if params else kwargs.get('params')

                query['params'] = seq_params

            start = time.monotonic()

            try:
                res = real_executemany(operation, seq_params, *args, **kwargs)

                end = time.monotonic()
                if self.settings.get('profile_queries_time'):
                    query['timespan'] = {
                        'start': start,
                        'end': end,
                        'diff': end - start
                    }

            except Exception as e:
                end = time.monotonic()
                if self.settings.get('profile_queries_time'):
                    query['timespan'] = {
                        'start': start,
                        'end': end,
                        'diff': end - start
                    }

                if self.settings.get('report_broken_queries'):
                    query['is_broken'] = True

                if not self.settings.get('combine_duplicated_queries'):
                    self.__queries.append(query)
                else:
                    if query['sql'] not in self.__dict_queries:
                        self.__dict_queries[query['sql']] = [query]
                    else:
                        self.__dict_queries[query['sql']].append(query)

                raise e

            if not self.settings.get('combine_duplicated_queries'):
                self.__queries.append(query)
            else:
                if query['sql'] not in self.__dict_queries:
                    self.__dict_queries[query['sql']] = [query]
                else:
                    self.__dict_queries[query['sql']].append(query)

            return res

        real_executemany = cursor.executemany
        cursor.executemany = mock_executemany

    def __reset(self):
        self.__queries.clear()
        self.__dict_queries.clear()

    def start(self):
        self.__reset()

    def stop(self):
        pass

    def report(self):
        self.reporter.report_environments(
            main_settings=self.main_settings,
            settings=self.settings,
            cls_info={
                'name': 'MySQL Profiler',
            })

        is_combined_query = self.settings.get('combine_duplicated_queries')

        if not is_combined_query:
            for index, query_profile in enumerate(self.__queries):
                self.reporter.report(index, query_profile)
        else:
            for index, (key, value) in enumerate(self.__dict_queries.items()):
                self.reporter.report(index, value, is_combined_query=True)

        self.reporter.report_final_report(
            self.__dict_queries if is_combined_query else self.__queries,
            is_combined_query
        )
