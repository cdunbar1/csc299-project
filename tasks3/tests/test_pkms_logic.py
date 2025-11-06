# tasks3/tests/test_pkms_logic.py
from tasks3.app import handle_task_add, handle_task_done 
from unittest.mock import MagicMock

# The handle_task_add function modifies a list in-place and calls save_data.
# We must mock save_data to stop it from touching the disk.

def test_add_task_structure_and_id(mocker):
    """Test that handle_task_add correctly increments ID and sets defaults."""
    # 1. Mock the save_data function to prevent writing to disk
    mocker.patch('tasks3.src.app.save_data')
    
    mock_tasks = [{'id': 1, 'description': 'Existing task', 'status': 'TODO'}]
    mock_args = MagicMock(description="Test task", priority='high', due_date='2025-12-01')
    
    handle_task_add(mock_tasks, mock_args)
    
    # Check that the list grew and the ID is correct
    assert len(mock_tasks) == 2
    assert mock_tasks[-1]['id'] == 2
    assert mock_tasks[-1]['priority'] == 'HIGH'

def test_task_done_status_update(mocker):
    """Test that handle_task_done correctly sets status to 'DONE'."""
    # 1. Mock the save_data function to prevent writing to disk
    mocker.patch('tasks3.src.app.save_data')
    
    # 2. Setup task list with one task to be completed (ID 5)
    mock_tasks = [{'id': 5, 'description': 'To be completed', 'status': 'TODO'}]
    mock_args = MagicMock(id=5)

    handle_task_done(mock_tasks, mock_args)
    
    # 3. Check that the task status was updated
    assert mock_tasks[0]['status'] == 'DONE'