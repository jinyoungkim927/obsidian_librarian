# Obsidian Librarian

![Obsidian Librarian](readme_assets/librarians.webp){width=50%}

Obsidian Librarian is a package that gives you more time for real thinking by:

1. Formatting your notes correctly
2. Pointing out gaps in understanding
3. Shortlisting interesting connections between ideas

## Installation

```bash
pip install obsidian-librarian
```

## Usage

```bash
olib [command] [subcommand] [options]
```

### Global Options

- `--tags`, `-t`     Filter by tags (e.g., `--tags economy,history`)
- `--notes`, `-n`    Specify note names
- `--period`, `-p`   Time period (default: last 24h)
- `--help`, `-h`     Show help message
- `--version`, `-v`  Show version number

### Commands

```bash
# Core Commands
format              Format notes and convert screenshots to text
check               Run various checks on notes
  accuracy          Check note accuracy and completeness
  private           Detect private/sensitive content

search              Search and analyze notes
  semantic          Perform semantic search across notes
  prereq            Identify missing prerequisites

# Note Management
notes               Note manipulation commands
  format            Format individual notes
  fill              Complete partial notes
  ocr               Convert screenshots to text

# System
analytics           Display note-taking analytics dashboard
config              Manage configuration
  prompt            Configure formatting prompts
history             Show command history
undo                Revert last command
```

# TODO: add edit_global which is a general command like "find notes related to X and change the content Y"

# TODO: add --revise flag or something to create a clone of the MD file with the changes, not directly editing the original file

## Philosophy

Read more about the philosophy behind Obsidian Librarian [here](https://google.com).

- **Effective Learning**: Notes should enhance learning through:
  - Building atomic knowledge
  - Fostering creative connections

- **Deliberate Understanding**: Learning must be effortful:
  - Document clear understanding
  - Explicitly mark gaps for further study

## License

MIT License. See [LICENSE](LICENSE) for details.
