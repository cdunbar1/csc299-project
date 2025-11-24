import sqlite3
import os
import cmd
import time
import textwrap
from openai import OpenAI, OpenAIError

# --- Global Configuration ---
DB_NAME = "pkms_data.db"
APP_NAME = "AI-PKMS-CLI"

# --- 1. Database Management ---

class DatabaseManager:
    """Handles all SQLite database operations."""
    def __init__(self, db_path):
        self.conn = None
        self.db_path = db_path
        self._connect()
        self._create_tables()

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            # Use check_same_thread=False for potential multi-threading, 
            # though for a CLI this is usually fine.
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def _create_tables(self):
        """Creates the necessary tables if they do not exist."""
        if not self.conn: return

        cursor = self.conn.cursor()
        
        # Knowledge Management Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                created_at TEXT NOT NULL
            )
        """)

        # Task Management Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                priority TEXT,
                status TEXT NOT NULL,
                due_date TEXT,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    # --- Task Methods ---

    def add_task(self, description, priority="Medium", due_date="N/A"):
        """Adds a new task to the database."""
        if not self.conn: return
        created = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (description, priority, status, due_date, created_at) VALUES (?, ?, ?, ?, ?)",
                (description, priority, "Pending", due_date, created)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            return None

    def get_task(self, task_id):
        """Retrieves a single task by its ID."""
        if not self.conn: return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving task: {e}")
            return None

    def list_tasks(self, status=None):
        """Lists tasks, optionally filtered by status."""
        if not self.conn: return []
        try:
            cursor = self.conn.cursor()
            if status:
                cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error listing tasks: {e}")
            return []

    def update_task_status(self, task_id, status):
        """Updates the status of a specific task."""
        if not self.conn: return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating task status: {e}")
            return False

    def delete_task(self, task_id):
        """Deletes a task by its ID."""
        if not self.conn: return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False

    # --- PKMS Methods (Knowledge) ---
    
    def add_knowledge(self, title, content, tags=""):
        """Adds a new knowledge entry."""
        if not self.conn: return
        created = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO knowledge (title, content, tags, created_at) VALUES (?, ?, ?, ?)",
                (title, content, tags, created)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding knowledge: {e}")
            return None

    def get_knowledge(self, note_id):
        """Retrieves a single knowledge entry by its ID."""
        if not self.conn: return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM knowledge WHERE id = ?", (note_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving knowledge: {e}")
            return None

    def update_knowledge(self, note_id, title, content, tags):
        """Updates an existing knowledge entry."""
        if not self.conn: return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE knowledge SET title = ?, content = ?, tags = ? WHERE id = ?",
                (title, content, tags, note_id)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating knowledge: {e}")
            return False

    def delete_knowledge(self, note_id):
        """Deletes a knowledge entry by its ID."""
        if not self.conn: return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM knowledge WHERE id = ?", (note_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting knowledge: {e}")
            return False

    def search_knowledge(self, query):
        """Searches knowledge entries by title, content, or tags."""
        if not self.conn: return []
        try:
            cursor = self.conn.cursor()
            # Use LIKE for fuzzy searching across columns
            like_query = f"%{query}%"
            cursor.execute("""
                SELECT * FROM knowledge 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? 
                ORDER BY created_at DESC
            """, (like_query, like_query, like_query))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching knowledge: {e}")
            return []

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

# --- 2. AI Agent ---

class AIAgent:
    """Handles all interactions with the OpenAI API."""
    def __init__(self):
        # The OpenAI client automatically looks for the OPENAI_API_KEY environment variable.
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found. AI features will be disabled.")
            self.client = None
        else:
            try:
                self.client = OpenAI()
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.client = None

    def summarize_text(self, text, model="gpt-3.5-turbo"):
        """Sends text to the AI to generate a concise summary."""
        if not self.client:
            return "AI is disabled due to missing API key."

        prompt = (
            "You are a helpful task and knowledge assistant. "
            "Provide a concise, single-sentence summary of the following text: "
            f"'{text}'"
        )
        
        # Simple retry logic for API calls
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a concise summarization bot."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()
            except OpenAIError as e:
                print(f"OpenAI API Error (Attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt) # Exponential backoff
                else:
                    return "AI Summarization failed after multiple retries."
            except Exception as e:
                # Handle other exceptions (e.g., network issues)
                return f"An unexpected error occurred during AI call: {e}"
        return "AI Summarization failed."
    
    def suggest_tags(self, text, model="gpt-3.5-turbo"):
        """Sends text to the AI to suggest three comma-separated tags."""
        if not self.client:
            return "AI is disabled due to missing API key."

        prompt = (
            "Analyze the following knowledge content and suggest exactly three, "
            "comma-separated tags. Do not include any extra text, quotes, or numbering. "
            f"Content: '{text}'"
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a tag generation bot. Output only three comma-separated tags."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()
            except OpenAIError as e:
                print(f"OpenAI API Error (Attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return "AI Tagging failed after multiple retries."
            except Exception as e:
                return f"An unexpected error occurred during AI call: {e}"
        return "AI Tagging failed."


# --- 3. CLI Application ---

class PKMSApp(cmd.Cmd):
    """The main Command Line Interface application."""
    intro = f'\nWelcome to the {APP_NAME}. Type help or ? to list commands.\n'
    prompt = f'({APP_NAME}) > '

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(DB_NAME)
        self.ai_agent = AIAgent()

    def postloop(self):
        """Called after the command loop finishes."""
        self.db.close()
        print("Thank you for using the PKMS. Goodbye!")

    # --- Task Commands ---

    def do_add_task(self, arg):
        """add_task <description>\nAdds a new task. Priority/due date are set to default."""
        args = arg.split()
        if not args:
            print("Usage: add_task <description>")
            return

        description = " ".join(args)
        
        new_id = self.db.add_task(description)
        if new_id:
            print(f"Task '{description[:40]}...' added with ID: {new_id}")
        else:
            print("Failed to add task.")

    def do_list_tasks(self, arg):
        """list_tasks [status: Pending/Complete]\nLists all tasks, or only those matching status."""
        status_filter = arg.strip().capitalize() if arg else None
        tasks = self.db.list_tasks(status=status_filter)
        
        if not tasks:
            print(f"No {status_filter or ''} tasks found.")
            return

        print("\n--- Task List ---")
        for t in tasks:
            print(f"[ID: {t['id']:<3}] [Status: {t['status']:<10}] [Pri: {t['priority']:<6}] Due: {t['due_date']:<10} | {t['description']}")
        print("-----------------\n")

    def do_complete_task(self, arg):
        """complete_task <id>\nMarks a task as Complete."""
        try:
            task_id = int(arg.strip())
            if self.db.update_task_status(task_id, "Complete"):
                print(f"Task {task_id} marked as Complete.")
            else:
                print(f"Task {task_id} not found or update failed.")
        except ValueError:
            print("Invalid usage. Please provide a numeric task ID.")

    def do_delete_task(self, arg):
        """delete_task <id>\nDeletes a task permanently."""
        try:
            task_id = int(arg.strip())
            if self.db.delete_task(task_id):
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Task {task_id} not found or deletion failed.")
        except ValueError:
            print("Invalid usage. Please provide a numeric task ID.")


    # --- Knowledge Commands ---

    def do_add_note(self, arg):
        """add_note <title>\nAdds a new knowledge note. Will prompt for content and tags."""
        title = arg.strip()
        if not title:
            print("Usage: add_note <title>")
            return
        
        print(f"--- Entering content for: {title} ---")
        print("Type 'END' on a new line to finish entry.")
        content_lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                content_lines.append(line)
            except EOFError:
                break
        
        content = "\n".join(content_lines)
        tags = input("Enter comma-separated tags (e.g., ai, research, planning): ")
        
        new_id = self.db.add_knowledge(title, content, tags.strip())
        if new_id:
            print(f"Knowledge note '{title}' added with ID: {new_id}")
        else:
            print("Failed to add knowledge note.")

    def do_view_note(self, arg):
        """view_note <id>\nDisplays the full content of a knowledge note."""
        try:
            note_id = int(arg.strip())
        except ValueError:
            print("Invalid usage. Please provide a numeric note ID.")
            return
        
        note = self.db.get_knowledge(note_id)
        if not note:
            print(f"Note with ID {note_id} not found.")
            return

        print(f"\n--- Note ID: {note['id']} | Title: {note['title']} ---")
        print(f"Tags: {note['tags']}")
        print(f"Created: {note['created_at']}")
        print("-" * 50)
        # Use textwrap to format the content for better readability in the terminal
        print(textwrap.fill(note['content'], width=78)) 
        print("-" * 50)
        
    def do_edit_note(self, arg):
        """edit_note <id>\nEdits the title, content, and tags of an existing note."""
        try:
            note_id = int(arg.strip())
        except ValueError:
            print("Invalid usage. Please provide a numeric note ID.")
            return
        
        note = self.db.get_knowledge(note_id)
        if not note:
            print(f"Note with ID {note_id} not found.")
            return
        
        print(f"\n--- Editing Note ID: {note_id} ---")
        
        # 1. Edit Title
        new_title = input(f"New Title (Current: {note['title']}): ") or note['title']
        
        # 2. Edit Content (Using the END pattern)
        print("\n--- Editing Content (Type 'END' on a new line to save) ---")
        print("Current Content:\n" + textwrap.fill(note['content'], width=78))
        print("\nEnter New Content (or just 'END' to keep current content):")
        
        new_content_lines = []
        is_new_content = False
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                new_content_lines.append(line)
                is_new_content = True
            except EOFError:
                break
        
        new_content = "\n".join(new_content_lines) if is_new_content and new_content_lines else note['content']
        
        # 3. Edit Tags
        new_tags = input(f"\nNew Tags (Current: {note['tags']}): ") or note['tags']
        
        if self.db.update_knowledge(note_id, new_title, new_content, new_tags):
            print(f"\nNote {note_id} updated successfully.")
        else:
            print("\nNote update failed.")
            
    def do_delete_note(self, arg):
        """delete_note <id>\nDeletes a knowledge note permanently."""
        try:
            note_id = int(arg.strip())
            if self.db.delete_knowledge(note_id):
                print(f"Note {note_id} deleted successfully.")
            else:
                print(f"Note {note_id} not found or deletion failed.")
        except ValueError:
            print("Invalid usage. Please provide a numeric note ID.")

    def do_search_notes(self, arg):
        """search_notes <query>\nSearches knowledge notes by title, content, or tags."""
        query = arg.strip()
        if not query:
            print("Usage: search_notes <query>")
            return

        results = self.db.search_knowledge(query)
        
        if not results:
            print(f"No knowledge notes found matching '{query}'.")
            return
        
        print(f"\n--- Knowledge Search Results for '{query}' ---")
        for k in results:
            # Show the first line of content or a snippet
            snippet = k['content'].split('\n', 1)[0][:70].strip() or k['content'][:70]
            print(f"[ID: {k['id']:<3}] [Tags: {k['tags']:<20}] Title: {k['title']}")
            print(f"    Content Preview: {snippet}...")
        print("------------------------------------------\n")
        
    # --- AI Agent Commands ---

    def do_ai_summarize_task(self, arg):
        """ai_summarize_task <id>\nUses the AI to provide a summary of a task description."""
        if not self.ai_agent.client:
            print("AI features are disabled. Please set the OPENAI_API_KEY environment variable.")
            return

        try:
            task_id = int(arg.strip())
        except ValueError:
            print("Invalid usage. Please provide a numeric task ID.")
            return
        
        task = self.db.get_task(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"\n[Task ID: {task['id']}] Requesting AI summary for: '{task['description'][:60]}...'")
        
        # Call the AI Agent
        summary = self.ai_agent.summarize_text(task['description'])
        
        print("\n--- AI Summary ---")
        print(summary)
        print("------------------\n")
        
    def do_ai_tag_knowledge(self, arg):
        """ai_tag_knowledge <id>\nUses the AI to suggest tags for a knowledge note."""
        if not self.ai_agent.client:
            print("AI features are disabled. Please set the OPENAI_API_KEY environment variable.")
            return

        try:
            note_id = int(arg.strip())
        except ValueError:
            print("Invalid usage. Please provide a numeric note ID.")
            return
        
        note = self.db.get_knowledge(note_id)
        if not note:
            print(f"Note with ID {note_id} not found.")
            return

        print(f"\n[Note ID: {note['id']}] Requesting AI tag suggestions for: '{note['title']}'")
        
        # Call the AI Agent
        suggested_tags = self.ai_agent.suggest_tags(note['content'])
        
        print("\n--- AI Suggested Tags ---")
        print(f"Current Tags: {note['tags']}")
        print(f"Suggestions:  {suggested_tags}")
        print("---------------------------\n")

    # --- Utility Commands ---
    
    def do_quit(self, arg):
        """quit\nExit the application."""
        return True

    def do_exit(self, arg):
        """exit\nExit the application."""
        return True
        
    def help_add_task(self):
        print('\n'.join([
            'add_task <description>',
            'Adds a new task to the system. Priority is set to Medium.',
            'Example: add_task Finish the PKMS CLI project'
        ]))
        
# --- Main Execution ---

if __name__ == '__main__':
    # Initialize the application and start the command loop
    app = PKMSApp()
    try:
        app.cmdloop()
    except KeyboardInterrupt:
        app.postloop() # Ensure DB connection is closed cleanly

# Instructions for running:
# 1. Install OpenAI library: pip install openai
# 2. Set API Key: export OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
# 3. Run: python pkms_cli.py