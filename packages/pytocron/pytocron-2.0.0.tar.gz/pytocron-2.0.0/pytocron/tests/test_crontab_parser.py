# Copyright (c) 2025 Sebastian Pipping <sebastian@pipping.org>
#
# Licensed under GNU Affero General Public License v3.0 or later
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import itertools
from io import StringIO
from textwrap import dedent
from unittest import TestCase

import pytz
from parameterized import parameterized

from .._crontab_parser import (
    _NAMED_FREQUENCY,
    CrontabEntry,
    _frequency_seven,
    _parse_crontab_line,
    iterate_crontab_entries,
)


class ParseCrontabLineTest(TestCase):
    @parameterized.expand(
        [
            (
                "1 2 3 4 5 6 1970 1 2 3",
                _frequency_seven("1 2 3 4 5 6 1970"),
            ),
            (
                "1 2 3 4 5 6 1970 1 2 3",
                _frequency_seven("1 2 3 4 5 6 1970"),
            ),
            (
                "@annually 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["annually"]),
            ),
            (
                "@daily 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["daily"]),
            ),
            (
                "@hourly 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["hourly"]),
            ),
            (
                "@midnight 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["midnight"]),
            ),
            (
                "@minutely 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["minutely"]),
            ),
            (
                "@monthly 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["monthly"]),
            ),
            (
                "@secondly 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["secondly"]),
            ),
            (
                "@weekly 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["weekly"]),
            ),
            (
                "@yearly 1 2 3",
                _frequency_seven(_NAMED_FREQUENCY["yearly"]),
            ),
        ],
    )
    def test_good(self, contrab_line, expected_frequency):
        actual_frequency, actual_command = _parse_crontab_line(contrab_line)
        self.assertEqual(actual_frequency.expressions, expected_frequency.expressions)
        self.assertEqual(actual_command, "1 2 3")


class IterateCrontabEntriesTest(TestCase):
    def test_good(self):
        content = dedent(
            """\
            1 1 1 1 1 1 1970 one

            # With comment
            2 2 2 2 2 2 1970 two

            # With comment and hc-ping:
            # hc-ping: https://hc-ping.com/00000000-0000-0000-0000-000000000000
            3 3 3 3 3 3 1970 three

            # With comment, no hc-ping
            4 4 4 4 4 4 1970 four
        """,
        )
        expected_entries = [
            CrontabEntry(
                frequency=_frequency_seven("1 1 1 1 1 1 1970"),
                command="one",
                hc_ping_url=None,
            ),
            CrontabEntry(
                frequency=_frequency_seven("2 2 2 2 2 2 1970"),
                command="two",
                hc_ping_url=None,
            ),
            CrontabEntry(
                frequency=_frequency_seven("3 3 3 3 3 3 1970"),
                command="three",
                hc_ping_url="https://hc-ping.com/00000000-0000-0000-0000-000000000000",
            ),
            CrontabEntry(
                frequency=_frequency_seven("4 4 4 4 4 4 1970"),
                command="four",
                hc_ping_url=None,
            ),
        ]
        actual_entries = list(iterate_crontab_entries(StringIO(content)))
        self.assertEqual(actual_entries, expected_entries)


class FrequencySevenDaylightSavingTest(TestCase):
    berlin_time_zone = pytz.timezone("Europe/Berlin")
    start_time = datetime.datetime(2025, 1, 1).astimezone(
        berlin_time_zone,
    )  # i.e. anything localized from before the first hit

    def test_forwards(self):
        # 2025-03-30 02:00 -> 03:00
        frequency_str = "0 0 * 30 3 * 2025"
        expected_isoformats = [
            "2025-03-30T00:00:00+01:00",
            "2025-03-30T01:00:00+01:00",
            "2025-03-30T03:00:00+02:00",
            "2025-03-30T04:00:00+02:00",
        ]

        actual_isoformats = [
            datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)
            .astimezone(self.berlin_time_zone)
            .isoformat()
            for epoch in itertools.islice(
                _frequency_seven(frequency_str, start_time=self.start_time),
                4,
            )
        ]

        self.assertEqual(actual_isoformats, expected_isoformats)

    def test_backwards(self):
        # 2025-10-26 03:00 -> 02:00
        frequency_str = "0 0 * 26 10 * 2025"
        expected_isoformats = [
            "2025-10-26T00:00:00+02:00",
            "2025-10-26T01:00:00+02:00",
            "2025-10-26T02:00:00+02:00",
            "2025-10-26T02:00:00+01:00",
        ]

        actual_isoformats = [
            datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)
            .astimezone(self.berlin_time_zone)
            .isoformat()
            for epoch in itertools.islice(
                _frequency_seven(frequency_str, start_time=self.start_time),
                4,
            )
        ]

        self.assertEqual(actual_isoformats, expected_isoformats)
