"""
Interactive shell for trackle todo using prompt_toolkit.
"""
import re
import shlex
import sys
from typing import List, Dict, Callable, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.table import Table
from typer import Context, Typer

from trackle.cli_todo import app, new_todo, list_todos, view_todo, edit_todo, mark_done, delete_todo, move_todo
from trackle.cli_todo import today_todos, tomorrow_todos, yesterday_todos, week_todos, date_todos, pending_todos


class TodoCompleter(Completer):
    """Custom completer for todo commands."""
    
    def __init__(self, commands: List[str], store=None):
        self.commands = commands
        self.word_completer = WordCompleter(commands, ignore_case=True)
        self.store = store
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()
        
        # If text is empty, complete all commands
        if not text:
            for command in self.commands:
                yield Completion(command, start_position=0, display=command)
            return
        
        # Complete commands if there's no space (still on first word)
        if ' ' not in text:
            # Manual command completion to avoid WordCompleter issues
            word_before_cursor = document.get_word_before_cursor() or ""
            for command in self.commands:
                if command and word_before_cursor and command.lower().startswith(word_before_cursor.lower()):
                    yield Completion(
                        command,
                        start_position=-len(word_before_cursor),
                        display=command
                    )
            return
        
        # Extract command and arguments
        parts = text.split(' ')
        command = parts[0].lower() if parts and parts[0] else ""
        current_word = parts[-1] if len(parts) > 1 else ""
        
        # Add specific completions for each command
        if (command == 'view' or command == 'edit' or command == 'done' or command == 'delete') and self.store:
            # Add completions for todo IDs - with error suppression
            try:
                todos = []
                # Silence warnings during tab completion
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    todos = self.store.get_all_todos()
                
                # Generate shortened IDs for UUIDs
                for todo in todos:
                    if not todo.id or not current_word:
                        continue
                    
                    # For UUID-like IDs, also offer a shortened version
                    todo_id = todo.id
                    display_id = todo_id
                    short_id = None
                    
                    # If it looks like a UUID, use first 8 chars as short_id
                    if len(todo_id) > 8 and '-' in todo_id:
                        short_id = todo_id[:8]
                        
                    # Check if either full ID or short ID matches current input
                    if todo_id.startswith(current_word):
                        display = f"{todo_id} - {todo.title}"
                        yield Completion(
                            todo_id,
                            start_position=-len(current_word),
                            display=display
                        )
                    elif short_id and short_id.startswith(current_word):
                        display = f"{short_id} - {todo.title} (full: {todo_id})"
                        yield Completion(
                            short_id,
                            start_position=-len(current_word),
                            display=display
                        )
            except Exception:
                # Fall back gracefully if there's an error
                pass


def parse_args(input_str: str) -> List[str]:
    """Parse input string into command and arguments."""
    if not input_str or not input_str.strip():
        return [""]
    
    try:
        args = shlex.split(input_str)
        return args if args else [""]
    except ValueError:
        args = input_str.split()
        return args if args else [""]


def print_help() -> None:
    """Display help information."""
    console = Console()
    console.print("\n[bold cyan]Trackle Todo Interactive Shell[/bold cyan]")
    console.print("\nAvailable commands:")
    console.print("  [green]new[/green]                 Create a new todo")
    console.print("  [green]edit[/green] [yellow]<id>[/yellow]          Edit an existing todo")
    console.print("  [green]delete[/green] [yellow]<id>[/yellow]        Delete a todo")
    console.print("  [green]list[/green]                List all todos")
    console.print("  [green]view[/green] [yellow]<id>[/yellow]          View a specific todo by ID")
    console.print("  [green]done[/green] [yellow]<id>[/yellow]          Mark a todo as completed")
    console.print("  [green]move[/green] [yellow]<id> <date>[/yellow]   Change a todo's due date")
    console.print("  [green]today[/green]              Show todos due today")
    console.print("  [green]tomorrow[/green]           Show todos due tomorrow")
    console.print("  [green]yesterday[/green]          Show todos due yesterday")
    console.print("  [green]week[/green]               Show todos for this week")
    console.print("  [green]date[/green] [yellow]<date>[/yellow]        Show todos for a specific date")
    console.print("  [green]pending[/green]            Show all pending todos")
    console.print("  [green]help[/green]               Show this help message")
    console.print("  [green]exit[/green], [green]quit[/green]           Exit the shell")
    console.print("\nExamples:")
    console.print("  new")
    console.print("  view 70eff3d6")
    console.print("  edit 70eff3d6")
    console.print("  done 70eff3d6")
    console.print("  move 70eff3d6 tomorrow")
    console.print("  date 2025-06-01")
    console.print("")


def run_interactive_shell() -> None:
    """Run the interactive shell."""
    # Import here to avoid circular imports
    from trackle.cli_todo import store
    
    # Configure prompt style
    style = Style.from_dict({
        'prompt': 'ansigreen bold',
    })
    
    # Set up command completion with hard-coded commands that match the CLI
    command_mapping = {
        "new": new_todo,
        "list": list_todos,
        "view": view_todo,
        "edit": edit_todo,
        "done": mark_done,
        "delete": delete_todo,
        "move": move_todo,
        "today": today_todos,
        "tomorrow": tomorrow_todos,
        "yesterday": yesterday_todos,
        "week": week_todos,
        "date": date_todos,
        "pending": pending_todos,
        "exit": lambda: sys.exit(0),
        "quit": lambda: sys.exit(0),
        "help": lambda: print_help()
    }
    commands = list(command_mapping.keys())
    completer = TodoCompleter(commands, store=store)
    
    # Create prompt session with history
    try:
        # Use a file in the user's home directory for history
        import os
        history_file = os.path.expanduser("~/.trackle_todo_history")
        session = PromptSession(
            history=FileHistory(history_file),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            style=style,
        )
    except:
        # Fall back to in-memory history if file can't be created
        session = PromptSession(
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            style=style,
        )
    
    console = Console()
    console.print("[bold cyan]Trackle Todo Interactive Shell[/bold cyan] - Type [green]help[/green] for available commands")
    
    while True:
        try:
            # Get input from user
            text = session.prompt("trackle todo> ")
            text = text.strip()
            
            # Skip empty input
            if not text:
                continue
            
            # Parse input
            args = parse_args(text)
            command = args[0].lower() if args and args[0] else ""
            command_args = args[1:]
            
            # Skip empty command
            if not command:
                continue
                
            # Try to find a matching command (including abbreviations)
            matching_commands = [cmd for cmd in command_mapping.keys() if cmd and command and cmd.startswith(command)]
            
            # Handle command matching
            if command in command_mapping:
                # Exact match
                matching_command = command
            elif len(matching_commands) == 1:
                # Single abbreviation match
                matching_command = matching_commands[0]
            elif len(matching_commands) > 1:
                # Multiple matches, show options
                console.print(f"[yellow]Ambiguous command:[/yellow] {command}")
                console.print("Did you mean one of these?")
                for cmd in matching_commands:
                    console.print(f"  [green]{cmd}[/green]")
                continue
            else:
                # No matches
                console.print(f"[red]Unknown command:[/red] {command}")
                console.print("Type [green]help[/green] for available commands")
                continue
            
            # Execute the matched command
            try:
                if matching_command == "help":
                    print_help()
                elif matching_command == "exit" or matching_command == "quit":
                    break
                elif matching_command == "new":
                    # Pass explicit None values for all parameters to avoid OptionInfo objects
                    new_todo(None, None, None, None)
                elif matching_command == "list":
                    list_todos(None)
                elif matching_command == "today":
                    today_todos()
                elif matching_command == "tomorrow":
                    tomorrow_todos()
                elif matching_command == "yesterday":
                    yesterday_todos()
                elif matching_command == "week":
                    week_todos()
                elif matching_command == "pending":
                    pending_todos()
                elif matching_command == "view":
                    if command_args:
                        view_todo(command_args[0])
                    else:
                        console.print("[red]Error:[/red] View requires a todo ID")
                elif matching_command == "edit":
                    if command_args:
                        edit_todo(command_args[0])
                    else:
                        console.print("[red]Error:[/red] Edit requires a todo ID")
                elif matching_command == "done":
                    if command_args:
                        mark_done(command_args[0])
                    else:
                        console.print("[red]Error:[/red] Done requires a todo ID")
                elif matching_command == "delete":
                    if command_args:
                        delete_todo(command_args[0])
                    else:
                        console.print("[red]Error:[/red] Delete requires a todo ID")
                elif matching_command == "move":
                    if len(command_args) >= 2:
                        move_todo(command_args[0], command_args[1])
                    else:
                        console.print("[red]Error:[/red] Move requires a todo ID and a date")
                elif matching_command == "date":
                    if command_args:
                        date_todos(command_args[0])
                    else:
                        console.print("[red]Error:[/red] Date requires a date string")
                else:
                    console.print(f"[red]Unknown command:[/red] {matching_command}")
            except Exception as e:
                console.print(f"[red]Error executing command:[/red] {str(e)}")
        
        except KeyboardInterrupt:
            # Handle Ctrl+C
            continue
        except EOFError:
            # Handle Ctrl+D
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    console.print("\nGoodbye!")


if __name__ == "__main__":
    run_interactive_shell()