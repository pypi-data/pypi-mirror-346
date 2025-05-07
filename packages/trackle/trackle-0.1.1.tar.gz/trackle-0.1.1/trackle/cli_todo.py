"""
CLI commands for todo management.
"""
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from trackle.core.todo import Todo, TodoStore
from trackle.utils.editor import open_editor

app = typer.Typer(help="Todo management commands")
console = Console()

# Initialize store
store = TodoStore()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Start the interactive shell if no command is provided."""
    if ctx.invoked_subcommand is None:
        # Import here to avoid circular imports
        from trackle.todo_shell import run_interactive_shell
        run_interactive_shell()

@app.command("new")
def new_todo(
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Todo title"),
    due: Optional[str] = typer.Option(None, "--due", "-d", help="Due date (e.g., 'today', '25-may', '5/25/2025')"),
    time: Optional[str] = typer.Option(None, "--time", "-m", help="Estimated time (e.g., '1h', '30m')"),
    details: Optional[str] = typer.Option(None, "--details", "-e", help="Todo details"),
):
    """Create a new todo."""
    # Convert any Typer OptionInfo objects to actual values
    if hasattr(title, "default"):
        title = None
    if hasattr(due, "default"):
        due = None
    if hasattr(time, "default"):
        time = None
    if hasattr(details, "default"):
        details = None
        
    if title is None:
        title = typer.prompt("Title")
    
    # Handle due date
    due_date = None
    if due is None:
        due_input = typer.prompt("Due date (e.g., 'today', '25-may', '5/25/2025')", default="")
        if due_input:
            try:
                due_date = store.parse_date(due_input)
            except ValueError as e:
                console.print(f"[red]Error:[/red] {str(e)}")
                return
    else:
        try:
            due_date = store.parse_date(due)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {str(e)}")
            return
    
    # Handle estimated time
    estimated_time = None
    if time is None:
        time_input = typer.prompt("Estimated time (e.g., '1h', '30m')", default="")
        if time_input:
            estimated_time = time_input
    else:
        estimated_time = time
    
    # Handle details
    todo_details = ""
    if details is None:
        if typer.confirm("Add details?", default=False):
            initial_content = "Enter todo details here..."
            todo_details = open_editor(initial_content)
            if todo_details is None:
                todo_details = ""
    else:
        todo_details = details
    
    # Create todo
    todo = store.create_todo(
        title=title,
        details=todo_details,
        due_date=due_date,
        estimated_time=estimated_time
    )
    
    console.print(f"[green]Todo created:[/green] {todo.title}")
    if todo.due_date:
        date_str = todo.due_date.strftime("%Y-%m-%d") if hasattr(todo.due_date, "strftime") else str(todo.due_date)
        console.print(f"Due date: {date_str}")
    if todo.estimated_time:
        console.print(f"Estimated time: {todo.estimated_time}")


@app.command("list")
def list_todos(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (pending, in_progress, completed)"),
):
    """List all todos."""
    # Convert any Typer OptionInfo objects to actual values
    if hasattr(status, "default"):
        status = None
        
    todos = []
    if status:
        todos = store.get_todos_by_status(status)
        if not todos:
            console.print(f"No todos with status '[bold]{status}[/bold]'")
            return
    else:
        todos = store.get_all_todos()
        if not todos:
            console.print("No todos found.")
            return
    
    # Create a rich table for display
    table = Table(title="Todos")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Due Date", style="magenta")
    table.add_column("Status", style="blue")
    table.add_column("Est. Time", style="yellow")
    
    for todo in todos:
        # Get a shorter ID for display
        short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
        
        # Format due date
        due_date = ""
        if todo.due_date:
            due_date = todo.due_date.strftime("%Y-%m-%d") if hasattr(todo.due_date, "strftime") else str(todo.due_date)
            
            # Highlight due today or overdue
            today = date.today()
            if hasattr(todo.due_date, "date"):
                todo_date = todo.due_date.date()
            else:
                todo_date = todo.due_date
                
            if todo_date < today and todo.status != "completed":
                due_date = f"[bold red]{due_date}[/bold red]"
            elif todo_date == today and todo.status != "completed":
                due_date = f"[bold yellow]{due_date}[/bold yellow]"
        
        # Format status with color
        status_str = todo.status
        if status_str == "completed":
            status_str = f"[green]{status_str}[/green]"
        elif status_str == "in_progress":
            status_str = f"[blue]{status_str}[/blue]"
        elif status_str == "pending":
            status_str = f"[yellow]{status_str}[/yellow]"
        
        table.add_row(
            short_id,
            todo.title,
            due_date,
            status_str,
            todo.estimated_time or ""
        )
    
    console.print(table)


@app.command("view")
def view_todo(todo_id: str = typer.Argument(..., help="The ID of the todo to view")):
    """View details of a specific todo."""
    todo = store.get_todo(todo_id)
    
    # If not found with exact ID, try prefix match
    if todo is None:
        todos = store.get_all_todos()
        matching_todos = [t for t in todos if t.id.startswith(todo_id)]
        
        if len(matching_todos) == 1:
            todo = matching_todos[0]
        elif len(matching_todos) > 1:
            console.print(f"Multiple todos found matching '{todo_id}':")
            for t in matching_todos:
                console.print(f"- {t.id[:8]}: {t.title}")
            return
    
    if todo is None:
        console.print(f"[red]Todo with ID '{todo_id}' not found.[/red]")
        return
    
    # Format dates
    created_at = todo.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(todo.created_at, "strftime") else str(todo.created_at)
    updated_at = todo.updated_at.strftime("%Y-%m-%d %H:%M") if hasattr(todo.updated_at, "strftime") else str(todo.updated_at)
    due_date = ""
    if todo.due_date:
        due_date = todo.due_date.strftime("%Y-%m-%d") if hasattr(todo.due_date, "strftime") else str(todo.due_date)
    
    # Display todo with rich formatting
    console.print(f"# {todo.title}", style="bold green")
    console.print(f"Status: {todo.status}", style="blue")
    if due_date:
        console.print(f"Due date: {due_date}", style="magenta")
    if todo.estimated_time:
        console.print(f"Estimated time: {todo.estimated_time}", style="yellow")
    console.print(f"Created: {created_at}", style="dim")
    console.print(f"Updated: {updated_at}", style="dim")
    
    if todo.details:
        console.print("\n[bold]Details:[/bold]")
        console.print(todo.details)


@app.command("edit")
def edit_todo(todo_id: str = typer.Argument(..., help="The ID of the todo to edit")):
    """Edit a todo."""
    # Convert any Typer Argument objects to actual values
    if hasattr(todo_id, "default"):
        console.print(f"[red]Error:[/red] Todo ID is required.")
        return
        
    todo = store.get_todo(todo_id)
    
    # If not found with exact ID, try prefix match
    if todo is None:
        todos = store.get_all_todos()
        matching_todos = [t for t in todos if t.id.startswith(todo_id)]
        
        if len(matching_todos) == 1:
            todo = matching_todos[0]
        elif len(matching_todos) > 1:
            console.print(f"Multiple todos found matching '{todo_id}':")
            for t in matching_todos:
                console.print(f"- {t.id[:8]}: {t.title}")
            return
    
    if todo is None:
        console.print(f"[red]Todo with ID '{todo_id}' not found.[/red]")
        return
    
    # Edit fields
    console.print(f"Editing todo: {todo.title}")
    
    # Edit title
    new_title = typer.prompt("Title", default=todo.title)
    
    # Edit due date
    due_date_str = ""
    if todo.due_date:
        due_date_str = todo.due_date.strftime("%Y-%m-%d") if hasattr(todo.due_date, "strftime") else str(todo.due_date)
    new_due_date_str = typer.prompt("Due date", default=due_date_str)
    new_due_date = None
    if new_due_date_str:
        try:
            new_due_date = store.parse_date(new_due_date_str)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {str(e)}")
            new_due_date = todo.due_date
    
    # Edit estimated time
    new_time = typer.prompt("Estimated time", default=todo.estimated_time or "")
    if not new_time:
        new_time = None
    
    # Edit status
    status_options = ["pending", "in_progress", "completed"]
    current_status = str(todo.status) if todo.status else "pending"
    status_index = status_options.index(current_status) if current_status in status_options else 0
    
    # Display available status options
    console.print("Available statuses: " + ", ".join(status_options))
    new_status = typer.prompt(f"Status", default=current_status)
    
    # Validate status
    if new_status not in status_options:
        console.print(f"[yellow]Warning:[/yellow] Invalid status '{new_status}'. Using '{current_status}' instead.")
        new_status = current_status
    
    # Edit details
    if typer.confirm("Edit details?", default=False):
        new_details = open_editor(todo.details or "")
        if new_details is not None:  # None means editing was cancelled
            todo.details = new_details
    
    # Update todo
    store.update_todo(
        todo.id,
        title=new_title,
        due_date=new_due_date,
        estimated_time=new_time,
        status=new_status
    )
    
    console.print(f"[green]Todo updated:[/green] {new_title}")


@app.command("done")
def mark_done(todo_id: str = typer.Argument(..., help="The ID of the todo to mark as completed")):
    """Mark a todo as completed."""
    todo = store.get_todo(todo_id)
    
    # If not found with exact ID, try prefix match
    if todo is None:
        todos = store.get_all_todos()
        matching_todos = [t for t in todos if t.id.startswith(todo_id)]
        
        if len(matching_todos) == 1:
            todo = matching_todos[0]
        elif len(matching_todos) > 1:
            console.print(f"Multiple todos found matching '{todo_id}':")
            for t in matching_todos:
                console.print(f"- {t.id[:8]}: {t.title}")
            return
    
    if todo is None:
        console.print(f"[red]Todo with ID '{todo_id}' not found.[/red]")
        return
    
    # Update status
    store.update_todo(todo.id, status="completed")
    console.print(f"[green]Marked as completed:[/green] {todo.title}")


@app.command("delete")
def delete_todo(todo_id: str = typer.Argument(..., help="The ID of the todo to delete")):
    """Delete a todo."""
    todo = store.get_todo(todo_id)
    
    # If not found with exact ID, try prefix match
    if todo is None:
        todos = store.get_all_todos()
        matching_todos = [t for t in todos if t.id.startswith(todo_id)]
        
        if len(matching_todos) == 1:
            todo = matching_todos[0]
        elif len(matching_todos) > 1:
            console.print(f"Multiple todos found matching '{todo_id}':")
            for t in matching_todos:
                console.print(f"- {t.id[:8]}: {t.title}")
            return
    
    if todo is None:
        console.print(f"[red]Todo with ID '{todo_id}' not found.[/red]")
        return
    
    # Confirm deletion
    if typer.confirm(f"Are you sure you want to delete todo '{todo.title}'?", default=False):
        if store.delete_todo(todo.id):
            console.print(f"[green]Todo deleted:[/green] {todo.title}")
        else:
            console.print("[red]Error deleting todo.[/red]")
    else:
        console.print("Deletion cancelled.")


@app.command("move")
def move_todo(
    todo_id: str = typer.Argument(..., help="The ID of the todo to move"),
    date_str: str = typer.Argument(..., help="New due date (e.g., 'today', '25-may', '5/25/2025')")
):
    """Change the due date of a todo."""
    todo = store.get_todo(todo_id)
    
    # If not found with exact ID, try prefix match
    if todo is None:
        todos = store.get_all_todos()
        matching_todos = [t for t in todos if t.id.startswith(todo_id)]
        
        if len(matching_todos) == 1:
            todo = matching_todos[0]
        elif len(matching_todos) > 1:
            console.print(f"Multiple todos found matching '{todo_id}':")
            for t in matching_todos:
                console.print(f"- {t.id[:8]}: {t.title}")
            return
    
    if todo is None:
        console.print(f"[red]Todo with ID '{todo_id}' not found.[/red]")
        return
    
    # Parse new date
    try:
        new_date = store.parse_date(date_str)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        return
    
    # Get current date for display
    old_date = None
    if todo.due_date:
        old_date = todo.due_date.strftime("%Y-%m-%d") if hasattr(todo.due_date, "strftime") else str(todo.due_date)
    
    # Update todo
    store.update_todo(todo.id, due_date=new_date)
    
    if old_date:
        console.print(f"[green]Moved todo:[/green] {todo.title}")
        console.print(f"From: {old_date}")
        console.print(f"To: {new_date}")
    else:
        console.print(f"[green]Set due date for todo:[/green] {todo.title}")
        console.print(f"Due date: {new_date}")


@app.command("today")
def today_todos():
    """List todos due today."""
    today = date.today()
    todos = store.get_todos_by_date(today)
    
    if not todos:
        console.print("No todos due today.")
        return
    
    # Create a rich table for display
    table = Table(title=f"Todos for Today ({today.strftime('%Y-%m-%d')})")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Status", style="blue")
    table.add_column("Est. Time", style="yellow")
    
    for todo in todos:
        # Get a shorter ID for display
        short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
        
        # Format status with color
        status_str = todo.status
        if status_str == "completed":
            status_str = f"[green]{status_str}[/green]"
        elif status_str == "in_progress":
            status_str = f"[blue]{status_str}[/blue]"
        elif status_str == "pending":
            status_str = f"[yellow]{status_str}[/yellow]"
        
        table.add_row(
            short_id,
            todo.title,
            status_str,
            todo.estimated_time or ""
        )
    
    console.print(table)


@app.command("tomorrow")
def tomorrow_todos():
    """List todos due tomorrow."""
    tomorrow = date.today() + timedelta(days=1)
    todos = store.get_todos_by_date(tomorrow)
    
    if not todos:
        console.print("No todos due tomorrow.")
        return
    
    # Create a rich table for display
    table = Table(title=f"Todos for Tomorrow ({tomorrow.strftime('%Y-%m-%d')})")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Status", style="blue")
    table.add_column("Est. Time", style="yellow")
    
    for todo in todos:
        # Get a shorter ID for display
        short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
        
        # Format status with color
        status_str = todo.status
        if status_str == "completed":
            status_str = f"[green]{status_str}[/green]"
        elif status_str == "in_progress":
            status_str = f"[blue]{status_str}[/blue]"
        elif status_str == "pending":
            status_str = f"[yellow]{status_str}[/yellow]"
        
        table.add_row(
            short_id,
            todo.title,
            status_str,
            todo.estimated_time or ""
        )
    
    console.print(table)


@app.command("yesterday")
def yesterday_todos():
    """List todos due yesterday."""
    yesterday = date.today() - timedelta(days=1)
    todos = store.get_todos_by_date(yesterday)
    
    if not todos:
        console.print("No todos due yesterday.")
        return
    
    # Create a rich table for display
    table = Table(title=f"Todos for Yesterday ({yesterday.strftime('%Y-%m-%d')})")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Status", style="blue")
    table.add_column("Est. Time", style="yellow")
    
    for todo in todos:
        # Get a shorter ID for display
        short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
        
        # Format status with color
        status_str = todo.status
        if status_str == "completed":
            status_str = f"[green]{status_str}[/green]"
        elif status_str == "in_progress":
            status_str = f"[blue]{status_str}[/blue]"
        elif status_str == "pending":
            status_str = f"[yellow]{status_str}[/yellow]"
        
        table.add_row(
            short_id,
            todo.title,
            status_str,
            todo.estimated_time or ""
        )
    
    console.print(table)


@app.command("week")
def week_todos():
    """List todos for the current week, grouped by day."""
    week_todos = store.get_week_todos()
    
    if not week_todos:
        console.print("No todos for this week.")
        return
    
    # Get the first day of the week (Monday)
    today = date.today()
    start_date = today - timedelta(days=today.weekday())
    
    # Display week range
    end_date = start_date + timedelta(days=6)
    console.print(f"[bold]Todos for Week: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}[/bold]")
    
    # Display todos for each day
    for day_num in range(7):
        current_date = start_date + timedelta(days=day_num)
        day_name = current_date.strftime("%A")
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Highlight today
        if current_date == today:
            console.print(f"\n[bold yellow]{day_name} ({date_str}) - TODAY[/bold yellow]")
        else:
            console.print(f"\n[bold]{day_name} ({date_str})[/bold]")
        
        if current_date in week_todos:
            day_todos = week_todos[current_date]
            
            # Create a table for this day's todos
            table = Table(show_header=True, box=None, pad_edge=False, show_edge=False)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Title", style="green")
            table.add_column("Status", style="blue")
            table.add_column("Est. Time", style="yellow")
            
            for todo in day_todos:
                # Get a shorter ID for display
                short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
                
                # Format status with color
                status_str = todo.status
                if status_str == "completed":
                    status_str = f"[green]{status_str}[/green]"
                elif status_str == "in_progress":
                    status_str = f"[blue]{status_str}[/blue]"
                elif status_str == "pending":
                    status_str = f"[yellow]{status_str}[/yellow]"
                
                table.add_row(
                    short_id,
                    todo.title,
                    status_str,
                    todo.estimated_time or ""
                )
            
            console.print(table)
        else:
            console.print("  No todos for this day")


@app.command("date")
def date_todos(date_str: str = typer.Argument(..., help="Date to list todos for (e.g., 'today', '25-may', '5/25/2025')")):
    """List todos for a specific date."""
    try:
        target_date = store.parse_date(date_str)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        return
    
    todos = store.get_todos_by_date(target_date)
    
    if not todos:
        console.print(f"No todos for {target_date.strftime('%Y-%m-%d')}.")
        return
    
    # Create a rich table for display
    day_name = target_date.strftime("%A")
    table = Table(title=f"Todos for {day_name}, {target_date.strftime('%Y-%m-%d')}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Status", style="blue")
    table.add_column("Est. Time", style="yellow")
    
    for todo in todos:
        # Get a shorter ID for display
        short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
        
        # Format status with color
        status_str = todo.status
        if status_str == "completed":
            status_str = f"[green]{status_str}[/green]"
        elif status_str == "in_progress":
            status_str = f"[blue]{status_str}[/blue]"
        elif status_str == "pending":
            status_str = f"[yellow]{status_str}[/yellow]"
        
        table.add_row(
            short_id,
            todo.title,
            status_str,
            todo.estimated_time or ""
        )
    
    console.print(table)


@app.command("pending")
def pending_todos():
    """List all pending todos."""
    todos = store.get_todos_by_status("pending")
    
    if not todos:
        console.print("No pending todos.")
        return
    
    # Create a rich table for display
    table = Table(title="Pending Todos")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Due Date", style="magenta")
    table.add_column("Est. Time", style="yellow")
    
    for todo in todos:
        # Get a shorter ID for display
        short_id = todo.id[:8] if len(todo.id) > 8 else todo.id
        
        # Format due date
        due_date = ""
        if todo.due_date:
            due_date = todo.due_date.strftime("%Y-%m-%d") if hasattr(todo.due_date, "strftime") else str(todo.due_date)
            
            # Highlight due today or overdue
            today = date.today()
            if hasattr(todo.due_date, "date"):
                todo_date = todo.due_date.date()
            else:
                todo_date = todo.due_date
                
            if todo_date < today:
                due_date = f"[bold red]{due_date}[/bold red]"
            elif todo_date == today:
                due_date = f"[bold yellow]{due_date}[/bold yellow]"
        
        table.add_row(
            short_id,
            todo.title,
            due_date,
            todo.estimated_time or ""
        )
    
    console.print(table)