[![CodeQL](https://github.com/sorzkode/renamex/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/sorzkode/renamex/actions/workflows/codeql-analysis.yml)
[[PyPI Package](https://pypi.org/project/renamex/)]
[[MIT Licence](https://en.wikipedia.org/wiki/MIT_License)]


![alt text](https://raw.githubusercontent.com/sorzkode/renamex/master/assets/reblogo.png)

# Renamomicon Ex-Bulkus

The script of the dead...AKA an Evil Dead themed bulk renaming utility.

## Features

- **Backup Support**: Automatic backup before renaming (enabled by default)
- **Dry Run Mode**: Preview changes without applying them
- **Confirmation Prompts**: Verify operations before execution
- **Logging**: Optional file logging for audit trails
- **File Filtering**: Filter by regex pattern or file extensions
- **Multiple Operations**: 12+ renaming commands available

## Installation

Install from PyPI:
```bash
pip install renamex
```

Or install from source:
```bash
git clone https://github.com/sorzkode/renamex.git
cd renamex
pip install -e .
```

## Requirements

- Python 3.8+
- click
- tkinter (included with Python on Windows, may need separate install on Linux)

## Usage

```
Usage: renamex [OPTIONS] COMMAND [ARGS]...

  Renamomicon Ex-Bulkus - The script of the dead.
  An Evil Dead themed bulk file renaming utility.

Options:
  -v, --version   Show version information
  -l, --log-file  Log operations to file
  --verbose       Enable verbose output
  --help          Show this message and exit.

Commands:
  date       Add today's date to filenames
  extension  Change file extensions
  lower      Convert filenames to lowercase
  number     Add sequential numbers to filenames
  prefix     Add prefix text to filenames
  replacer   Replace part of filenames (supports regex)
  restore    Restore files from a backup directory
  sanitize   Remove/replace special characters from filenames
  suffix     Add suffix text to filenames
  titlecase  Convert filenames to Title Case
  upper      Convert filenames to uppercase
  xspaces    Remove spaces from filenames
```

### Common Options (available on most commands)

| Option | Description |
|--------|-------------|
| `-d, --directory` | Directory to process (opens dialog if not specified) |
| `-b, --backup/--no-backup` | Create backup before renaming (default: enabled) |
| `--dry-run` | Preview changes without applying them |
| `-y, --yes` | Skip confirmation prompt |
| `-p, --pattern` | Regex pattern to filter files |
| `-e, --extensions` | File extensions to include (e.g., `-e .txt -e .pdf`) |

### Examples

Remove spaces from filenames:
```bash
renamex xspaces -d /path/to/files
```

Replace text in filenames (with regex support):
```bash
renamex replacer -d /path/to/files -f "old" -r "new"
renamex replacer -d /path/to/files -f "IMG_(\d+)" -r "photo_\1" --regex
```

Add date to filenames:
```bash
renamex date -d /path/to/files --delimiter "_" --format "%Y-%m-%d"
```

Add sequential numbers:
```bash
renamex number -d /path/to/files --start 1 --padding 4 --template "{num}_{name}"
```

Dry run (preview without changes):
```bash
renamex upper -d /path/to/files --dry-run
```

Process only specific file types:
```bash
renamex lower -d /path/to/files -e .jpg -e .png
```

Restore from backup:
```bash
renamex restore -b /path/to/.renamex_backup_20231201_143022
```
