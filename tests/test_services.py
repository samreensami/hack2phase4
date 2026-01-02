import pytest
import sys
import os

# Add backend to the Python path for imports
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_dir)

from services import TaskService
from models import Task

@pytest.fixture
def task_service():
    """Provides a fresh TaskService instance for each test."""
    # Clear the _tasks dictionary to ensure test isolation
    TaskService._tasks = {} 
    return TaskService()

def test_create_task(task_service):
    """Test that tasks can be created correctly."""
    task = task_service.create_task("Test Task", "Description for test task")
    assert isinstance(task, Task)
    assert task.title == "Test Task"
    assert task.description == "Description for test task"
    assert not task.completed
    assert task.id in TaskService._tasks

    # Test creating a task with empty title
    with pytest.raises(ValueError, match="Title cannot be empty."):
        task_service.create_task("", "Invalid task")

def test_get_task(task_service):
    """Test retrieving a single task by ID."""
    task = task_service.create_task("Get Task", "Description for get task")
    retrieved_task = task_service.get_task(task.id)
    assert retrieved_task == task
    assert task_service.get_task("non-existent-id") is None

def test_get_all_tasks(task_service):
    """Test retrieving all tasks."""
    task_service.create_task("Task 1", "")
    task_service.create_task("Task 2", "")
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 2
    assert all(isinstance(t, Task) for t in tasks)

def test_update_task(task_service):
    """Test updating an existing task."""
    task = task_service.create_task("Original Title", "Original Description")
    
    # Update only title
    updated_task = task_service.update_task(task.id, "New Title", "")
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description" # Description unchanged

    # Update only description
    updated_task = task_service.update_task(task.id, "", "New Description")
    assert updated_task.title == "New Title" # Title unchanged
    assert updated_task.description == "New Description"

    # Update both
    updated_task = task_service.update_task(task.id, "Final Title", "Final Description")
    assert updated_task.title == "Final Title"
    assert updated_task.description == "Final Description"

    assert task_service.update_task("non-existent-id", "Title", "Desc") is None

def test_complete_task(task_service):
    """Test marking a task as complete."""
    task = task_service.create_task("Task to Complete", "")
    completed_task = task_service.complete_task(task.id)
    assert completed_task.completed
    assert task_service.complete_task("non-existent-id") is None

def test_delete_task(task_service):
    """Test deleting a task."""
    task = task_service.create_task("Task to Delete", "")
    assert task_service.delete_task(task.id) is True
    assert task_service.get_task(task.id) is None
    assert task_service.delete_task("non-existent-id") is False # Should return False for non-existent
