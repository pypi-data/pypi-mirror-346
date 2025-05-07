"""
Editor utilities for handling user input.
"""
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def get_editor() -> str:
    """Get the user's preferred editor."""
    return os.environ.get("EDITOR", os.environ.get("VISUAL", "vi"))


def open_editor(initial_content: str = "") -> Optional[str]:
    """
    Open the user's editor and return the edited content.
    
    Returns None if the user cancels by:
    1. Not modifying the content and the cancel marker is present
    2. Removing all content
    3. If there's a subprocess error
    """
    editor = get_editor()
    
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w+", delete=False) as temp:
        temp_path = Path(temp.name)
        
        # Write initial content
        if initial_content:
            temp.write(initial_content)
        temp.flush()
    
    try:
        # Open the editor
        subprocess.run([editor, str(temp_path)], check=True)
        
        # Read the updated content
        with open(temp_path, "r") as f:
            content = f.read()
        
        # Check for cancellation
        if not content or content.strip() == "":
            print("Cancelled: Empty file")
            return None
            
        # Check if content was unchanged
        if initial_content and content.strip() == initial_content.strip():
            print("Cancelled: No changes made")
            return None
        
        return content
    except subprocess.SubprocessError:
        print(f"Error: Failed to open editor {editor}")
        return None
    finally:
        # Clean up
        if temp_path.exists():
            temp_path.unlink()