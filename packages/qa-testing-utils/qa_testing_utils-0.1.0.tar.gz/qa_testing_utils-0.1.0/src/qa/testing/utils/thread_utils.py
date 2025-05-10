# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import concurrent.futures
import time
from datetime import timedelta

COMMON_EXECUTOR = concurrent.futures.ThreadPoolExecutor()


def sleep_for(duration: timedelta):
    time.sleep(duration.total_seconds())
