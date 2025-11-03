# Tasks Prototype (tasks2)

## How to Run

1.  Ensure you have Python installed.
2.  Open your terminal or command prompt.
3.  Navigate to this `tasks2` directory:
    ```bash
    cd your/path/to/csc299-project/tasks2
    ```
4.  Run commands using the format:
    `python app.py <main_command> <sub_command> [options]`

## Features

1. **Add a High Priority Task:** `python app.py task add "Setup SQLite database" --priority high --due 2025-11-05`

2. **Add a Note:** `python app.py note add "SQLite Planning" --content "I plan to use SQLite for tasks2 as recommended."`

3. **List Tasks:** `python app.py task list --priority high`

4. **List Notes:** `python app.py note list`