# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Iterator

from qa.testing.utils.object_utils import Predicate


def process_next[T](i: Iterator[T], p: Predicate[T]) -> Iterator[T]:
    # DELETEME -- not needed so far
    """
    Processes next items per specified predicate. Useful, for cases in which
    first item in a stream decides the meaning of rest of items.

    Args:
        i (Iterator[T]): the iterator to process
        p (Predicate[T]): the predicate to be applied on `next(i)`

    Returns:
        Iterator[T]: the original iterator if the predicate evaluated true, \
            otherwise empty iterator
    """
    return i if p(next(i)) else iter([])
