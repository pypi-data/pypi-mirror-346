"""
Tests for the Todo module.
"""
import os
import json
import tempfile
import unittest
from datetime import datetime, date, timedelta
from pathlib import Path

from trackle.core.todo import Todo, TodoStore


class TestTodo(unittest.TestCase):
    """Test case for the Todo class."""
    
    def test_todo_init(self):
        """Test Todo initialization."""
        # Create a todo with minimal params
        todo = Todo(title="Test Todo")
        
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.details, "")
        self.assertIsNone(todo.due_date)
        self.assertIsNone(todo.estimated_time)
        self.assertEqual(todo.status, "pending")
        self.assertIsNotNone(todo.id)  # Should generate a UUID
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
        
        # Create a todo with all params
        due_date = datetime.now().date()
        todo = Todo(
            title="Test Todo",
            details="Test details",
            due_date=due_date,
            estimated_time="1h",
            status="in_progress",
            todo_id="test-id",
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 2)
        )
        
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.details, "Test details")
        self.assertEqual(todo.due_date, due_date)
        self.assertEqual(todo.estimated_time, "1h")
        self.assertEqual(todo.status, "in_progress")
        self.assertEqual(todo.id, "test-id")
        self.assertEqual(todo.created_at, datetime(2025, 1, 1))
        self.assertEqual(todo.updated_at, datetime(2025, 1, 2))
    
    def test_todo_to_dict(self):
        """Test converting Todo to dict."""
        due_date = datetime(2025, 5, 1).date()
        created_at = datetime(2025, 1, 1)
        updated_at = datetime(2025, 1, 2)
        
        todo = Todo(
            title="Test Todo",
            details="Test details",
            due_date=due_date,
            estimated_time="1h",
            status="in_progress",
            todo_id="test-id",
            created_at=created_at,
            updated_at=updated_at
        )
        
        todo_dict = todo.to_dict()
        
        self.assertEqual(todo_dict["id"], "test-id")
        self.assertEqual(todo_dict["title"], "Test Todo")
        self.assertEqual(todo_dict["details"], "Test details")
        self.assertEqual(todo_dict["due_date"], due_date.isoformat())
        self.assertEqual(todo_dict["estimated_time"], "1h")
        self.assertEqual(todo_dict["status"], "in_progress")
        self.assertEqual(todo_dict["created_at"], created_at.isoformat())
        self.assertEqual(todo_dict["updated_at"], updated_at.isoformat())
    
    def test_todo_from_dict(self):
        """Test creating Todo from dict."""
        due_date = date(2025, 5, 1)
        created_at = datetime(2025, 1, 1)
        updated_at = datetime(2025, 1, 2)
        
        todo_dict = {
            "id": "test-id",
            "title": "Test Todo",
            "details": "Test details",
            "due_date": due_date.isoformat(),
            "estimated_time": "1h",
            "status": "in_progress",
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        }
        
        todo = Todo.from_dict(todo_dict)
        
        self.assertEqual(todo.id, "test-id")
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.details, "Test details")
        self.assertTrue(isinstance(todo.due_date, datetime))
        self.assertEqual(todo.due_date.date(), due_date)
        self.assertEqual(todo.estimated_time, "1h")
        self.assertEqual(todo.status, "in_progress")
        self.assertTrue(isinstance(todo.created_at, datetime))
        self.assertTrue(isinstance(todo.updated_at, datetime))
    
    def test_todo_update(self):
        """Test updating Todo attributes."""
        todo = Todo(title="Test Todo")
        original_created_at = todo.created_at
        
        # Update some attributes
        todo.update(
            title="Updated Todo",
            details="New details",
            status="completed"
        )
        
        self.assertEqual(todo.title, "Updated Todo")
        self.assertEqual(todo.details, "New details")
        self.assertEqual(todo.status, "completed")
        self.assertEqual(todo.created_at, original_created_at)  # Created time shouldn't change
        self.assertNotEqual(todo.updated_at, original_created_at)  # Updated time should change


class TestTodoStore(unittest.TestCase):
    """Test case for the TodoStore class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for todos
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = TodoStore(Path(self.temp_dir.name))
    
    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()
    
    def test_create_todo(self):
        """Test creating a todo."""
        todo = self.store.create_todo(
            title="Test Todo",
            details="Test details",
            due_date=date(2025, 5, 1),
            estimated_time="1h"
        )
        
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(len(self.store.todos), 1)
        
        # Check that the todo was saved to file
        self.assertTrue(self.store.todos_file.exists())
        
        # Check file content
        with open(self.store.todos_file, "r") as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Todo")
    
    def test_get_todo(self):
        """Test getting a todo by ID."""
        todo = self.store.create_todo(title="Test Todo")
        
        retrieved_todo = self.store.get_todo(todo.id)
        self.assertEqual(retrieved_todo.title, "Test Todo")
        
        # Test with non-existent ID
        self.assertIsNone(self.store.get_todo("non-existent-id"))
    
    def test_get_all_todos(self):
        """Test getting all todos."""
        # Create some todos
        self.store.create_todo(title="Todo 1")
        self.store.create_todo(title="Todo 2")
        self.store.create_todo(title="Todo 3")
        
        todos = self.store.get_all_todos()
        self.assertEqual(len(todos), 3)
        self.assertEqual(todos[0].title, "Todo 1")
        self.assertEqual(todos[1].title, "Todo 2")
        self.assertEqual(todos[2].title, "Todo 3")
    
    def test_update_todo(self):
        """Test updating a todo."""
        todo = self.store.create_todo(title="Test Todo")
        
        # Update the todo
        updated_todo = self.store.update_todo(
            todo.id,
            title="Updated Todo",
            status="completed"
        )
        
        self.assertEqual(updated_todo.title, "Updated Todo")
        self.assertEqual(updated_todo.status, "completed")
        
        # Get the todo again to verify it was saved
        retrieved_todo = self.store.get_todo(todo.id)
        self.assertEqual(retrieved_todo.title, "Updated Todo")
        self.assertEqual(retrieved_todo.status, "completed")
        
        # Test with non-existent ID
        self.assertIsNone(self.store.update_todo("non-existent-id", title="New Title"))
    
    def test_delete_todo(self):
        """Test deleting a todo."""
        todo = self.store.create_todo(title="Test Todo")
        
        # Verify it exists
        self.assertEqual(len(self.store.todos), 1)
        
        # Delete it
        result = self.store.delete_todo(todo.id)
        self.assertTrue(result)
        
        # Verify it's gone
        self.assertEqual(len(self.store.todos), 0)
        self.assertIsNone(self.store.get_todo(todo.id))
        
        # Test with non-existent ID
        self.assertFalse(self.store.delete_todo("non-existent-id"))
    
    def test_get_todos_by_status(self):
        """Test getting todos by status."""
        # Create todos with different statuses
        self.store.create_todo(title="Todo 1", status="pending")
        self.store.create_todo(title="Todo 2", status="in_progress")
        self.store.create_todo(title="Todo 3", status="completed")
        self.store.create_todo(title="Todo 4", status="pending")
        
        # Get todos by status
        pending_todos = self.store.get_todos_by_status("pending")
        in_progress_todos = self.store.get_todos_by_status("in_progress")
        completed_todos = self.store.get_todos_by_status("completed")
        
        self.assertEqual(len(pending_todos), 2)
        self.assertEqual(len(in_progress_todos), 1)
        self.assertEqual(len(completed_todos), 1)
        
        # Check titles of pending todos
        pending_titles = [todo.title for todo in pending_todos]
        self.assertIn("Todo 1", pending_titles)
        self.assertIn("Todo 4", pending_titles)
    
    def test_get_todos_by_date(self):
        """Test getting todos by date."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        # Create todos with different dates
        self.store.create_todo(title="Today Todo", due_date=today)
        self.store.create_todo(title="Yesterday Todo", due_date=yesterday)
        self.store.create_todo(title="Tomorrow Todo", due_date=tomorrow)
        self.store.create_todo(title="Another Today Todo", due_date=today)
        
        # Get todos by date
        today_todos = self.store.get_todos_by_date(today)
        yesterday_todos = self.store.get_todos_by_date(yesterday)
        tomorrow_todos = self.store.get_todos_by_date(tomorrow)
        
        self.assertEqual(len(today_todos), 2)
        self.assertEqual(len(yesterday_todos), 1)
        self.assertEqual(len(tomorrow_todos), 1)
        
        # Check titles of today's todos
        today_titles = [todo.title for todo in today_todos]
        self.assertIn("Today Todo", today_titles)
        self.assertIn("Another Today Todo", today_titles)
    
    def test_get_todos_by_date_range(self):
        """Test getting todos by date range."""
        today = date.today()
        day1 = today - timedelta(days=1)
        day2 = today
        day3 = today + timedelta(days=1)
        day4 = today + timedelta(days=2)
        
        # Create todos with different dates
        self.store.create_todo(title="Day 1 Todo", due_date=day1)
        self.store.create_todo(title="Day 2 Todo", due_date=day2)
        self.store.create_todo(title="Day 3 Todo", due_date=day3)
        self.store.create_todo(title="Day 4 Todo", due_date=day4)
        
        # Get todos in range day1 to day3
        range_todos = self.store.get_todos_by_date_range(day1, day3)
        
        self.assertEqual(len(range_todos), 3)  # 3 dates with todos
        self.assertIn(day1, range_todos)
        self.assertIn(day2, range_todos)
        self.assertIn(day3, range_todos)
        
        # Check number of todos for each day
        self.assertEqual(len(range_todos[day1]), 1)
        self.assertEqual(len(range_todos[day2]), 1)
        self.assertEqual(len(range_todos[day3]), 1)
        
        # Check titles
        self.assertEqual(range_todos[day1][0].title, "Day 1 Todo")
        self.assertEqual(range_todos[day2][0].title, "Day 2 Todo")
        self.assertEqual(range_todos[day3][0].title, "Day 3 Todo")
    
    def test_parse_date(self):
        """Test date parsing."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        # Test natural language
        self.assertEqual(self.store.parse_date("today"), today)
        self.assertEqual(self.store.parse_date("tomorrow"), tomorrow)
        self.assertEqual(self.store.parse_date("yesterday"), yesterday)
        
        # Test specific date formats
        may_25 = date(today.year, 5, 25)
        self.assertEqual(self.store.parse_date("25-may").replace(year=today.year), may_25)
        self.assertEqual(self.store.parse_date("5/25").replace(year=today.year), may_25)
        
        # Test with year
        may_25_2025 = date(2025, 5, 25)
        self.assertEqual(self.store.parse_date("25-may-2025"), may_25_2025)
        self.assertEqual(self.store.parse_date("5/25/2025"), may_25_2025)
        
        # Test invalid date
        with self.assertRaises(ValueError):
            self.store.parse_date("invalid date")
    
    def test_get_week_todos(self):
        """Test getting todos for the current week."""
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        next_monday = monday + timedelta(days=7)
        
        # Create todos for the week
        self.store.create_todo(title="Monday Todo", due_date=monday)
        self.store.create_todo(title="Sunday Todo", due_date=sunday)
        self.store.create_todo(title="Today Todo", due_date=today)
        self.store.create_todo(title="Next Week Todo", due_date=next_monday)
        
        # Get this week's todos
        week_todos = self.store.get_week_todos()
        
        self.assertEqual(len(week_todos), 3)  # 3 dates with todos in this week
        self.assertIn(monday, week_todos)
        self.assertIn(today, week_todos)
        self.assertIn(sunday, week_todos)
        self.assertNotIn(next_monday, week_todos)
        
        # Check titles
        self.assertEqual(week_todos[monday][0].title, "Monday Todo")
        self.assertEqual(week_todos[today][0].title, "Today Todo")
        self.assertEqual(week_todos[sunday][0].title, "Sunday Todo")


if __name__ == "__main__":
    unittest.main()