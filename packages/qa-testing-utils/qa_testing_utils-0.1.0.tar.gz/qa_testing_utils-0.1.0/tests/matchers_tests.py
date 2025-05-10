# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from typing import Callable

import attr
import pytest
from functional import seq
from hamcrest import all_of, assert_that, has_item, has_property, is_  # type: ignore -- seq
from qa.testing.utils.string_utils import to_string
from qa.testing.utils.matchers import *
from qa.testing.utils.object_utils import *
from qa.testing.utils.string_utils import *


@to_string()
@attr.define  # provides semantic equality based on attribute values
class Foo(WithMixin):
    id: int = 8
    name: str = "kuku"


def should_match():
    # NOTE this is how a basic assertion framework would be implemented
    # luckily, we have PyHamcrest
    # https://github.com/hamcrest/PyHamcrest
    def asserter[T](actual: T, rule: Callable[[T], bool]):
        assert rule(actual)

    def is_[T](expected: T) -> Callable[[T], bool]:
        def matcher(actual: T) -> bool:
            return actual == expected
        return matcher

    def has_len(expected: int) -> Callable[[str], bool]:
        def matcher(actual: str) -> bool:
            return len(actual) == expected
        return matcher

    asserter("123456", has_len(6))
    asserter("123", is_("123"))
    # NOTE Foo is defined with semantic equality, hence this works
    asserter(Foo(), is_(Foo()))


def should_match_properties():
    assert_that(
        Foo(),
        all_of(
            has_property("id", 8),
            has_property("name", "kuku")))


def should_adapt_object():
    # NOTE: instead of assert_that(Foo().id, is_(8)), can use this:
    assert_that(Foo(), adapted_object(lambda foo: foo.id, is_(8)))


def should_have_item():
    assert_that([Foo(), Foo().with_(name="muku")],
                has_item(Foo().with_(name="muku")))


def should_adapt_sequence():
    # NOTE: instead of building full object, can adapt to specific field:
    assert_that([Foo(), Foo().with_(name="muku")],
                adapted_sequence(lambda foo: foo.name,  # type: ignore -- seq
                                 has_item(is_("muku"))))  # type: ignore -- seq


def should_match_item_in_iterator():
    assert_that(iter([Foo(), Foo().with_(name="muku")]),
                yields_item(Foo()))


def should_match_items_in_iterator():
    assert_that(iter([Foo(), Foo().with_(name="muku"), Foo().with_(
        name="kuku")]), yields_items([Foo().with_(name="muku"), Foo()]))


def should_match_all_in_iterator():
    assert_that(
        iter(
            [Foo(),
             Foo().with_(name="muku"),
             Foo().with_(name="kuku")]),
        yields_every(has_property("name")))


def should_adapt_iterator():
    assert_that(iter([Foo(), Foo().with_(name="muku")]), adapted_iterator(
        lambda foo: foo.name, yields_item(is_("muku"))))


def should_adapt_stream():
    '''
    Proves than iterators/streams are lazily consumed, in this case Foo(other)
    is not verified at all. If the items are yielded from a communication
    channel or file, it means skipping unnecessary items.
    '''
    assert_that(iter(seq([Foo(), Foo().with_(name="muku"),
                          Foo().with_(name="other")])
                     .peek(print)),   # type: ignore -- seq
                adapted_iterator(lambda foo: foo.name,  # type: ignore -- seq
                                 yields_item(is_("muku"))))


@pytest.mark.parametrize(
    "test_date, start_date, end_date",
    [
        (datetime(2023, 6, 15), datetime(2023, 1, 1), datetime(2023, 12, 31)),
        (datetime(2023, 6, 15), None, datetime(2023, 7, 1)),
        (datetime(2023, 6, 15), datetime(2023, 6, 1), None),
        (datetime(2023, 1, 1), datetime(2023, 1, 1), datetime(2023, 12, 31)),
        (datetime(2023, 12, 31), datetime(2023, 1, 1), datetime(2023, 12, 31)),
    ]
)
def should_match_within_dates(
        test_date: datetime, start_date: Union[datetime, None],
        end_date: Union[datetime, None]):
    assert_that(test_date, within_dates(start_date, end_date))


@pytest.mark.parametrize(
    "test_date, start_date, end_date",
    [
        (datetime(2022, 12, 31), datetime(2023, 1, 1), datetime(2023, 12, 31)),
        (datetime(2024, 1, 1), datetime(2023, 1, 1), datetime(2023, 12, 31)),
    ]
)
def should_fail_not_within_dates(
        test_date: datetime, start_date: Union[datetime, None],
        end_date: Union[datetime, None]):
    with pytest.raises(AssertionError):
        assert_that(test_date, within_dates(start_date, end_date))
