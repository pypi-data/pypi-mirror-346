"""
Storage module for handling notes and vector index.
"""
import json
import os
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .note import Note

class KnowledgeStore:
    """Class for storing and retrieving knowledge notes."""
    
    DEFAULT_STORE_DIR = Path.home() / "trackle" / "store"
    DEFAULT_INDEX_DIR = Path.home() / "trackle" / ".index"
    MODEL_NAME = "all-MiniLM-L6-v2"
    
    def __init__(
        self,
        store_dir: Optional[Path] = None,
        index_dir: Optional[Path] = None,
        model_name: Optional[str] = None
    ):
        self.store_dir = store_dir or self.DEFAULT_STORE_DIR
        self.index_dir = index_dir or self.DEFAULT_INDEX_DIR
        self.model_name = model_name or self.MODEL_NAME
        self.model = None
        self.index = None
        self.metadata = {}  # UUID -> filepath mapping
        self.last_index_time = 0  # Timestamp of last index build
        
        # Create directories if they don't exist
        os.makedirs(self.store_dir, exist_ok=True)
        os.makedirs(self.index_dir, exist_ok=True)
        
        # Create index timestamp file path
        self.index_timestamp_path = self.index_dir / "last_index_time.txt"
        
        # Load the last index time if it exists
        if self.index_timestamp_path.exists():
            try:
                with open(self.index_timestamp_path, "r") as f:
                    self.last_index_time = float(f.read().strip())
            except Exception:
                # If the file is invalid, default to 0
                self.last_index_time = 0
    
    def _load_model(self):
        """Load the sentence transformer model."""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
    
    def create_note(self, title: str, content: str, tags: List[str], note_type: str) -> Note:
        """Create a new note and save it."""
        note = Note(title=title, content=content, tags=tags, note_type=note_type)
        note.save(self.store_dir)
        return note
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID."""
        # Sanitize note_id - remove any spaces or unwanted characters
        note_id = str(note_id).strip()
        
        # Try both with and without .md extension
        file_path = self.store_dir / f"{note_id}.md"
        if file_path.exists():
            print(f"Found note at: {file_path}")
            return Note.from_file(file_path)
            
        # Try without .md if it was included
        if note_id.endswith('.md'):
            note_id = note_id[:-3]
            file_path = self.store_dir / f"{note_id}.md"
            if file_path.exists():
                print(f"Found note at: {file_path}")
                return Note.from_file(file_path)
                
        # Try partial match
        print(f"File not found at: {file_path}")
        return None
        
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID."""
        # Sanitize note_id - remove any spaces or unwanted characters
        note_id = str(note_id).strip()
        
        # Try both with and without .md extension
        file_path = self.store_dir / f"{note_id}.md"
        if file_path.exists():
            file_path.unlink()  # Delete the file
            return True
            
        # Try without .md if it was included
        if note_id.endswith('.md'):
            note_id = note_id[:-3]
            file_path = self.store_dir / f"{note_id}.md"
            if file_path.exists():
                file_path.unlink()  # Delete the file
                return True
                
        # File not found
        return False
    
    def list_notes(self) -> List[Note]:
        """List all notes."""
        notes = []
        for file_path in self.store_dir.glob("*.md"):
            notes.append(Note.from_file(file_path))
        return notes
    
    def _encode_text(self, text: str) -> np.ndarray:
        """Encode text to vector using the sentence transformer model."""
        self._load_model()
        return self.model.encode(text)
    
    def build_index(self) -> None:
        """Build the vector index for all notes."""
        self._load_model()
        notes = self.list_notes()
        
        if not notes:
            print("No notes found. Index not built.")
            return
        
        # Clear previous metadata
        self.metadata = {}
        
        # Encode all notes
        texts = []
        for note in notes:
            # Combine title and content for better semantic representation
            text = f"{note.title}\n\n{note.content}"
            texts.append(text)
            
            # Store metadata mapping
            self.metadata[note.id] = {
                "id": note.id,
                "title": note.title,
                "path": str(self.store_dir / f"{note.id}.md"),
                "type": note.type,
                "tags": note.tags,
                "date": note.date.strftime("%Y-%m-%d") if hasattr(note.date, "strftime") else note.date
            }
        
        # Create embeddings
        embeddings = self.model.encode(texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add vectors to the index
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Save the index and metadata
        self._save_index()
    
    def _save_index(self) -> None:
        """Save the index and metadata to disk."""
        if self.index is None:
            return
        
        # Save FAISS index
        index_path = self.index_dir / "vector.index"
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata
        metadata_path = self.index_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f)
            
        # Update timestamp
        self.last_index_time = time.time()
        with open(self.index_timestamp_path, "w") as f:
            f.write(str(self.last_index_time))
    
    def _load_index(self) -> bool:
        """Load the index and metadata from disk."""
        index_path = self.index_dir / "vector.index"
        metadata_path = self.index_dir / "metadata.json"
        
        if not index_path.exists() or not metadata_path.exists():
            return False
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_path))
        
        # Load metadata
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)
        
        return True
    
    def needs_reindex(self) -> bool:
        """Check if the index needs to be updated based on file modifications."""
        # If index doesn't exist, definitely need reindex
        index_path = self.index_dir / "vector.index"
        metadata_path = self.index_dir / "metadata.json"
        if not index_path.exists() or not metadata_path.exists():
            return True
            
        # Check if any markdown files have been added or modified since last index
        markdown_files = list(self.store_dir.glob("*.md"))
        
        # Check if we have any files
        if not markdown_files:
            return False
            
        # Check if any files were modified since last index
        for file_path in markdown_files:
            # Get the last modification time of the file
            mtime = file_path.stat().st_mtime
            
            # If file is newer than last index time, reindex
            if mtime > self.last_index_time:
                return True
                
        # Check if any files in index don't exist anymore
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Check if any indexed files have been deleted
                for note_id, meta in metadata.items():
                    file_path = Path(meta.get("path", ""))
                    if not file_path.exists():
                        return True
            except Exception:
                # If there's an error reading metadata, assume reindex needed
                return True
                
        return False
    
    def query(self, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the vector index for similar notes."""
        if not self._load_index():
            raise RuntimeError("Index not found. Please run 'trackle reindex' first.")
        
        # Print some debug info
        print(f"Loaded index with {self.index.ntotal} vectors")
        print(f"Metadata contains {len(self.metadata)} entries")
        
        try:
            self._load_model()
            
            # Encode query
            query_vector = self._encode_text(query_text)
            query_vector = np.array([query_vector]).astype('float32')
            
            # Search
            if self.index.ntotal == 0:
                # No vectors in index
                return []
                
            print(f"Searching for: {query_text}")
            distances, indices = self.index.search(query_vector, min(k, self.index.ntotal))
            
            # Get results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1 and idx < len(self.metadata):
                    note_id = list(self.metadata.keys())[idx]
                    metadata = self.metadata[note_id]
                    results.append({
                        "id": note_id,
                        "title": metadata["title"],
                        "score": float(1.0 / (1.0 + distances[0][i])),
                        "date": metadata["date"],
                        "type": metadata["type"],
                        "tags": metadata["tags"]
                    })
            
            return results
        except Exception as e:
            print(f"Error during query: {str(e)}")
            raise RuntimeError(f"Query failed: {str(e)}")