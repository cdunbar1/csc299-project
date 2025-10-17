import json
import os

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

def main():
    """Main function to run the task manager application."""
    tasks = load_tasks()

    print("Welcome to your Task Manager!")
    while True:
        print("\nCommands: add <description>, list, search <keyword>, quit")
        command = input("Enter command: ").strip().lower()
        parts = command.split(' ', 1) # Split only on the first space

        if parts[0] == 'add':
            if len(parts) > 1:
                add_task(tasks, parts[1])
            else:
                print("Usage: add <description>")
        elif parts[0] == 'list':
            list_tasks(tasks)
        elif parts[0] == 'search':
            if len(parts) > 1:
                search_tasks(tasks, parts[1])
            else:
                print("Usage: search <keyword>")
        elif parts[0] == 'quit':
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()