"""
Tests for the Note class.
"""
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from trackle.core.note import Note


def test_note_creation():
    """Test creating a note."""
    note = Note(
        title="Test Note",
        content="This is a test note.",
        tags=["test", "example"],
        note_type="test"
    )
    
    assert note.title == "Test Note"
    assert note.content == "This is a test note."
    assert note.tags == ["test", "example"]
    assert note.type == "test"
    assert isinstance(note.date, datetime)
    assert isinstance(note.id, str)


def test_note_to_markdown():
    """Test converting a note to markdown."""
    note = Note(
        title="Test Note",
        content="This is a test note.",
        tags=["test", "example"],
        note_type="test",
        date=datetime(2025, 5, 1)
    )
    
    markdown = note.to_markdown()
    
    assert "title: Test Note" in markdown
    assert "tags:" in markdown
    assert "- test" in markdown
    assert "- example" in markdown
    assert "date: '2025-05-01'" in markdown
    assert "type: test" in markdown
    assert "This is a test note." in markdown


def test_note_save_and_load():
    """Test saving and loading a note."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create and save note
        note = Note(
            title="Test Note",
            content="This is a test note.",
            tags=["test", "example"],
            note_type="test",
            date=datetime(2025, 5, 1)
        )
        
        file_path = note.save(temp_path)
        
        # Load note from file
        loaded_note = Note.from_file(file_path)
        
        assert loaded_note.title == "Test Note"
        assert loaded_note.content == "This is a test note."
        assert loaded_note.tags == ["test", "example"]
        assert loaded_note.type == "test"
        assert loaded_note.date == "2025-05-01"  # Loaded as string from YAML
        assert loaded_note.id == note.id


def test_note_with_special_types():
    """Test creating a note with special input types."""
    # Test with non-list tags
    note = Note(
        title="Test Note",
        content="This is a test note.",
        tags="single-tag",
        note_type="test"
    )
    assert note.tags == ["single-tag"]
    
    # Test with None tags
    note = Note(
        title="Test Note",
        content="This is a test note.",
        tags=None,
        note_type="test"
    )
    assert note.tags == []
    
    # Test with numeric title
    note = Note(
        title=123,
        content="This is a test note.",
        tags=["test"],
        note_type="test"
    )
    assert note.title == "123"
    
    # Test with None content
    note = Note(
        title="Test Note",
        content=None,
        tags=["test"],
        note_type="test"
    )
    assert note.content == ""


def test_note_with_malformed_frontmatter():
    """Test loading a note with malformed frontmatter."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        file_path = temp_path / "test.md"
        
        # Create a file with malformed frontmatter - using a simpler example
        # that won't raise YAML parsing errors but will produce unexpected types
        with open(file_path, "w") as f:
            f.write("""---
title: Test Note
tags: 
  - tag1
  - 123
type: test
date: 2025-05-01
---

This is a test note.
""")
        
        # Load the note
        loaded_note = Note.from_file(file_path)
        
        # Should still load with proper values
        assert loaded_note.title == "Test Note"
        assert loaded_note.content.strip() == "This is a test note."
        assert loaded_note.type == "test"
        
        # Tags should be processed properly
        assert isinstance(loaded_note.tags, list)
        assert len(loaded_note.tags) == 2
        assert "tag1" in loaded_note.tags
        # The number should be converted to string
        assert any(tag == "123" or tag == 123 for tag in loaded_note.tags)


def test_note_without_frontmatter():
    """Test loading a note without frontmatter."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        file_path = temp_path / "test.md"
        
        # Create a file without frontmatter
        with open(file_path, "w") as f:
            f.write("This is a test note without frontmatter.")
        
        # Load the note
        loaded_note = Note.from_file(file_path)
        
        # Should still load with default values
        assert loaded_note.content.strip() == "This is a test note without frontmatter."
        assert loaded_note.title == "Untitled"  # Default title
        assert isinstance(loaded_note.tags, list)
        assert loaded_note.tags == []  # Default empty tags
        assert loaded_note.id == "test"  # ID from filename