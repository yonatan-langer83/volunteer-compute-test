"""Tests for single-shift duration, formatting, and validation."""

from datetime import time

from pantry_shifts import Shift, format_shift, shift_hours, validate_shift


def test_same_day_hours():
    shift = Shift("Ada Lovelace", "sorter", time(9, 0), time(12, 30))
    assert shift_hours(shift) == 3.5


def test_format_shift_line():
    shift = Shift("Ada Lovelace", "sorter", time(9, 0), time(12, 30))
    assert format_shift(shift) == "Ada Lovelace | sorter | 09:00-12:30 (3.5h)"


def test_quarter_hour_shift_is_valid():
    shift = Shift("Sam Rivera-Cole", "intake", time(13, 0), time(13, 15))
    assert shift_hours(shift) == 0.25
    assert validate_shift(shift) == []


def test_eight_hours_is_allowed():
    shift = Shift("Sam Rivera-Cole", "driver", time(8, 0), time(16, 0))
    assert shift_hours(shift) == 8
    assert validate_shift(shift) == []


def test_rejects_blank_role_time_and_zero_length():
    shift = Shift(" ", "chef", time(9, 10), time(9, 10))
    assert validate_shift(shift) == [
        "volunteer name is required",
        "role must be one of: closer, driver, intake, sorter",
        "start and end must be on a 15-minute boundary",
        "shift must be longer than 0 hours",
    ]


def test_rejects_nonzero_seconds():
    shift = Shift("Ada Lovelace", "sorter", time(9, 0, 30), time(12, 0))
    assert validate_shift(shift) == [
        "start and end must be on a 15-minute boundary",
    ]


def test_rejects_overtime():
    shift = Shift("Ada Lovelace", "driver", time(8, 0), time(17, 0))
    assert shift_hours(shift) == 9
    assert validate_shift(shift) == ["shift must be at most 8 hours"]


def test_zero_length_is_zero_hours():
    shift = Shift("Ada Lovelace", "sorter", time(9, 0), time(9, 0))
    assert shift_hours(shift) == 0
    assert validate_shift(shift) == ["shift must be longer than 0 hours"]


def test_overnight_closer_is_four_hours():
    shift = Shift("Sam Rivera-Cole", "closer", time(21, 0), time(1, 0))
    assert shift_hours(shift) == 4.0
    assert validate_shift(shift) == []


def test_overnight_overtime_is_rejected():
    shift = Shift("Sam Rivera-Cole", "closer", time(21, 0), time(6, 0))
    assert shift_hours(shift) == 9.0
    assert validate_shift(shift) == ["shift must be at most 8 hours"]
