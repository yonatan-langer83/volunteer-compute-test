"""Shift records, duration, formatting, and single-shift validation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time

MAX_SHIFT_HOURS = 8


@dataclass(frozen=True)
class Shift:
    """One volunteer working one role from ``start`` until ``end``."""

    volunteer: str
    role: str
    start: time
    end: time


def shift_hours(shift: Shift) -> float:
    """Return the shift length in hours.

    Intended rule: when ``end`` is earlier than ``start``, the shift runs
    past midnight and the length is the forward span across that boundary.
    A shift that starts and ends at the same clock time is zero hours long.

    Deliberate bug (task ``fix-overnight-hours``): a negative span is not
    wrapped forward. A closer who works 21:00-01:00 is reported as -20.0
    hours instead of 4.0. ``test_overnight_closer_is_four_hours`` covers
    this and is marked ``xfail`` so the suite stays green until the fix.
    """
    start_minutes = shift.start.hour * 60 + shift.start.minute
    end_minutes = shift.end.hour * 60 + shift.end.minute
    return (end_minutes - start_minutes) / 60.0


def format_shift(shift: Shift) -> str:
    """Return one whiteboard line. This does not validate the shift.

    Example: ``Ada Lovelace | sorter | 09:00-12:30 (3.5h)``.
    """
    hours = shift_hours(shift)
    start = shift.start.strftime("%H:%M")
    end = shift.end.strftime("%H:%M")
    return f"{shift.volunteer} | {shift.role} | {start}-{end} ({hours:.1f}h)"


def _on_quarter_hour(clock: time) -> bool:
    return clock.second == 0 and clock.microsecond == 0 and clock.minute % 15 == 0


def validate_shift(shift: Shift) -> list[str]:
    """Return problems with a single shift. An empty list means it is valid.

    A shift is valid when the volunteer name is non-empty after stripping
    whitespace, the role is one of the pantry roles, both clocks fall on a
    15-minute boundary with zero seconds, and the length is greater than 0
    hours and at most 8 hours.
    """
    allowed_roles = ("closer", "driver", "intake", "sorter")
    problems: list[str] = []

    if not shift.volunteer.strip():
        problems.append("volunteer name is required")

    if shift.role not in allowed_roles:
        problems.append("role must be one of: " + ", ".join(allowed_roles))

    if not _on_quarter_hour(shift.start) or not _on_quarter_hour(shift.end):
        problems.append("start and end must be on a 15-minute boundary")

    hours = shift_hours(shift)
    if hours <= 0:
        problems.append("shift must be longer than 0 hours")
    elif hours > MAX_SHIFT_HOURS:
        problems.append(f"shift must be at most {MAX_SHIFT_HOURS} hours")

    return problems
