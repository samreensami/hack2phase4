
import os
from pathlib import Path

# ==============================================================================
# FILE CONTENTS
# ==============================================================================

# Using a dictionary to hold the content of each file to be created.
# This makes it easy to manage and extend.

files_content = {
    "src/models.py": """
from dataclasses import dataclass, field
import uuid

@dataclass
class Task:
    """Represents a single task in the to-do list."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    completed: bool = False

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{self.id[:6]}] {self.title} - {status}"
""",

    "src/services.py": """
from typing import Dict, List, Optional
from .models import Task

class TaskService:
    """
    In-memory service for CRUD operations on Tasks.
    This class holds the application's state.
    """
    _tasks: Dict[str, Task] = {}

    def create_task(self, title: str, description: str) -> Task:
        """Creates and stores a new task."""
        if not title:
            raise ValueError("Title cannot be empty.")
        
        new_task = Task(title=title, description=description)
        self._tasks[new_task.id] = new_task
        print(f"Task '{title}' created successfully.")
        return new_task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieves a task by its ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Returns a list of all tasks."""
        return list(self._tasks.values())

    def update_task(self, task_id: str, title: str, description: str) -> Optional[Task]:
        """Updates a task's title and description."""
        task = self.get_task(task_id)
        if task:
            task.title = title if title else task.title
            task.description = description if description else task.description
            print(f"Task '{task.title}' updated.")
            return task
        print(f"Error: Task with ID '{task_id}' not found.")
        return None

    def complete_task(self, task_id: str) -> Optional[Task]:
        """Marks a task as completed."""
        task = self.get_task(task_id)
        if task:
            task.completed = True
            print(f"Task '{task.title}' marked as complete.")
            return task
        print(f"Error: Task with ID '{task_id}' not found.")
        return None

    def delete_task(self, task_id: str) -> bool:
        """Deletes a task from memory."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            print(f"Task with ID '{task_id}' deleted.")
            return True
        print(f"Error: Task with ID '{task_id}' not found.")
        return False
""",

    "src/cli.py": """
from .services import TaskService

def display_menu():
    """Prints the main menu options to the console."""
    print("\n--- To-Do List CLI ---")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Delete a task")
    print("5. Exit")
    print("------------------------")

def run_cli():
    """The main loop for the command-line interface."""
    service = TaskService()
    
    # Pre-populate with some data for demonstration
    service.create_task("Project Setup", "Create the initial project structure.")
    service.create_task("Read Docs", "Read the project documentation.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            try:
                service.create_task(title, description)
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            tasks = service.get_all_tasks()
            if not tasks:
                print("\nNo tasks found.")
            else:
                print("\n--- All Tasks ---")
                for task in tasks:
                    print(task)
        
        elif choice == '3':
            task_id = input("Enter the ID of the task to complete: ")
            service.complete_task(task_id)

        elif choice == '4':
            task_id = input("Enter the ID of the task to delete: ")
            service.delete_task(task_id)

        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

",

    "main.py": """
import sys
from src.cli import run_cli

def main():
    """Main entry point for the application."""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
""",

    "CONSTITUTION.md": """
# Project Constitution

## Version 1.0.0

This document outlines the core principles and conventions governing this project. Adherence to these principles is mandatory for all contributions.

### 1. **Simplicity First**
- All code, architecture, and documentation should be as simple as possible, but no simpler. Avoid premature optimization and unnecessary complexity.

### 2. **In-Memory Data Store**
- The application must operate on an in-memory data model. No external databases, files, or persistent storage mechanisms are to be used unless explicitly approved as a core feature change.

### 3. **CLI-Centric Interface**
- The primary interface for this application is the command-line (CLI). All core functionality must be accessible and usable through the terminal.

### 4. **PEP 8 Compliance**
- All Python code must strictly adhere to the PEP 8 style guide. Code should be clean, readable, and consistent.

### 5. **Modularity and Separation of Concerns**
- **models.py**: Defines the data structures (the "nouns").
- **services.py**: Contains the business logic (the "verbs").
- **cli.py**: Handles user interaction and presentation.

### 6. **Testing**
- While not implemented in the initial build, all new features or bug fixes should ideally be accompanied by corresponding tests in the `/tests` directory.
""",

    "CLAUDE.md": """
# Claude Code & Spec-Kit Plus Integration

This file serves as a placeholder for integrating with external AI development tools like Claude Code and Spec-Kit Plus.

## Purpose
- To define prompts, specifications, and instructions that can be used by AI assistants to understand and extend the project.
- To maintain a context for AI-driven development, ensuring consistency with the project's constitution.

## Usage
When interacting with an AI, reference this file and the `CONSTITUTION.md` to provide the necessary context for generating code, documentation, or tests.
"""
}

# ==============================================================================
# SCRIPT LOGIC
# ==============================================================================

def build_project():
    """
    Main function to create the project structure, directories, and files.
    """
    print("Starting project build...")
    
    # --- 1. Create Directories ---
    # Define directories to be created.
    # Using Path objects for OS-agnostic paths.
    directories = [Path("src"), Path("tests")]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Directory created: {directory}/")
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            return # Exit if directory creation fails

    # --- 2. Create Files ---
    # Iterate over the dictionary and write content to each file.
    for file_path_str, content in files_content.items():
        file_path = Path(file_path_str)
        try:
            # The strip() removes leading/trailing whitespace from the content string.
            file_path.write_text(content.strip())
            print(f"File created: {file_path}")
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")

    print("\nProject build complete!")
    print("To run the application, execute: python main.py")

if __name__ == "__main__":
    build_project()
