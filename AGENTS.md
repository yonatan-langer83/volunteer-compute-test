# Volunteering on Harbor Pantry

This repo is a test target for a volunteer compute broker. The work is posted as tasks in `volunteer-compute.yaml`. The project, not the volunteer, decides what to do. Claim one task, do that task, and open one pull request.

You are an AI agent (Claude, Gemini, Grok Bot, or any other MCP client). Follow these instructions on every task.

## Setup

Requires Python 3.11 or newer. From a clean checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

On the seed commit the suite exits 0. `test_overnight_closer_is_four_hours` is an expected failure (`xfail`, `strict=True`) until task `fix-overnight-hours` removes that marker. Leave the marker in place unless your task tells you to remove it.

GitHub Actions runs `python -m pytest` on every pull request. A green run is required.

## Coding style

Match the code already in `pantry_shifts/`.

- Python 3.11+, standard library only.
- 4-space indentation. Keep lines under 100 characters.
- Type hints on public functions. Use `list[str]` style, not `typing.List`.
- Prefer frozen dataclasses for new records.
- Names are `snake_case` for functions and `PascalCase` for classes.
- Tests live in `tests/`, are named `test_*`, and use plain pytest asserts. No fixtures unless the task asks for them.
- Comments explain a non-obvious rule. They do not narrate the change.

## One task, one pull request

- Complete exactly one task per pull request.
- Leave every other task untouched, including the overnight-hours bug when it is not your task.
- Edit only the files named in the task's `instructions`. A file not named there is out of scope, including this file and `volunteer-compute.yaml`.
- Add a dependency only when the task says to add that dependency. The seed uses pytest and the standard library.
- When a task lists `dependsOn`, those tasks are already merged. Use the functions they added. Do not reimplement them.

## Pull request format

Title:

```text
[task-id] short title
```

`task-id` is the task's `id` from `volunteer-compute.yaml`. Example: `[fix-overnight-hours] Count overnight shifts forward`.

Body, in this order:

1. Restate the task's acceptance criteria in your own words, completely enough that a reviewer can check the PR against them without opening the YAML.
2. A fenced block with the full output of `python -m pytest` from the branch you are submitting.

Keep the description about the task you did.
