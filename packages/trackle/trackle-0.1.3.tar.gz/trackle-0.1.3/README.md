# trackle

A personal, offline knowledge logging and retrieval system using local markdown files and semantic search powered by embeddings.

## Features

- Create, store, and search markdown knowledge notes
- Semantic search using sentence embeddings
- Local-first design with FAISS vector storage
- Completely offline, no LLM dependencies

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd trackle

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install the package
pip install -e .
```

## Usage

### Interactive Shell

Simply run `trackle` without any arguments to enter the main interactive shell:

```bash
trackle
```

From there, you can access specialized shells for notes and todos:

```
trackle> note    # Enter note management shell
trackle> todo    # Enter todo management shell
```

You can also access these shells directly:

```bash
trackle note    # Enter note management shell
trackle todo    # Enter todo management shell
```

Features:
- Prompt with command history (arrow up/down)
- Tab completion for commands and IDs
- Direct command entry (e.g., `query kubernetes`, `view note1`)
- Exit with `exit`, `quit`, or Ctrl+D

### Command Mode

You can also use the CLI in command mode for both notes and todos:

#### Note commands

```bash
trackle note new          # Create a new note
trackle note list         # List all notes
trackle note reindex      # Rebuild the search index
trackle note query "text" # Search for notes
trackle note view <id>    # View a specific note
```

#### Todo commands

```bash
trackle todo new           # Create a new todo
trackle todo list          # List all todos
trackle todo today         # Show todos due today
trackle todo view <id>     # View a specific todo
trackle todo done <id>     # Mark a todo as completed
```

You can also use the legacy direct commands for notes which are maintained for backward compatibility:

```bash
trackle new          # Create a new note
trackle list         # List all notes
trackle reindex      # Rebuild the search index
trackle query "text" # Search for notes
trackle view <id>    # View a specific note
```

### Create a new note

```bash
trackle new
```

You will be prompted for a title, tags, and an editor will open for content input.

### Rebuild the search index

After adding new notes, rebuild the search index:

```bash
trackle reindex
```

### Search for notes

```bash
trackle query "how to migrate to java 17"
```

### View a specific note

```bash
trackle view <note-id>
```

### List all notes

```bash
trackle list
```

## File Structure

- Notes are stored as markdown files in `~/trackle/store/`
- Each note includes YAML frontmatter with metadata
- Vector index is stored in `~/trackle/.index/`

## Example Note Format

```markdown
---
title: Migrate to Java 17
tags: [java, migration]
date: 2025-05-01
type: migration
---

##### Context
Need to upgrade all services to Java 17 due to EOL.

##### Steps
- Upgrade Gradle toolchain
- Refactor `javax.*` usages
```