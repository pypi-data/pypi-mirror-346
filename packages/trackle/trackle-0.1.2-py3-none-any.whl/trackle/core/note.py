"""
Note module for handling knowledge notes.
"""
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import yaml

class Note:
    """Class representing a knowledge note."""
    
    def __init__(
        self,
        title: str,
        content: str,
        tags: List[str] = None,
        note_type: str = "note",
        date: Optional[datetime] = None,
        note_id: Optional[str] = None
    ):
        # Ensure title is a string
        self.title = str(title) if title is not None else "Untitled"
        
        # Ensure content is a string
        self.content = str(content) if content is not None else ""
        
        # Normalize tags
        if tags is None:
            self.tags = []
        elif hasattr(tags, "__iter__") and not isinstance(tags, (str, bytes)):
            # It's a non-string iterable, convert elements to strings
            self.tags = [str(tag) for tag in tags]
        else:
            # It's a single non-list item
            self.tags = [str(tags)]
            
        # Ensure note_type is a string
        self.type = str(note_type) if note_type is not None else "note"
        
        # Handle date
        if date is None:
            self.date = datetime.now()
        elif isinstance(date, datetime):
            self.date = date
        else:
            # Try to convert to string
            self.date = str(date)
            
        # Generate or use provided ID
        self.id = str(note_id) if note_id is not None else str(uuid.uuid4())
    
    @classmethod
    def from_file(cls, file_path: Path) -> "Note":
        """Load a note from a markdown file."""
        with open(file_path, "r") as f:
            content = f.read()
        
        # Extract YAML frontmatter
        if content.startswith("---"):
            end_index = content.find("---", 3)
            if end_index != -1:
                frontmatter = content[3:end_index].strip()
                
                # Use safe_load with error handling
                try:
                    metadata = yaml.safe_load(frontmatter)
                    if metadata is None:
                        metadata = {}
                except Exception as e:
                    print(f"Warning: Error parsing YAML in {file_path}: {str(e)}")
                    metadata = {}
                
                body = content[end_index + 3:].strip()
                
                # Normalize tags from metadata
                tags = metadata.get("tags", [])
                if tags is None:
                    tags = []
                elif not isinstance(tags, list):
                    # If it's not a list, convert to a single-item list
                    tags = [str(tags)]
                
                return cls(
                    title=metadata.get("title", "Untitled"),
                    content=body,
                    tags=tags,
                    note_type=metadata.get("type", "note"),
                    date=metadata.get("date"),
                    note_id=file_path.stem  # Use filename as ID
                )
        
        # If no frontmatter, treat entire content as body
        return cls(
            title="Untitled",
            content=content,
            note_id=file_path.stem
        )
    
    def to_markdown(self) -> str:
        """Convert note to markdown format with YAML frontmatter."""
        # Convert tags to list of strings if it's not already
        tags = self.tags
        if hasattr(self.tags, "__iter__") and not isinstance(self.tags, str):
            # Convert to list of strings and handle any special objects
            tags = [str(tag) for tag in self.tags]
        elif not isinstance(self.tags, list):
            # If it's some other type, convert to string and make a single-item list
            tags = [str(self.tags)]
            
        frontmatter = {
            "title": self.title,
            "tags": tags,
            "date": self.date.strftime("%Y-%m-%d") if hasattr(self.date, "strftime") else str(self.date),
            "type": self.type
        }
        
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)
        return f"---\n{yaml_str}---\n\n{self.content}"
    
    def save(self, directory: Path) -> Path:
        """Save note to a file."""
        file_path = directory / f"{self.id}.md"
        with open(file_path, "w") as f:
            f.write(self.to_markdown())
        return file_path
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert note to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "type": self.type,
            "date": self.date.strftime("%Y-%m-%d") if isinstance(self.date, datetime) else self.date,
            "content": self.content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Note":
        """Create note from dictionary."""
        return cls(
            title=data.get("title", "Untitled"),
            content=data.get("content", ""),
            tags=data.get("tags", []),
            note_type=data.get("type", "note"),
            date=data.get("date"),
            note_id=data.get("id")
        )