# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any

from qa.testing.utils.exception_utils import *


def should_swallow_exception():
    def trouble(p: Any) -> str:
        raise Exception("trouble")

    assert safely(lambda: trouble(7)).value_or("nada") == "nada"
