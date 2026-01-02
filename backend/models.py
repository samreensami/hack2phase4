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
