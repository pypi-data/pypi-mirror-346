"""
Command Line Interface for trackle.
"""
import os
import sys
import warnings
from pathlib import Path
from typing import List, Optional

# Suppress the LibreSSL warning from urllib3
warnings.filterwarnings("ignore", message=".*OpenSSL.*LibreSSL.*")

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from trackle.core.note import Note
from trackle.core.storage import KnowledgeStore
from trackle.utils.editor import open_editor
from trackle.cli_todo import app as todo_app
from trackle.cli_note import app as note_app

app = typer.Typer(help="trackle - A personal knowledge logging and retrieval system")
console = Console()

# Initialize store
store = KnowledgeStore()

# Add subcommands
app.add_typer(todo_app, name="todo")
app.add_typer(note_app, name="note")


@app.command()
def new(
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Note title"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-g", help="Tags for the note"),
    note_type: str = typer.Option("note", "--type", "-y", help="Note type (note, migration, bug, etc.)"),
):
    """Create a new knowledge note."""
    if title is None:
        title = typer.prompt("Title")
    
    # Handle tags
    processed_tags = []
    if tags is None:
        tags_input = typer.prompt("Tags (comma separated)")
        processed_tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
    else:
        # Safely convert any type to a list of strings
        if hasattr(tags, "__iter__") and not isinstance(tags, (str, bytes)):
            # It's some kind of iterable (list, tuple, etc.)
            processed_tags = [str(tag) for tag in tags]
        else:
            # It's a single value (or a string which we don't want to split by char)
            processed_tags = [str(tags)]
    
    # First gather all metadata before opening editor
    typer.echo("\nCreating new note")
    typer.echo("-----------------")
    typer.echo(f"Title: {title}")
    typer.echo(f"Tags: {', '.join(processed_tags)}")
    typer.echo(f"Type: {note_type}")
    typer.echo("-----------------\n")
    
    typer.echo("Now opening editor for content. Enter your note details.")
    typer.echo("(To cancel, follow the instructions in the editor)")
    
    # Prepare initial content with template and metadata reminder
    initial_content = f"""##### Context

##### Details
"""
    
    # Open editor for content
    content = open_editor(initial_content)
    if not content:
        typer.echo("Note creation cancelled.")
        raise typer.Exit(1)
    
    # Create and save note
    note = store.create_note(
        title=title,
        content=content,
        tags=processed_tags,
        note_type=note_type
    )
    
    typer.echo(f"Note created with ID: {note.id}")
    typer.echo(f"Saved to: {store.store_dir / f'{note.id}.md'}")


@app.command()
def reindex():
    """Rebuild the vector index for all notes."""
    typer.echo("Building index...")
    store.build_index()
    typer.echo("Index built successfully.")


@app.command()
def query(
    query_text: str = typer.Argument(..., help="The query text to search for"),
    limit: int = typer.Option(5, "--limit", "-l", help="Maximum number of results"),
):
    """Search for notes semantically similar to the query."""
    try:
        results = store.query(query_text, k=limit)
        
        if not results:
            typer.echo("No matching notes found.")
            return
        
        # Create a rich table for display
        table = Table(title=f"Results for: {query_text}")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Type", style="blue")
        table.add_column("Date", style="magenta")
        table.add_column("Score", style="yellow")
        
        for result in results:
            table.add_row(
                result["id"],  # Show full ID
                result["title"],
                result["type"],
                result["date"],
                f"{result['score']:.2f}"
            )
        
        console.print(table)
        
    except RuntimeError as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)


@app.command()
def view(note_id: str = typer.Argument(..., help="The ID of the note to view")):
    """View a specific note by ID."""
    console.print(f"Searching for note: {note_id}")
    
    # Try exact ID first
    note = store.get_note(note_id)
    
    # Debug info
    if note:
        console.print(f"Found exact match: {note.id}")
    else:
        console.print(f"No exact match for: {note_id}")
        console.print("Trying partial match...")
    
    # If not found, try to match partial ID
    if note is None:
        all_notes = store.list_notes()
        # Try to match the beginning of any note ID
        matching_notes = [n for n in all_notes if n.id.startswith(note_id)]
        
        # If no matches found by prefix, try to match anywhere in the ID
        if not matching_notes:
            matching_notes = [n for n in all_notes if note_id in n.id]
            
        if len(matching_notes) == 1:
            note = matching_notes[0]
            console.print(f"Found one matching note: {note.id}")
        elif len(matching_notes) > 1:
            console.print(f"Multiple notes found matching '{note_id}':")
            for n in matching_notes:
                console.print(f"- {n.id}: {n.title}")
            raise typer.Exit(1)
        else:
            console.print("No matches found by ID substring")
    
    if note is None:
        # One last attempt - try to match by title
        all_notes = store.list_notes()
        title_matches = [n for n in all_notes if note_id.lower() in n.title.lower()]
        
        if len(title_matches) == 1:
            note = title_matches[0]
            console.print(f"Found by title match: {note.title}")
        elif len(title_matches) > 1:
            console.print(f"Multiple notes found with title matching '{note_id}':")
            for n in title_matches:
                console.print(f"- {n.id}: {n.title}")
            raise typer.Exit(1)
    
    if note is None:
        console.print(f"[red]Note with ID or title '{note_id}' not found.[/red]")
        raise typer.Exit(1)
    
    # Display note with rich formatting
    console.print(f"# {note.title}", style="bold green")
    console.print(f"Type: {note.type}", style="blue")
    console.print(f"Date: {note.date}", style="magenta")
    console.print(f"Tags: {', '.join(note.tags)}", style="cyan")
    console.print("\n" + note.content)


@app.command()
def list():
    """List all notes."""
    notes = store.list_notes()
    
    if not notes:
        typer.echo("No notes found.")
        return
    
    # Create a rich table for display
    table = Table(title="All Notes")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Type", style="blue")
    table.add_column("Date", style="magenta")
    table.add_column("Tags", style="yellow")
    
    for note in notes:
        date_str = note.date.strftime("%Y-%m-%d") if hasattr(note.date, "strftime") else str(note.date)
        
        # Show short ID but include full ID for copy-paste convenience
        short_id = note.id
        if len(note.id) > 8:
            # For UUIDs, just show first 8 chars
            short_id = note.id[:8]
            typer.echo(f"Note ID: {short_id} (full: {note.id})")
        
        table.add_row(
            short_id,  # Show shortened ID for readability
            note.title,
            note.type,
            date_str,
            ", ".join(note.tags)
        )
    
    console.print(table)


@app.command()
def delete(note_id: str = typer.Argument(..., help="The ID of the note to delete")):
    """Delete a note."""
    console.print(f"Searching for note: {note_id}")
    
    # First try to find the note
    note = store.get_note(note_id)
    
    # If not found, try partial matches
    if note is None:
        all_notes = store.list_notes()
        # Try to match the beginning of any note ID
        matching_notes = [n for n in all_notes if n.id.startswith(note_id)]
        
        # If no matches found by prefix, try to match anywhere in the ID
        if not matching_notes:
            matching_notes = [n for n in all_notes if note_id in n.id]
            
        if len(matching_notes) == 1:
            note = matching_notes[0]
            console.print(f"Found one matching note: {note.id}")
        elif len(matching_notes) > 1:
            console.print(f"Multiple notes found matching '{note_id}':")
            for n in matching_notes:
                console.print(f"- {n.id}: {n.title}")
            raise typer.Exit(1)
    
    if note is None:
        typer.echo(f"Note with ID {note_id} not found.")
        raise typer.Exit(1)
    
    # Preview the note before deletion
    console.print(f"\n[bold red]About to delete note:[/bold red]")
    console.print(f"# {note.title}", style="bold green")
    console.print(f"Type: {note.type}", style="blue")
    console.print(f"Date: {note.date}", style="magenta")
    console.print(f"Tags: {', '.join(note.tags)}", style="cyan")
    
    # Confirm deletion
    if not typer.confirm(f"\nAre you sure you want to delete this note?", default=False):
        console.print("Deletion cancelled.")
        raise typer.Exit(0)
    
    # Delete the note
    if store.delete_note(note.id):
        console.print(f"[bold green]Note '{note.title}' ({note.id}) has been deleted.[/bold green]")
    else:
        console.print(f"[bold red]Error:[/bold red] Failed to delete note.")
        raise typer.Exit(1)


@app.command()
def edit(note_id: str = typer.Argument(..., help="The ID of the note to edit")):
    """Edit an existing note's content."""
    console.print(f"Searching for note: {note_id}")
    
    # First try to find the note
    note = store.get_note(note_id)
    
    # If not found, try partial matches
    if note is None:
        all_notes = store.list_notes()
        # Try to match the beginning of any note ID
        matching_notes = [n for n in all_notes if n.id.startswith(note_id)]
        
        # If no matches found by prefix, try to match anywhere in the ID
        if not matching_notes:
            matching_notes = [n for n in all_notes if note_id in n.id]
            
        if len(matching_notes) == 1:
            note = matching_notes[0]
            console.print(f"Found one matching note: {note.id}")
        elif len(matching_notes) > 1:
            console.print(f"Multiple notes found matching '{note_id}':")
            for n in matching_notes:
                console.print(f"- {n.id}: {n.title}")
            raise typer.Exit(1)
    
    if note is None:
        typer.echo(f"Note with ID {note_id} not found.")
        raise typer.Exit(1)
    
    # Now we have a note to edit
    console.print(f"Editing note: {note.title} ({note.id})")
    
    # Allow editing metadata
    if typer.confirm("Edit metadata (title, tags, type)?", default=False):
        # Edit title
        new_title = typer.prompt("Title", default=note.title)
        
        # Edit tags
        tags_str = ", ".join(note.tags)
        new_tags_str = typer.prompt("Tags (comma separated)", default=tags_str)
        new_tags = [tag.strip() for tag in new_tags_str.split(",") if tag.strip()]
        
        # Edit type
        new_type = typer.prompt("Type", default=note.type)
        
        # Update the note's metadata
        note.title = new_title
        note.tags = new_tags
        note.type = new_type
    
    # Edit content
    from trackle.utils.editor import open_editor
    updated_content = open_editor(note.content)
    
    if updated_content is None:
        typer.echo("Note editing cancelled.")
        raise typer.Exit(1)
    
    # Update content if it was changed
    if updated_content != note.content:
        note.content = updated_content
    
    # Save the updated note
    note.save(store.store_dir)
    typer.echo(f"Note updated: {note.id}")
    
    # Display preview of updated note
    console.print("\n[bold]Updated Note:[/bold]")
    console.print(f"# {note.title}", style="bold green")
    console.print(f"Type: {note.type}", style="blue")
    console.print(f"Tags: {', '.join(note.tags)}", style="cyan")
    console.print("\n" + note.content[:200] + ("..." if len(note.content) > 200 else ""))


def check_and_auto_reindex():
    """Check if reindexing is needed and perform it automatically if required."""
    if store.needs_reindex():
        typer.echo("Detected new or modified notes. Auto-reindexing...")
        store.build_index()
        typer.echo("Index rebuilt successfully.")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Start the interactive shell if no command is provided."""
    if ctx.invoked_subcommand is None:
        # Check if reindexing is needed
        check_and_auto_reindex()
        
        # Import here to avoid circular imports
        from trackle.shell import run_interactive_shell
        run_interactive_shell()
    elif ctx.invoked_subcommand != "reindex":
        # For all commands except reindex, check if reindexing is needed
        check_and_auto_reindex()


if __name__ == "__main__":
    app()
