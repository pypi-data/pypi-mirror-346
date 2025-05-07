"""
Todo module for handling todo items.
"""
import json
import uuid
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

class Todo:
    """Class representing a todo item."""
    
    def __init__(
        self,
        title: str,
        details: str = "",
        due_date: Optional[Union[datetime, date, str]] = None,
        estimated_time: Optional[str] = None,
        status: str = "pending",
        todo_id: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
        updated_at: Optional[Union[datetime, str]] = None
    ):
        self.title = str(title) if title is not None else "Untitled"
        self.details = str(details) if details is not None else ""
        
        # Handle due_date
        self.due_date = None
        if due_date is not None:
            if isinstance(due_date, (datetime, date)):
                self.due_date = due_date
            else:
                # Try to parse from string
                try:
                    from dateutil import parser
                    self.due_date = parser.parse(str(due_date))
                except Exception:
                    pass
        
        self.estimated_time = str(estimated_time) if estimated_time is not None else None
        self.status = str(status) if status is not None else "pending"
        self.id = str(todo_id) if todo_id is not None else str(uuid.uuid4())
        
        # Handle timestamps
        if created_at is None:
            self.created_at = datetime.now()
        elif isinstance(created_at, datetime):
            self.created_at = created_at
        else:
            try:
                from dateutil import parser
                self.created_at = parser.parse(str(created_at))
            except Exception:
                self.created_at = datetime.now()
                
        if updated_at is None:
            self.updated_at = datetime.now()
        elif isinstance(updated_at, datetime):
            self.updated_at = updated_at
        else:
            try:
                from dateutil import parser
                self.updated_at = parser.parse(str(updated_at))
            except Exception:
                self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert todo to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "estimated_time": self.estimated_time,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Todo":
        """Create todo from dictionary."""
        return cls(
            title=data.get("title", "Untitled"),
            details=data.get("details", ""),
            due_date=data.get("due_date"),
            estimated_time=data.get("estimated_time"),
            status=data.get("status", "pending"),
            todo_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def update(self, **kwargs):
        """Update todo attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()


class TodoStore:
    """Class for storing and retrieving todos."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize todo storage."""
        # Create todo storage directory within the trackle store
        if data_dir is None:
            self.data_dir = Path.home() / "trackle" / "todos"
        else:
            self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.todos_file = self.data_dir / "todos.json"
        self.todos = []
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize the todo store."""
        if self.todos_file.exists():
            self._load_todos()
        else:
            # Create an empty todos file
            self.todos = []
            self._save_todos()
    
    def _load_todos(self):
        """Load todos from file."""
        try:
            with open(self.todos_file, "r") as f:
                data = json.load(f)
            self.todos = [Todo.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading todos: {str(e)}")
            self.todos = []
    
    def _save_todos(self):
        """Save todos to file."""
        data = [todo.to_dict() for todo in self.todos]
        with open(self.todos_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def create_todo(self, **kwargs) -> Todo:
        """Create a new todo."""
        todo = Todo(**kwargs)
        self.todos.append(todo)
        self._save_todos()
        return todo
    
    def get_todo(self, todo_id: str) -> Optional[Todo]:
        """Get a todo by ID."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None
    
    def get_all_todos(self) -> List[Todo]:
        """Get all todos."""
        return self.todos
    
    def update_todo(self, todo_id: str, **kwargs) -> Optional[Todo]:
        """Update a todo."""
        todo = self.get_todo(todo_id)
        if todo:
            todo.update(**kwargs)
            self._save_todos()
            return todo
        return None
    
    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo."""
        todo = self.get_todo(todo_id)
        if todo:
            self.todos.remove(todo)
            self._save_todos()
            return True
        return False
    
    def get_todos_by_status(self, status: str) -> List[Todo]:
        """Get todos filtered by status."""
        return [todo for todo in self.todos if todo.status == status]
    
    def get_todos_by_date(self, target_date: date) -> List[Todo]:
        """Get todos due on a specific date."""
        result = []
        for todo in self.todos:
            if todo.due_date:
                # Convert to date if it's a datetime
                todo_date = todo.due_date.date() if isinstance(todo.due_date, datetime) else todo.due_date
                if todo_date == target_date:
                    result.append(todo)
        return result
    
    def get_todos_by_date_range(self, start_date: date, end_date: date) -> Dict[date, List[Todo]]:
        """Get todos in a date range, grouped by day."""
        result = {}
        current = start_date
        while current <= end_date:
            todos_for_day = self.get_todos_by_date(current)
            if todos_for_day:
                result[current] = todos_for_day
            current += timedelta(days=1)
        return result
    
    def parse_date(self, date_str: str) -> date:
        """
        Parse various date formats into a date object.
        
        Supported formats:
        - Natural language: "today", "tomorrow", "yesterday"
        - Short formats: "25-may", "5/25"
        - Full formats: "25-may-2025", "5/25/2025"
        """
        today = date.today()
        
        # Convert to string to handle potential OptionInfo objects from typer
        date_str = str(date_str)
        
        # Handle natural language
        date_str_lower = date_str.lower()
        if date_str_lower == "today":
            return today
        elif date_str_lower == "tomorrow":
            return today + timedelta(days=1)
        elif date_str_lower == "yesterday":
            return today - timedelta(days=1)
        elif date_str_lower == "this week":
            # Return the start of the week
            return today - timedelta(days=today.weekday())
        
        # Try various date formats with dateutil.parser
        try:
            from dateutil import parser
            date_obj = parser.parse(date_str, fuzzy=True)
            
            # If year wasn't specified, use current year
            if date_str_lower.find(str(date_obj.year)) == -1:
                date_obj = date_obj.replace(year=today.year)
                
            return date_obj.date()
        except Exception as e:
            raise ValueError(f"Could not parse date: {date_str}") from e
    
    def get_week_todos(self) -> Dict[date, List[Todo]]:
        """Get todos for the current week (Monday to Sunday)."""
        today = date.today()
        # Get the first day of the week (Monday)
        start_date = today - timedelta(days=today.weekday())
        # Get the last day of the week (Sunday)
        end_date = start_date + timedelta(days=6)
        return self.get_todos_by_date_range(start_date, end_date)