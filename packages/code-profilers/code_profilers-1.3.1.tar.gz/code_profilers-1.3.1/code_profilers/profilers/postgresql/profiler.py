import time

from code_profilers.profilers.base.profiler import BaseProfiler
from code_profilers.profilers.postgresql.reporter import PostgreSQLTerminalReporter
from code_profilers.profilers.postgresql.settings import DEFAULT_SETTINGS


try:
    import psycopg2
    from psycopg2.extensions import connection, cursor
except Exception as e:
    raise Exception("PostgreSQLProfiler Will not work without postgres installed.")


class PostgreSQLProfilerCursor(cursor):

    @classmethod
    def init_class(cls, profiler):
        cls.__profiler = profiler
        return cls

    def executemany(self, query=None, vars=None):
        return self.__profiler.patch_PostgreSQLProfilerCursor_executemany(
            self.__cursor, query, vars,
        )

    def execute(self, query, vars = None):
        return self.__profiler.patch_PostgreSQLProfilerCursor_execute(
            self, query, vars,
        )

    def super_executemany(self, query, vars_list):
        return super().executemany(query, vars_list)

    def super_execute(self, query, vars = None):
        return super().execute(query, vars)


class PostgreSQLProfilerConnection(connection):

    @classmethod
    def init_class(cls, profiler):
        cls.__profiler = profiler
        return cls

    def cursor(self, *args, **kwargs):
        if not issubclass(self.cursor_factory, PostgreSQLProfilerCursor):
            self.cursor_factory = self.__patch_cursor().init_class(self.__profiler)

        return super().cursor(*args, **kwargs)

    def __patch_cursor(self):
        class PostgreSQLProfilerCursorFactory(PostgreSQLProfilerCursor, self.cursor_factory):
            pass

        return PostgreSQLProfilerCursorFactory


class PostgreSQLProfiler(BaseProfiler):

    def __init__(self, **settings) -> None:
        super().__init__(**{**DEFAULT_SETTINGS, **settings})

        self.__queries: list[dict] = []
        self.__dict_queries = {}

        self.reporter = PostgreSQLTerminalReporter()

    def patch(self, **kwargs):
        super(PostgreSQLProfiler, self).patch(**kwargs)

        self.__patch_PostgressConnection()

    def __patch_PostgressConnection(self):
        def mock_connection(*mock_connection_args, **mock_connection_kwargs):
            if len(mock_connection_args) > 2:
                mock_connection_args[2] = self.__get_mocked_cursor_factory(mock_connection_args[2])
            elif 'cursor_factory' in mock_connection_kwargs:
                mock_connection_kwargs['cursor_factory'] = self.__get_mocked_cursor_factory(mock_connection_kwargs['cursor_factory'])
            else:
                mock_connection_kwargs['cursor_factory'] = PostgreSQLProfilerCursor.init_class(self)

            mock_connection_kwargs['connection_factory'] = PostgreSQLProfilerConnection.init_class(self)
            return real_connection(*mock_connection_args, **mock_connection_kwargs)

        real_connection = psycopg2.connect
        psycopg2.connect = mock_connection

    def __get_mocked_cursor_factory(self, cursor_factory):
        class PostgreSQLProfilerCursorFactory(PostgreSQLProfilerCursor, cursor_factory):
            pass

        return PostgreSQLProfilerCursorFactory.init_class(self)

    def patch_PostgreSQLProfilerCursor_execute(self, cursor: PostgreSQLProfilerCursor, query_str, vars):
        query = {
            'is_broken': False
        }

        query['sql'] = query_str

        if self.settings.get('profile_queries_params'):
            query['params'] = vars

        start = time.monotonic()

        try:
            res = cursor.super_execute(query_str, vars)

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

    def patch_PostgreSQLProfilerCursor_executemany(self, cursor: PostgreSQLProfilerCursor, query_str, vars_list):
        query = {
            'is_broken': False
        }

        query['sql'] = query_str

        if self.settings.get('profile_queries_params'):
            query['params'] = vars_list

        start = time.monotonic()

        try:
            res = cursor.super_executemany(query_str, vars_list)

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
                'name': 'Postgres Profiler',
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
