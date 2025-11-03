import json
import os
import argparse

TASKS_FILE = 'tasks.json'

def load_tasks():
    """Loads tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks, description):
    """Adds a new task to the list."""
    task_id = 1 if not tasks else max(task['id'] for task in tasks) + 1
    new_task = {'id': task_id, 'description': description, 'completed': False}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task {task_id} added: '{description}'")

def list_tasks(tasks):
    """Lists all tasks."""
    if not tasks:
        print("No tasks found.")
        return
    print("\n--- Your Tasks ---")
    for task in tasks:
        status = "[DONE]" if task.get('completed', False) else "[TODO]"
        print(f"{task['id']}. {status} {task['description']}")
    print("------------------")

def search_tasks(tasks, keyword):
    """Searches tasks by keyword in their description."""
    found_tasks = [task for task in tasks if keyword.lower() in task['description'].lower()]
    if not found_tasks:
        print(f"No tasks found matching '{keyword}'.")
        return
    print(f"\n--- Search Results for '{keyword}' ---")
    for task in found_tasks:
        status = "[DONE]" if task.get('completed', False) else "[TODO]"
        print(f"{task['id']}. {status} {task['description']}")
    print("-----------------------------------")

def setup_parser():
    """Sets up the argument parser with subcommands for add, list, and search."""
    parser = argparse.ArgumentParser(description="Terminal Task Manager (TTM)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. ADD Subcommand
    parser_add = subparsers.add_parser("add", help="Add a new task.")
    parser_add.add_argument("description", type=str, help="The description of the new task.")

    # 2. LIST Subcommand
    subparsers.add_parser("list", help="List all current tasks.")

    # 3. SEARCH Subcommand
    parser_search = subparsers.add_parser("search", help="Search tasks by keyword.")
    parser_search.add_argument("keyword", type=str, help="The keyword to search for in task descriptions.")

    return parser

def main():
    """Parses arguments and calls the appropriate task function once."""
    parser = setup_parser()
    args = parser.parse_args()
    tasks= load_tasks()

    if args.command == "add":
        add_task(tasks, args.description)
    elif args.command == "list":
        list_tasks(tasks)
    elif args.command == "search":
        search_tasks(tasks, args.keyword)

if __name__ == "__main__":
    main()