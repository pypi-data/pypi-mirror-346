# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from functools import wraps
from typing import Callable, ParamSpec, Self, TypeVar

from qa.testing.utils.logger import *
from qa.testing.utils.string_utils import *


def should_trace():
    @to_string(show_static=True)
    class Message:
        value: str = "hello"
        id: int = 0

    @to_string()
    class Foo(LoggerMixin):
        @traced
        def run(self, message: Message) -> Self:
            self.log.debug(f"{message}")
            return self

    Foo().run(Message())


# see -- https://stackoverflow.com/questions/78891660/how-to-make-python-3-12-function-decorator-preserve-signature
def should_preserve_signature():
    P = ParamSpec('P')
    R = TypeVar('R')

    def my_decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        return wrapper

    @my_decorator
    def my_func(s: str):
        '''my documentation'''
        pass

    my_func("s")

    print(my_func.__name__)  # Prints: my_func
    print(my_func.__doc__)  # Prints: my documentation
