# TaskTrack

**TaskTrack** is a simple YAML-based task time tracker for grouping daily tasks under named categories. It provides a command-line interface to add, list, and delete tasks with time accumulation and optional summaries.

## Features

* ✅ Add or update time on a task under a specific group
* ✅ Store tasks under `dailyTasks` in the YAML backend
* ✅ Optional summaries for each task
* ✅ List all tasks for a group, showing time and summary
* ✅ Delete tasks
* 📦 Installable as a Python package with a `tasktrack` CLI
* 🧪 Unit-tested with pytest, with isolated I/O fixtures

## Installation

```bash
# Clone the repo
git clone https://github.com/yourname/tasktrack.git
cd tasktrack

# Install in editable mode
pip install -e .
```

## Project Structure

```
tasktrack/               # Project root
├── task_tracker/         # Package directory
│   ├── __init__.py       # Package marker
│   ├── cli.py            # CLI entry point
│   ├── manager.py        # Core logic (load, save, update, list, delete)
│   ├── utils.py          # Time parsing/formatting helpers
│   └── tasks.yaml        # YAML backend (created on first run)
├── tests/                # Pytest test suite
│   └── test_manager.py   # Unit tests with I/O patching
├── pyproject.toml        # Build metadata and CLI entry point
└── README.md             # This file
```

## Usage

Once installed, you can run the `tasktrack` command from anywhere.

### Add or update a task

```bash
tasktrack add <group>/<task> <time> [--summary "Your summary"]
```

* `<group>`: e.g. `a`, `b`, etc.
* `<task>`: the task name (no spaces recommended)
* `<time>`: time to add, in minutes (`Xm`) or hours (`Xh`)
* `--summary`: optional summary string

**Example:**

```bash
tasktrack add a/testtask 15m --summary "Refactored manager logic"
```

### List tasks in a group

```bash
tasktrack list <group>
```

**Example:**

```bash
tasktrack list a
```

Output:

```
- testtask: 15m — Refactored manager logic
- other: 30m
```

### Delete a task

```bash
tasktrack delete <group>/<task>
```

**Example:**

```bash
tasktrack delete a/testtask
```

## Configuration

By default, the YAML database is stored in `task_tracker/tasks.yaml`. To override:

```bash
export TASK_TRACKER_DB=/path/to/custom_tasks.yaml
```

## Testing

Run the unit tests with:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: \`git commit -m "Add new feature"
4. Push to your branch: `git push origin feature/YourFeature`
5. Open a Pull Request

---

*Enjoy tracking your daily tasks!*

Give me the pure markdown version
