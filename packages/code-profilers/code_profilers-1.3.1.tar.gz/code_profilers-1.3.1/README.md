# Introduction
This is a package for profiling your code, and use it to better understand what is happening in your code and debug better.
This is availale to use in any python code (no framework specific).


# Profilers
There is `Main Profiler` Which will register all profilers and responsible for handling issues and reporting info.

### Currently Supported Profilers
* MySQLProfiler

# Integrations
For the ease of development, we added some integrations which will take the `Main Profiler` and handle the integration with other frameworks.
Also you could use profilers without integrations, but you will write more code.


### Currently Supported Integrations
* Flask
    * It is used for integrating profilers with flask with only few code


# Examples
This is an example for using MySQL Profiler With Flask
```python
from flask import Flask

from code_profilers.main_profiler import MainProfiler
from code_profilers.profilers.mysql.profiler import MySQLProfiler
from code_profilers.integrations.flask import FlaskIntegration

app = Flask(__name__)

profiler = MainProfiler()
profiler.register_profiler(MySQLProfiler())
FlaskIntegration(app, profiler)
```
Then you are ready to go and test your code
