# Harbor Pantry shift board

Harbor Pantry is a fictional community food bank. `pantry_shifts` is a small Python package that formats volunteer shift lines and checks them against the pantry's scheduling rules: known roles, a 15-minute clock grid, and a maximum shift length.

This repository is a test target for a volunteer compute broker. Open-source projects, including nonprofits, post small tasks with clear instructions. Donors' AI agents (Claude, Gemini, Grok Bot, or any MCP client) claim one task at a time, do the work the project described, and hand back a diff. The project's workflow turns accepted diffs into pull requests. The tasks for this repo are in [`volunteer-compute.yaml`](volunteer-compute.yaml). Harbor Pantry is fictional, and this code is the broker's first test target.

## Known issue

`shift_hours` counts a shift that crosses midnight as a negative duration. A closer who works 21:00-01:00 is reported as -20.0 hours instead of 4.0. The bug is covered by `test_overnight_closer_is_four_hours`, marked `xfail` so the test run stays green until a volunteer fixes it. That fix is task `fix-overnight-hours`.

## Volunteer agents

Start here:

1. Connect to the volunteer MCP server and claim a task. The server only hands out tasks whose `dependsOn` tasks are done.
2. Read [`AGENTS.md`](AGENTS.md) and follow it for setup, coding style, and the submission format.
3. Do that task only, then submit your `git diff` with `submit_result`.

## Development

Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

The suite passes on this seed. `test_overnight_closer_is_four_hours` is an expected failure until `fix-overnight-hours` lands.
