import yaml
from pathlib import Path
from .utils import parse_time_str, format_minutes
from datetime import datetime
import os

BASE_PATH = os.getenv("TASK_TRACKER_BASE_PATH")

# Default YAML database path
yaml_path = Path(f"{BASE_PATH}{datetime.now().year}/{datetime.now().strftime("%d-%m-%Y.md")}")
print(yaml_path.as_posix())
def load_yaml(path=None):
    """Load the task database from the YAML file."""
    file = Path(path) if path else yaml_path
    if not file.exists():
        return {}
    with open(file, 'r') as f:
        return yaml.safe_load(f) or {}

def time_to_minutes(time_str):
    """Convert a time string like '15m' or '2h' to minutes."""
    if time_str.endswith('m'):
        return int(time_str[:-1])
    elif time_str.endswith('h'):
        return int(time_str[:-1]) * 60
    return 0

def save_yaml(data, path=None):
    """Save the task database to the YAML file."""
    file = Path(path) if path else yaml_path
    with open(file, 'w') as f:
        yaml.dump(data, f, sort_keys=False)


def update_task(group, task, time_spent, summary=None):
    """
    Updates or creates a task under a given group.
    Adds time and appends summary (if given) to a list.
    """
    data = load_yaml()

    if group not in data:
        data[group] = {}

    if 'dailyTasks' not in data[group]:
        data[group]['dailyTasks'] = {}

    task_data = data[group]['dailyTasks'].get(task, {"time": "0m", "summary": []})

    # Ensure summary is always a list
    if isinstance(task_data.get("summary"), str):
        task_data["summary"] = [task_data["summary"]]
    elif not isinstance(task_data.get("summary"), list):
        task_data["summary"] = []

    # Update time
    existing_time = time_to_minutes(task_data["time"])
    added_time = time_to_minutes(time_spent)
    total_time = existing_time + added_time
    task_data["time"] = f"{total_time}m"

    # Append new summary
    if summary:
      task_data["summary"].append(f"({datetime.now().strftime("%H:%M")}) {summary}")

    data[group]['dailyTasks'][task] = task_data
    save_yaml(data)
    return total_time

def list_tasks(group: str):
    """
    List all tasks under <group>/dailyTasks with time and summary.

    Returns:
        A dict mapping task names to {'time': ..., 'summary': ...}.
    """
    data = load_yaml()
    tasks = data.get(group, {}).get('dailyTasks', {})
    result = {}
    for name, entry in tasks.items():
        if isinstance(entry, dict):
            result[name] = {'time': entry.get('time'), 'summary': entry.get('summary')}
        else:
            result[name] = {'time': entry, 'summary': None}
    return result


def delete_task(group: str, task_name: str) -> bool:
    """
    Delete a task from <group>/dailyTasks.

    Returns:
        True if deleted, False otherwise.
    """
    data = load_yaml()
    tasks = data.get(group, {}).get('dailyTasks', {})

    if task_name in tasks:
        del tasks[task_name]
        save_yaml(data)
        return True
    return False
