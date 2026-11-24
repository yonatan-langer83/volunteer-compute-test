# Volunteering on Harbor Pantry

This repo is a test target for a volunteer compute broker. The work is posted as tasks in `volunteer-compute.yaml`. The project, not the volunteer, decides what to do. Claim one task through the volunteer MCP server, do that task, and hand back one diff with `submit_result`. You do not need a GitHub account: after a maintainer accepts your diff, the project's own workflow opens the pull request and credits your volunteer name.

You are an AI agent (Claude, Gemini, Grok Bot, or any other MCP client). Follow these instructions on every task.

## Setup

Requires Python 3.11 or newer and git. Start in an empty folder:

```bash
git clone https://github.com/yonatan-langer83/volunteer-compute-test
cd volunteer-compute-test
python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
```

On the seed commit the suite exits 0. `test_overnight_closer_is_four_hours` is an expected failure (`xfail`, `strict=True`) until task `fix-overnight-hours` removes that marker. Leave the marker in place unless your task tells you to remove it.

Before a pull request opens, the project's workflow applies your diff and runs `python -m pytest`. A diff that fails the tests is refused, so run them yourself first.

## Coding style

Match the code already in `pantry_shifts/`.

- Python 3.11+, standard library only.
- 4-space indentation. Keep lines under 100 characters.
- Type hints on public functions. Use `list[str]` style, not `typing.List`.
- Prefer frozen dataclasses for new records.
- Names are `snake_case` for functions and `PascalCase` for classes.
- Tests live in `tests/`, are named `test_*`, and use plain pytest asserts. No fixtures unless the task asks for them.
- Comments explain a non-obvious rule. They do not narrate the change.

## One task, one diff

- Complete exactly one task per submission.
- Leave every other task untouched, including the overnight-hours bug when it is not your task.
- Edit only the files in the task's `do` list. Everything else is out of scope, including this file, `volunteer-compute.yaml` and `.github/`.
- If the brief is unclear or contradicts itself, call `release_task` with the reason. Do not guess.
- Claims last 45 minutes for small tasks and 90 for medium. Call `keep_working` if you need longer.
- Add a dependency only when the task says to add that dependency. The seed uses pytest and the standard library.
- When a task lists `dependsOn`, those tasks are already merged. Use the functions they added. Do not reimplement them.

## Submission format

Call `submit_result` with:

- `patch`: the output of `git diff` from your checkout, covering only the files in `do`. New files must be included (`git add -N <file>` before `git diff`).
- `summary`, in this order:
  1. The task id and title, for example `[fix-overnight-hours] Count overnight shifts forward`.
  2. The task's acceptance criteria in your own words, completely enough that a reviewer can check the diff against them without opening the YAML.
  3. The full output of `python -m pytest` from your checkout.

Keep the summary about the task you did.
