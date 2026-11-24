"""Tests for schedule-level validation."""

from datetime import time

from pantry_shifts import Shift, validate_schedule


def test_empty_schedule():
    assert validate_schedule([]) == []


def test_valid_schedule():
    shifts = [
        Shift("Ada Lovelace", "sorter", time(9, 0), time(12, 0)),
        Shift("Grace Hopper", "driver", time(9, 0), time(12, 0)),
    ]
    assert validate_schedule(shifts) == []


def test_indexes_problems_from_one():
    shifts = [
        Shift("Ada Lovelace", "sorter", time(9, 0), time(12, 0)),
        Shift(" ", "chef", time(9, 10), time(9, 10)),
    ]
    problems = validate_schedule(shifts)
    assert problems
    assert all(item.startswith("shift 2: ") for item in problems)
