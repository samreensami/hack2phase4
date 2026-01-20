# MCP Tools: Task Management

**MCP SDK**: Official MCP SDK
**Feature**: AI Chatbot

This document defines the tools exposed via the MCP (Machine-Centric Protocol) server for the AI agent. These tools allow the agent to manage tasks on behalf of the user.

---

## Tool: `add_task`

Adds a new task to the user's list.

- **Arguments**:
  - `title` (string, required): The title of the task.
  - `description` (string, optional): A longer description of the task.
  - `category` (string, optional): A category to assign to the task (e.g., "Work", "Personal").
- **Returns**:
  - A dictionary object representing the newly created task, including its `id`, `title`, `description`, `status`, and `category`.
- **Example**:
  - Agent call: `add_task(title="Buy milk", category="Groceries")`
  - Result: `{ "id": 101, "title": "Buy milk", "description": null, "status": false, "category": "Groceries", ... }`

---

## Tool: `list_tasks`

Lists all tasks for the current user.

- **Arguments**:
  - `category` (string, optional): Filters tasks by a specific category.
  - `status` (string, optional): Filters tasks by status. Can be "complete" or "incomplete".
- **Returns**:
  - A list of task objects. If no tasks are found, returns an empty list.
- **Example**:
  - Agent call: `list_tasks(category="Work", status="incomplete")`
  - Result: `[{ "id": 102, "title": "Finish report", "status": false, "category": "Work", ... }]`

---

## Tool: `complete_task`

Marks one or more tasks as complete.

- **Arguments**:
  - `task_ids` (list[int], required): A list of task IDs to mark as complete.
- **Returns**:
  - A dictionary with a "status" key indicating success and a "completed_ids" key with the list of updated task IDs.
- **Example**:
  - Agent call: `complete_task(task_ids=[101, 102])`
  - Result: `{ "status": "success", "completed_ids": [101, 102] }`

---

## Tool: `delete_task`

Deletes one or more tasks.

- **Arguments**:
  - `task_ids` (list[int], required): A list of task IDs to delete.
- **Returns**:
  - A dictionary with a "status" key indicating success and a "deleted_ids" key with the list of deleted task IDs.
- **Example**:
  - Agent call: `delete_task(task_ids=[99])`
  - Result: `{ "status": "success", "deleted_ids": [99] }`

---

## Tool: `update_task`

Updates the details of a single task.

- **Arguments**:
  - `task_id` (int, required): The ID of the task to update.
  - `title` (string, optional): The new title for the task.
  - `description` (string, optional): The new description for the task.
  - `category` (string, optional): The new category for the task.
  - `status` (string, optional): The new status for the task ("complete" or "incomplete").
- **Returns**:
  - A dictionary object representing the updated task.
- **Example**:
  - Agent call: `update_task(task_id=102, title="Finish quarterly report", category="Urgent")`
  - Result: `{ "id": 102, "title": "Finish quarterly report", "description": "...", "status": false, "category": "Urgent", ... }`
