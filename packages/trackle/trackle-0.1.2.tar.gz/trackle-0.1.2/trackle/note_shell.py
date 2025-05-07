"""
Interactive shell for trackle note using prompt_toolkit.
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

from trackle.cli_note import app, new, reindex, query, view, edit, delete, list_notes


class NoteCompleter(Completer):
    """Custom completer for note commands."""
    
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
        if (command == 'view' or command == 'edit' or command == 'delete') and self.store:
            # Add completions for note IDs - with error suppression
            try:
                notes = []
                # Silence warnings during tab completion
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    notes = self.store.list_notes()
                
                # Generate shortened IDs for UUIDs
                for note in notes:
                    if not note.id or not current_word:
                        continue
                    
                    # For UUID-like IDs, also offer a shortened version
                    note_id = note.id
                    display_id = note_id
                    short_id = None
                    
                    # If it looks like a UUID, use first 8 chars as short_id
                    if len(note_id) > 8 and '-' in note_id:
                        short_id = note_id[:8]
                        
                    # Check if either full ID or short ID matches current input
                    if note_id.startswith(current_word):
                        display = f"{note_id} - {note.title}"
                        yield Completion(
                            note_id,
                            start_position=-len(current_word),
                            display=display
                        )
                    elif short_id and short_id.startswith(current_word):
                        display = f"{short_id} - {note.title} (full: {note_id})"
                        yield Completion(
                            short_id,
                            start_position=-len(current_word),
                            display=display
                        )
            except Exception:
                # Fall back gracefully if there's an error
                pass
        elif command == 'query':
            # No completions for query text
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
    console.print("\n[bold cyan]Trackle Note Interactive Shell[/bold cyan]")
    console.print("\nAvailable commands:")
    console.print("  [green]new[/green]                 Create a new knowledge note")
    console.print("  [green]edit[/green] [yellow]<id>[/yellow]          Edit an existing note")
    console.print("  [green]delete[/green] [yellow]<id>[/yellow]        Delete a note")
    console.print("  [green]list[/green]                List all notes")
    console.print("  [green]view[/green] [yellow]<id>[/yellow]          View a specific note by ID")
    console.print("  [green]query[/green] [yellow]<text>[/yellow]       Search for notes")
    console.print("  [green]reindex[/green]             Rebuild the search index")
    console.print("  [green]help[/green]                Show this help message")
    console.print("  [green]exit[/green], [green]quit[/green]           Exit the shell")
    console.print("\nExamples:")
    console.print("  query kubernetes migration")
    console.print("  view 70eff3d6")
    console.print("  edit 70eff3d6")
    console.print("  delete 70eff3d6")
    console.print("  new")
    console.print("")


def run_interactive_shell() -> None:
    """Run the interactive shell."""
    # Import here to avoid circular imports
    from trackle.cli_note import store
    
    # Configure prompt style
    style = Style.from_dict({
        'prompt': 'ansigreen bold',
    })
    
    # Set up command completion with hard-coded commands that match the CLI
    command_mapping = {
        "new": new,
        "edit": edit,
        "delete": delete,
        "reindex": reindex,
        "query": query,
        "view": view,
        "list": list_notes,
        "exit": lambda: sys.exit(0),
        "quit": lambda: sys.exit(0),
        "help": lambda: print_help()
    }
    commands = list(command_mapping.keys())
    completer = NoteCompleter(commands, store=store)
    
    # Create prompt session with history
    try:
        # Use a file in the user's home directory for history
        import os
        history_file = os.path.expanduser("~/.trackle_note_history")
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
    console.print("[bold cyan]Trackle Note Interactive Shell[/bold cyan] - Type [green]help[/green] for available commands")
    
    while True:
        try:
            # Get input from user
            text = session.prompt("trackle note> ")
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
                    new()
                elif matching_command == "reindex":
                    reindex()
                elif matching_command == "list":
                    list_notes()
                elif matching_command == "query":
                    if command_args:
                        query_text = " ".join(command_args)
                        query(query_text=query_text)
                    else:
                        console.print("[red]Error:[/red] Query requires search text")
                elif matching_command == "view":
                    if command_args:
                        view(note_id=command_args[0])
                    else:
                        console.print("[red]Error:[/red] View requires a note ID")
                elif matching_command == "edit":
                    if command_args:
                        edit(note_id=command_args[0])
                    else:
                        console.print("[red]Error:[/red] Edit requires a note ID")
                elif matching_command == "delete":
                    if command_args:
                        delete(note_id=command_args[0])
                    else:
                        console.print("[red]Error:[/red] Delete requires a note ID")
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