try:
    from pygments.style import Style
    from pygments.token import Keyword, Name, Comment, String, Error, \
        Number, Operator, Generic, Whitespace

    class CustomStyle(Style):
        """
        The default style (inspired by Emacs 22).
        """
        name = 'default'

        background_color = "#f8f8f8"

        styles = {
            Whitespace:                "#bbbbbb",
            Comment:                   "italic #3D7B7B",
            Comment.Preproc:           "noitalic #9C6500",

            #Keyword:                   "bold #AA22FF",
            Keyword:                   "bold #008000",
            Keyword.Pseudo:            "nobold",
            Keyword.Type:              "nobold #B00040",

            Operator:                  "#FFAD66",
            Operator.Word:             "bold #AA22FF",

            Name.Builtin:              "#008000",
            Name.Function:             "#0000FF",
            Name.Class:                "bold #0000FF",
            Name.Namespace:            "bold #0000FF",
            Name.Exception:            "bold #CB3F38",
            Name.Variable:             "#19177C",
            Name.Constant:             "#880000",
            Name.Label:                "#767600",
            Name.Entity:               "bold #717171",
            Name.Attribute:            "#687822",
            Name.Tag:                  "bold #008000",
            Name.Decorator:            "#AA22FF",

            String:                    "#D2665A",
            String.Doc:                "italic",
            String.Interpol:           "bold #A45A77",
            String.Escape:             "bold #AA5D1F",
            String.Regex:              "#A45A77",
            #String.Symbol:             "#B8860B",
            String.Symbol:             "#19177C",
            String.Other:              "#008000",
            Number:                    "#FFAD66",

            Generic.Heading:           "bold #000080",
            Generic.Subheading:        "bold #800080",
            Generic.Deleted:           "#A00000",
            Generic.Inserted:          "#008400",
            Generic.Error:             "#E40000",
            Generic.Emph:              "italic",
            Generic.Strong:            "bold",
            Generic.EmphStrong:        "bold italic",
            Generic.Prompt:            "bold #000080",
            Generic.Output:            "#717171",
            Generic.Traceback:         "#04D",

            Error:                     "border:#FF0000"
        }

except Exception:
    pass

class MySQLTerminalReporter:

    def __init__(self) -> None:
        pass

    def report_environments(
        self, main_settings: dict, settings: dict, cls_info: dict
    ):
        print(f" {cls_info['name']} Report:")
        spaces = 3
        for setting_key, setting_value in settings.items():
            print(f"{' ' * spaces}{setting_key.upper()}: {setting_value}")

        print(f"\n{' ' * spaces}Queries:\n")

    def report(self, index: int, query_profile: dict|list, *args, **kwargs):
        ####### Report Query Number
        self.__print_query_number(index)
        sql_name_spaces = 4
        print(f"{' ' * sql_name_spaces}| SQL:")

        ####### Filter Query From Spaces
        _query_str = self.__prepare_query(query_profile, kwargs.get('is_combined_query'))

        ####### Report Query SQL
        print()
        print(_query_str)
        print()

        ####### Report Number Of Duplication
        self.__report_duplication_number(query_profile, kwargs.get('is_combined_query'))

        ####### Report Broken SQLs
        self.__report_broken_queries(query_profile, kwargs.get('is_combined_query'))

        ####### Report Time Span For Query Execution
        self.__report_time_span(query_profile, kwargs.get('is_combined_query'))

        ####### Report Query Params Params
        self.__report_param(query_profile, kwargs.get('is_combined_query'))

        ####### Close Query Report
        sql_name_spaces = 4
        print(f"{' ' * sql_name_spaces} {'__' * 30}")
        print()

    def __print_query_number(self, index):
        print(f"  {index + 1}")

    def __prepare_query(self, query_profile: dict|list, is_combined_query):
        if is_combined_query:
            _query_sql: str = query_profile[0]['sql']
        else:
            _query_sql: str = query_profile['sql']

        try:
            from pygments import highlight
            from pygments.lexers.sql import PostgresLexer
            from pygments.formatters import TerminalTrueColorFormatter

            import sqlparse

            _query_sql = highlight(
                sqlparse.format(
                    _query_sql,
                    keyword_case='upper',
                    reindent=True,
                    reindent_aligned=True,
                    use_space_around_operators=True,
                ),
                PostgresLexer(stripnl=False),
                TerminalTrueColorFormatter(style=CustomStyle)
            )
        except:
            pass

        _lines = []
        for line in _query_sql.splitlines():
            if line.strip() != '':
                _lines.append(line)

        return '\n'.join(_lines)

    def __report_duplication_number(self, query_profile, is_combined_query):
        _spaces = 4
        if not is_combined_query:
            duplication_number = 1
        else:
            duplication_number = len(query_profile)

        print(f"{' ' * _spaces}|")
        print(f"{' ' * _spaces}| Duplication Number: {duplication_number}")

    def __report_broken_queries(self, query_profile, is_combined_query):
        _spaces = 4
        print(f"{' ' * _spaces}|")

        if not is_combined_query:
            print(f"{' ' * _spaces}| Broken Queries: {query_profile.get('is_broken', False)}")

        else:
            broken_queries = [
                index + 1
                for index, _query in enumerate(query_profile)
                if _query.get('is_broken', False)]
            print(f"{' ' * _spaces}| Broken Queries: {broken_queries}")

    def __report_time_span(self, query_profile: dict|list, is_combined_query):
        timespan_spaces = 4
        print(f"{' ' * timespan_spaces}|")
        if not is_combined_query:
            if query_profile.get('timespan'):
                print(f"{' ' * timespan_spaces}| Time Span: {round(query_profile['timespan']['diff'] * 1000, 2)} ms")
        else:
            print(f"{' ' * timespan_spaces}| Time Spans:")
            for index, _query in enumerate(query_profile):
                if _query.get('timespan'):
                    print(
                        f"{' ' * timespan_spaces}|"
                        f"{' ' * 3}Query {index + 1} Time Span. {round(_query['timespan']['diff'] * 1000, 2)} ms")

    def __report_param(self, query_profile: dict|list, is_combined_query):
        params_spaces = 4
        print(f"{' ' * params_spaces}|")
        print(f"{' ' * params_spaces}| Params:")

        if not is_combined_query:
            if query_profile.get('params'):
                params = query_profile.get('params')
                spaces = 2
                if isinstance(params, (list, tuple)):
                    print(f"{' ' * params_spaces}|{' ' * spaces}| ({params})")
                elif isinstance(params, dict):
                    for key, value in params.items():
                        print(f"{' ' * params_spaces}|{' ' * spaces}| {key}: {value}")

        else:
            for index, _query in enumerate(query_profile):
                if _query.get('params'):
                    print(f"{' ' * params_spaces}|{' ' * 2}| Query {index + 1} Params:")
                    params = _query.get('params')
                    if isinstance(params, (list, tuple)):
                        print(f"{' ' * params_spaces}|{' ' * 2}|{' ' * 2}| ({params})")
                    elif isinstance(params, dict):
                        for key, value in params.items():
                            print(f"{' ' * params_spaces}|{' ' * 2}|{' ' * 2}| {key}: {value}")

                    print(f"{' ' * params_spaces}|{' ' * 2}|")

    def report_final_report(self, queries: dict|list, is_combined_query):
        queries_count = 0
        max_query_time = 0

        if is_combined_query:
            for index, queries in queries.items():
                queries_count += len(queries)
                for query in queries:
                    if query['timespan']['diff'] * 1000 > max_query_time:
                        max_query_time = query['timespan']['diff'] * 1000
        else:
            queries_count = len(queries)
            for query in queries:
                if query['timespan']['diff'] * 1000 > max_query_time:
                    max_query_time = query['timespan']['diff'] * 1000

        print('\n\n')
        print('    STATICS:')
        print('    ______')
        print('    |')
        print('    | Queries Count     | -> ' + str(queries_count))
        print('    | Max Query Time    | -> ' + str(round(max_query_time, 2)) + ' ms')
        print('    |')
