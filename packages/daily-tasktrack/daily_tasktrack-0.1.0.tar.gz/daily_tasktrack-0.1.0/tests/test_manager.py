import pytest
import tempfile
import os
import yaml
import re

from task_tracker import manager

# Use your exact starting structure here, including dailyTasks → {"test": "30m"}
YAML_TEMPLATE = {
    "a": {
        "training": {},
        "dailyTasks": {
            "test": {"time": "30m", "summary": []}
        }
    },
    "b": {
        "training": {}
    },
    "personal": {
        "training": ["30 regular pushs"],
        "Arabic": ["Learned numbers from 20-100"]
    }
}

@pytest.fixture
def patch_yaml_io(tmp_path, monkeypatch):
    tmp_file = tmp_path / "tasks.yaml"
    with open(tmp_file, "w") as f:
        yaml.dump(YAML_TEMPLATE, f, sort_keys=False)

    def _load(path=None):
        with open(tmp_file) as f:
            return yaml.safe_load(f) or {}

    def _save(data, path=None):
        with open(tmp_file, "w") as f:
            yaml.dump(data, f, sort_keys=False)

    monkeypatch.setattr(manager, "load_yaml", _load)
    monkeypatch.setattr(manager, "save_yaml", _save)

    return tmp_file

def test_add_new_task(patch_yaml_io):
    minutes = manager.update_task("a", "newtask", "15m", summary="New work")
    assert minutes == 15

    data = manager.load_yaml()
    entry = data["a"]["dailyTasks"]["newtask"]
    assert entry["time"] == "15m"
    assert bool(re.search(r'\(\d\d:\d\d\) New work', entry["summary"][0]))

def test_update_existing_task(patch_yaml_io):
    updated = manager.update_task("a", "test", "10m", summary="Updated summary")
    assert updated == 40

    data = manager.load_yaml()
    task = data["a"]["dailyTasks"]["test"]
    assert task["time"] == "40m"
    assert bool(re.search(r'\(\d\d:\d\d\) Updated summary', task["summary"][0]))

def test_append_multiple_summaries(patch_yaml_io):
    # Add first summary
    manager.update_task("a", "test", "10m", summary="First summary")
    # Add second summary
    manager.update_task("a", "test", "5m", summary="Second summary")

    data = manager.load_yaml()
    task = data["a"]["dailyTasks"]["test"]
    assert bool(re.search(r'\(\d\d:\d\d\) First summary', task["summary"][0]))
    assert bool(re.search(r'\(\d\d:\d\d\) Second summary', task["summary"][1]))
