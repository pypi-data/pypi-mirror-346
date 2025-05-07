"""
Interactive shell for trackle main CLI.
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
    console.print("\n[bold cyan]Trackle Interactive Shell[/bold cyan]")
    console.print("\nAvailable modules:")
    console.print("  [green]note[/green]                Manage knowledge notes with interactive shell")
    console.print("  [green]todo[/green]                Manage todos with interactive shell")
    console.print("  [green]help[/green]                Show this help message")
    console.print("  [green]exit[/green], [green]quit[/green]           Exit the shell")
    console.print("\nExamples:")
    console.print("  note          # Enter note management shell")
    console.print("  todo          # Enter todo management shell")
    
    console.print("\nLegacy note commands (for backward compatibility):")
    console.print("  [green]new[/green]                 Create a new knowledge note")
    console.print("  [green]edit[/green] [yellow]<id>[/yellow]          Edit an existing note")
    console.print("  [green]delete[/green] [yellow]<id>[/yellow]        Delete a note")
    console.print("  [green]list[/green]                List all notes")
    console.print("  [green]view[/green] [yellow]<id>[/yellow]          View a specific note by ID")
    console.print("  [green]query[/green] [yellow]<text>[/yellow]       Search for notes")
    console.print("  [green]reindex[/green]             Rebuild the search index")
    console.print("")


def run_interactive_shell() -> None:
    """Run the interactive shell."""
    # Configure prompt style
    style = Style.from_dict({
        'prompt': 'ansigreen bold',
    })
    
    # Set up command completion
    commands = ["note", "todo", "exit", "quit", "help",
                # Legacy note commands for backward compatibility
                "new", "list", "view", "edit", "delete", "query", "reindex"]
    completer = WordCompleter(commands, ignore_case=True)
    
    # Create prompt session with history
    try:
        # Use a file in the user's home directory for history
        import os
        history_file = os.path.expanduser("~/.trackle_history")
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
    console.print("[bold cyan]Trackle Interactive Shell[/bold cyan] - Type [green]help[/green] for available commands")
    
    while True:
        try:
            # Get input from user
            text = session.prompt("trackle> ")
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
                
            # Handle command matching
            if command == "help":
                print_help()
            elif command == "exit" or command == "quit":
                break
            elif command == "note":
                # Import and run note shell
                try:
                    from trackle.note_shell import run_interactive_shell as run_note_shell
                    run_note_shell()
                except Exception as e:
                    console.print(f"[red]Error running note shell:[/red] {str(e)}")
            elif command == "todo":
                # Import and run todo shell
                try:
                    from trackle.todo_shell import run_interactive_shell as run_todo_shell
                    run_todo_shell()
                except Exception as e:
                    console.print(f"[red]Error running todo shell:[/red] {str(e)}")
            # For backward compatibility, forward note commands to note shell
            elif command in ["new", "list", "view", "edit", "delete", "query", "reindex"]:
                # Forward to note shell
                try:
                    # Import note commands
                    from trackle.cli_note import new, list_notes, view, edit, delete, query, reindex
                    
                    # Execute the command
                    if command == "new":
                        new()
                    elif command == "list":
                        list_notes()
                    elif command == "view":
                        if command_args:
                            view(note_id=command_args[0])
                        else:
                            console.print("[red]Error:[/red] View requires a note ID")
                    elif command == "edit":
                        if command_args:
                            edit(note_id=command_args[0])
                        else:
                            console.print("[red]Error:[/red] Edit requires a note ID")
                    elif command == "delete":
                        if command_args:
                            delete(note_id=command_args[0])
                        else:
                            console.print("[red]Error:[/red] Delete requires a note ID")
                    elif command == "query":
                        if command_args:
                            query_text = " ".join(command_args)
                            query(query_text=query_text)
                        else:
                            console.print("[red]Error:[/red] Query requires search text")
                    elif command == "reindex":
                        reindex()
                except Exception as e:
                    console.print(f"[red]Error executing note command:[/red] {str(e)}")
            else:
                # No matches
                console.print(f"[red]Unknown command:[/red] {command}")
                console.print("Type [green]help[/green] for available commands")
        
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