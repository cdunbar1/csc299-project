import unittest
import os
import sqlite3
import time
from pkms_cli import DatabaseManager # Assuming pkms_cli is in the same directory

# Use a temporary database name for testing
TEST_DB_NAME = "test_pkms_data.db" 

class TestDatabaseManager(unittest.TestCase):
    """Unit tests for the DatabaseManager class."""

    def setUp(self):
        """Set up a fresh database before each test."""
        # Ensure the test DB is deleted if it exists from a previous run
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)
        # Initialize the DatabaseManager, which creates the test DB and tables
        self.db = DatabaseManager(TEST_DB_NAME)
        # Check connection is established
        self.assertIsNotNone(self.db.conn)

    def tearDown(self):
        """Clean up the database after each test."""
        self.db.close()
        # Delete the test database file
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

    # --- Task Tests ---

    def test_add_and_get_task(self):
        """Test adding a task and retrieving it."""
        task_id = self.db.add_task("Buy groceries", priority="High")
        self.assertIsNotNone(task_id)
        
        task = self.db.get_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task['description'], "Buy groceries")
        self.assertEqual(task['priority'], "High")
        self.assertEqual(task['status'], "Pending")

    def test_update_task_status(self):
        """Test updating a task's status."""
        task_id = self.db.add_task("Draft project plan")
        self.assertTrue(self.db.update_task_status(task_id, "Complete"))
        
        task = self.db.get_task(task_id)
        self.assertEqual(task['status'], "Complete")

    def test_delete_task(self):
        """Test deleting a task."""
        task_id = self.db.add_task("Task to be deleted")
        self.assertTrue(self.db.delete_task(task_id))
        self.assertIsNone(self.db.get_task(task_id))

    def test_list_tasks_filtering(self):
        """Test listing tasks with and without a status filter."""
        self.db.add_task("Pending task 1")
        self.db.add_task("Pending task 2")
        complete_id = self.db.add_task("Completed task")
        self.db.update_task_status(complete_id, "Complete")
        
        all_tasks = self.db.list_tasks()
        self.assertEqual(len(all_tasks), 3)

        pending_tasks = self.db.list_tasks(status="Pending")
        self.assertEqual(len(pending_tasks), 2)

    # --- Knowledge Tests ---
    
    def test_add_and_get_knowledge(self):
        """Test adding a knowledge entry and retrieving it."""
        note_id = self.db.add_knowledge("AI RAG", "Retrieval Augmented Generation is cool.", "AI, Research")
        self.assertIsNotNone(note_id)
        
        note = self.db.get_knowledge(note_id)
        self.assertIsNotNone(note)
        self.assertEqual(note['title'], "AI RAG")
        self.assertEqual(note['tags'], "AI, Research")

    def test_update_knowledge(self):
        """Test updating a knowledge entry."""
        note_id = self.db.add_knowledge("Old Title", "Old Content", "tag1")
        new_content = "New, better content."
        new_tags = "tag2, update"
        
        self.assertTrue(self.db.update_knowledge(note_id, "New Title", new_content, new_tags))
        
        note = self.db.get_knowledge(note_id)
        self.assertEqual(note['title'], "New Title")
        self.assertEqual(note['content'], new_content)
        self.assertEqual(note['tags'], new_tags)

    def test_search_knowledge(self):
        """Test searching knowledge by keywords."""
        self.db.add_knowledge("Python Classes", "A class is a blueprint for creating objects.", "coding, python")
        self.db.add_knowledge("SQLite Basics", "SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.", "database, sql")
        
        search_results = self.db.search_knowledge("sql")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]['title'], "SQLite Basics")
        
        search_results_2 = self.db.search_knowledge("object")
        self.assertEqual(len(search_results_2), 1)
        self.assertEqual(search_results_2[0]['title'], "Python Classes")

    def test_delete_knowledge(self):
        """Test deleting a knowledge note."""
        note_id = self.db.add_knowledge("Note to be deleted", "Delete me.", "trash")
        self.assertTrue(self.db.delete_knowledge(note_id))
        self.assertIsNone(self.db.get_knowledge(note_id))

# Instructions for running unit tests:
# 1. Ensure 'pkms_cli.py' is in the same directory.
# 2. Run from the terminal: python -m unittest test_pkms.py

if __name__ == '__main__':
    # Run the tests
    unittest.main()