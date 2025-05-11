import argparse
import logging
from . import manager
import traceback

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    parser = argparse.ArgumentParser(description="YAML Task Time Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add or update time for a task")
    add_parser.add_argument("path", help="Format: <group>/<task>")
    add_parser.add_argument("time", help="Time to add (e.g., 15m, 1h)")
  
    # Add to add_parser
    add_parser.add_argument("--summary", help="Optional task summary", default=None)

    # List command
    list_parser = subparsers.add_parser("list", help="List all dailyTasks in a group")
    list_parser.add_argument("group", help="Group name (e.g., 'a', 'b')")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task from a group")
    delete_parser.add_argument("path", help="Format: <group>/<task>")

    args = parser.parse_args()

    try:
        if args.command == "add":
            group, task = args.path.split("/")
            total = manager.update_task(group, task, args.time, summary=args.summary)
            logging.info(f"✅ '{task}' updated to {total} minutes in group '{group}'.")

        elif args.command == "list":
            tasks = manager.list_tasks(args.group)
            if tasks:
                for name, info in tasks.items():
                    print(f"- {name}: {info['time']}", end="")
                    if info.get("summary"):
                        print(f" — {info['summary']}")
                    else:
                        print()

        elif args.command == "delete":
            group, task = args.path.split("/")
            success = manager.delete_task(group, task)
            if success:
                logging.info(f"🗑️ '{task}' deleted from group '{group}'.")
            else:
                logging.warning(f"⚠️ Task '{task}' not found in group '{group}'.")
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        print(traceback.format_exc())
