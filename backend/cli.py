from services import TaskService

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
