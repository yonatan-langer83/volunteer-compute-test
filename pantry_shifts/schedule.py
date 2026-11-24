"""Schedule-level checks across a list of shifts."""

from __future__ import annotations

from pantry_shifts.shifts import Shift, validate_shift


def validate_schedule(shifts: list[Shift]) -> list[str]:
    """Validate each shift, numbered from 1 in input order.

    Each problem is prefixed with ``shift N:``. Overlap reporting is a
    separate task (``report-schedule-overlaps``) and is not done here.
    """
    problems: list[str] = []
    for index, shift in enumerate(shifts, start=1):
        for problem in validate_shift(shift):
            problems.append(f"shift {index}: {problem}")
    return problems
