# tasks3/src/tasks3/app.py
import json
import os
import argparse
from datetime import datetime

# --- CONFIGURATION ---
TASKS_FILE = 'tasks.json'
NOTES_FILE = 'notes.json'
# NOTE: For this project iteration, we will use a MOCK_LLM_RESPONSE 
# instead of making a real API call.

# --- FILE HANDLING FUNCTIONS ---

def load_data(filename):
    """Loads data from a JSON file, handling non-existence and empty files."""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    """Saves data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# --- TASK MANAGEMENT FUNCTIONS ---

def handle_task_add(tasks, args):
    """Adds a new task with priority and due date."""
    task_id = 1 if not tasks else max(task['id'] for task in tasks) + 1
    
    # Validate date format (optional, but good practice)
    due_date_str = args.due_date if args.due_date else None
    if due_date_str and due_date_str.lower() != 'none':
        try:
            # Simple check: Does it look like a date?
            datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Error: Invalid due date format. Use YYYY-MM-DD.")
            return

    new_task = {
        'id': task_id,
        'description': args.description,
        'status': 'TODO',
        'priority': args.priority.upper(),
        'due_date': due_date_str,
        'linked_note_id': None 
    }
    tasks.append(new_task)
    save_data(TASKS_FILE, tasks)
    print(f"TASK {task_id} added successfully.")
    print(f"  Priority: {new_task['priority']}, Due: {new_task['due_date'] if new_task['due_date'] else 'None'}")

def handle_task_list(tasks, args):
    """Lists tasks with optional filtering."""
    filtered_tasks = tasks
    
    # Filtering logic (Notion-inspired)
    if args.status:
        filtered_tasks = [t for t in filtered_tasks if t['status'] == args.status.upper()]
    if args.priority:
        filtered_tasks = [t for t in filtered_tasks if t['priority'] == args.priority.upper()]

    if not filtered_tasks:
        print("No tasks found matching your criteria.")
        return
        
    print("\n--- Filtered Tasks ---")
    for task in filtered_tasks:
        status_display = f"[{task['status']}]"
        priority_display = f"({task['priority']})"
        due_display = f"Due: {task['due_date']}" if task['due_date'] else ""
        link_display = f"[Note {task['linked_note_id']}]" if task['linked_note_id'] else ""
        
        print(f"{task['id']}. {status_display} {priority_display} {due_display} {link_display} - {task['description']}")
    print("----------------------")


def handle_task_done(tasks, args):
    """Marks a task as DONE."""
    task_id = args.id
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'DONE'
            save_data(TASKS_FILE, tasks)
            print(f"Task {task_id} marked as DONE.")
            return
    print(f"Error: Task ID {task_id} not found.")


# --- KNOWLEDGE MANAGEMENT FUNCTIONS ---

def handle_note_add(notes, args):
    """Adds a new knowledge note (PKMS item)."""
    note_id = 1 if not notes else max(note['id'] for note in notes) + 1
    new_note = {
        'id': note_id,
        'title': args.title,
        'content': args.content, # For simplicity, content is taken as a single argument
        'created_date': datetime.now().strftime('%Y-%m-%d')
    }
    notes.append(new_note)
    save_data(NOTES_FILE, notes)
    print(f"NOTE {note_id} added: '{args.title}'")

def handle_note_list(notes, args):
    """Lists all knowledge note titles."""
    if not notes:
        print("No notes found.")
        return
    
    print("\n--- Knowledge Notes ---")
    for note in notes:
        print(f"NOTE {note['id']} ({note['created_date']}): {note['title']}")
    print("-----------------------")


# --- AI AGENT FUNCTIONS ---

def handle_agent_suggest(tasks, notes):
    """
    MOCK AI AGENT: Analyzes tasks and notes to provide a smart suggestion.
    In a real system, this would call a Gemini/Claude/etc. API.
    """
    print("\n--- AI Contextual Planner Agent ---")
    
    # 1. Identify high-priority, incomplete tasks
    critical_tasks = [t for t in tasks if t['priority'] == 'HIGH' and t['status'] != 'DONE']
    
    if not critical_tasks:
        print("All critical tasks are complete. Focus on MEDIUM priority or add new tasks.")
        return
        
    # 2. Select the most critical task (e.g., the one with the earliest due date, or just the first one)
    target_task = critical_tasks[0]
    
    # 3. Find any linked knowledge (Mocking the linked data, since linking wasn't implemented yet)
    MOCK_LLM_RESPONSE = f"""
    Based on Task ID {target_task['id']} ('{target_task['description']}') which is due soon, 
    the best next step is to **Structure the `agent suggest` function and implement the core mocking logic**. 
    
    *Self-Correction: Note that the tasks are not explicitly linked to knowledge yet, so the immediate next task is implementation.*
    """
    
    # In a real scenario, the LLM API call would happen here.
    print(f"Analyzing {len(critical_tasks)} critical tasks and {len(notes)} notes...")
    print("\n[AGENT SUGGESTION]")
    print(MOCK_LLM_RESPONSE.strip())
    print("\n-----------------------------------")


# --- ARGPARSE SETUP (Refactored for Nested Commands) ---

def setup_parser():
    parser = argparse.ArgumentParser(
        description="Integrated PKMS and Task Manager (Tasks2 Iteration)"
    )
    # The top-level commands are 'task', 'note', and 'agent'
    main_subparsers = parser.add_subparsers(dest="main_command", required=True)

    # ----------------------------------------------------
    # 1. TASK TOP-LEVEL COMMAND 
    # ----------------------------------------------------
    task_parser = main_subparsers.add_parser("task", help="Manage tasks (todos).")
    task_subparsers = task_parser.add_subparsers(dest="task_command", required=True)

    # task add [description] --priority [level] --due [date]
    parser_task_add = task_subparsers.add_parser("add", help="Add a new task.")
    parser_task_add.add_argument("description", type=str, help="The description of the new task.")
    parser_task_add.add_argument("--priority", default="medium", choices=["low", "medium", "high"], help="Set task priority.")
    parser_task_add.add_argument("--due", dest="due_date", help="Set due date (YYYY-MM-DD).")
    parser_task_add.set_defaults(func=handle_task_add)
    
    # task list [--status STATUS] [--priority PRIORITY]
    parser_task_list = task_subparsers.add_parser("list", help="List and filter tasks.")
    parser_task_list.add_argument("--status", choices=["todo", "in-progress", "done"], help="Filter by status.")
    parser_task_list.add_argument("--priority", choices=["low", "medium", "high"], help="Filter by priority.")
    parser_task_list.set_defaults(func=handle_task_list)

    # task done [id]
    parser_task_done = task_subparsers.add_parser("done", help="Mark a task as completed.")
    parser_task_done.add_argument("id", type=int, help="ID of the task to mark done.")
    parser_task_done.set_defaults(func=handle_task_done)

    # ----------------------------------------------------
    # 2. NOTE TOP-LEVEL COMMAND (PKMS) 
    # ----------------------------------------------------
    note_parser = main_subparsers.add_parser("note", help="Manage knowledge notes (PKMS).")
    note_subparsers = note_parser.add_subparsers(dest="note_command", required=True)

    # note add [title] --content [text]
    parser_note_add = note_subparsers.add_parser("add", help="Add a new note/knowledge item.")
    parser_note_add.add_argument("title", type=str, help="The title of the note.")
    parser_note_add.add_argument("--content", default="", help="The content of the note.")
    parser_note_add.set_defaults(func=handle_note_add)

    # note list
    parser_note_list = note_subparsers.add_parser("list", help="List all note titles.")
    parser_note_list.set_defaults(func=handle_note_list)
    
    # ----------------------------------------------------
    # 3. AGENT TOP-LEVEL COMMAND
    # ----------------------------------------------------
    agent_parser = main_subparsers.add_parser("agent", help="Run AI-powered analysis and planning steps.")
    agent_subparsers = agent_parser.add_subparsers(dest="agent_command", required=True)

    # agent suggest (The AI logic)
    parser_agent_suggest = agent_subparsers.add_parser("suggest", help="Get AI suggestion for the next highest-priority action.")
    # Note: We use a lambda to pass the tasks and notes data into the handler function
    parser_agent_suggest.set_defaults(func=lambda tasks, notes, args: handle_agent_suggest(tasks, notes))

    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    # Load all data needed for the entire system
    tasks = load_data(TASKS_FILE)
    notes = load_data(NOTES_FILE)
    
    # Dispatch the call to the appropriate handler function
    if args.main_command == 'task':
        args.func(tasks, args)
    elif args.main_command == 'note':
        args.func(notes, args)
    elif args.main_command == 'agent':
        # The agent handler needs both tasks and notes lists
        args.func(tasks, notes, args)

if __name__ == "__main__":
    main()