#!/usr/bin/env python3
"""
Renamomicon Ex-Bulkus - The script of the dead
An Evil Dead themed bulk file renaming utility

Author: sorzkode
https://github.com/sorzkode

MIT License
Copyright (c) 2025 sorzkode
"""

import os
import re
import sys
import shutil
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
from tkinter import filedialog, Tk

import click

# ASCII Art Banner (Windows console compatible)
BANNER = r"""
 ____  _____ _   _    _    __  __  ___  __  __ ___ ____ ___  _   _
|  _ \| ____| \ | |  / \  |  \/  |/ _ \|  \/  |_ _/ ___/ _ \| \ | |
| |_) |  _| |  \| | / _ \ | |\/| | | | | |\/| || | |  | | | |  \| |
|  _ <| |___| |\  |/ ___ \| |  | | |_| | |  | || | |__| |_| | |\  |
|_| \_\_____|_| \_/_/   \_\_|  |_|\___/|_|  |_|___\____\___/|_| \_|

              _____  __     ____  _   _ _     _  ___   _ ____
             | ____| \ \   / __ )| | | | |   | |/ / | | / ___|
             |  _| |__\ \ / |__) | | | | |   | ' /| | | \___ \
             | |__|_____> |  __ /| |_| | |___| . \| |_| |___) |
             |_____|   /_/|_| \_\ \___/|_____|_|\_\\___/|____/
"""

TAGLINE = "The script of the dead... AKA an Evil Dead themed bulk file renaming utility"

# Configure logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class RenamexError(Exception):
    """Custom exception for Renamex errors."""
    pass


class Renamex:
    """Main class for bulk file renaming operations."""

    def __init__(self, log_file: Optional[str] = None, verbose: bool = False):
        """Initialize the Renamex instance.

        Args:
            log_file: Optional path to log file
            verbose: Enable verbose console output
        """
        self.logger = self._setup_logging(log_file, verbose)
        self._root = None

    def _setup_logging(self, log_file: Optional[str], verbose: bool) -> logging.Logger:
        """Configure logging for the application."""
        logger = logging.getLogger("renamex")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
        logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
            logger.addHandler(file_handler)

        return logger

    def _get_tk_root(self) -> Tk:
        """Get or create the Tk root window."""
        if self._root is None:
            self._root = Tk()
            self._root.withdraw()
        return self._root

    def select_directory(self, directory: Optional[str] = None) -> Path:
        """Select a directory via dialog or validate provided path.

        Args:
            directory: Optional directory path to use instead of dialog

        Returns:
            Path object for the selected directory

        Raises:
            RenamexError: If directory is invalid or not selected
        """
        if directory:
            dir_path = Path(directory)
            if not dir_path.exists():
                raise RenamexError(f"Directory does not exist: {directory}")
            if not dir_path.is_dir():
                raise RenamexError(f"Path is not a directory: {directory}")
            return dir_path

        self._get_tk_root()
        selected = filedialog.askdirectory(title="Select Directory for Renaming")

        if not selected:
            raise RenamexError("No directory selected. Operation cancelled.")

        return Path(selected)

    def get_files(self, directory: Path, pattern: Optional[str] = None,
                  extensions: Optional[List[str]] = None) -> List[Path]:
        """Get list of files in directory with optional filtering.

        Args:
            directory: Directory to scan
            pattern: Optional regex pattern to filter filenames
            extensions: Optional list of extensions to filter (e.g., ['.txt', '.pdf'])

        Returns:
            List of Path objects for matching files
        """
        files = []

        for item in directory.iterdir():
            if not item.is_file():
                continue

            # Extension filter
            if extensions:
                if item.suffix.lower() not in [ext.lower() for ext in extensions]:
                    continue

            # Pattern filter
            if pattern:
                try:
                    if not re.search(pattern, item.name):
                        continue
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern: {e}")
                    continue

            files.append(item)

        return sorted(files, key=lambda f: f.name.lower())

    def backup_files(self, files: List[Path], backup_dir: Optional[Path] = None) -> Path:
        """Create backups of files before renaming.

        Args:
            files: List of files to backup
            backup_dir: Optional custom backup directory

        Returns:
            Path to the backup directory
        """
        if not files:
            raise RenamexError("No files to backup.")

        source_dir = files[0].parent

        if backup_dir:
            backup_path = Path(backup_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = source_dir / f".renamex_backup_{timestamp}"

        backup_path.mkdir(parents=True, exist_ok=True)

        for file in files:
            dest = backup_path / file.name
            shutil.copy2(file, dest)
            self.logger.debug(f"Backed up: {file.name}")

        self.logger.info(f"Created backup of {len(files)} file(s) in: {backup_path}")
        return backup_path

    def preview_rename(self, renames: List[Tuple[Path, str]]) -> None:
        """Display preview of rename operations.

        Args:
            renames: List of (source_path, new_name) tuples
        """
        if not renames:
            click.echo("No files to rename.")
            return

        click.echo("\n" + "=" * 60)
        click.echo("RENAME PREVIEW")
        click.echo("=" * 60)

        for old_path, new_name in renames:
            click.echo(f"  {old_path.name}")
            click.echo(f"    -> {new_name}")

        click.echo("=" * 60)
        click.echo(f"Total: {len(renames)} file(s) to rename\n")

    def execute_rename(self, renames: List[Tuple[Path, str]],
                       dry_run: bool = False) -> Tuple[int, int]:
        """Execute the rename operations.

        Args:
            renames: List of (source_path, new_name) tuples
            dry_run: If True, only simulate the operations

        Returns:
            Tuple of (successful_count, failed_count)
        """
        success = 0
        failed = 0

        for old_path, new_name in renames:
            new_path = old_path.parent / new_name

            try:
                # Check for conflicts
                if new_path.exists() and new_path != old_path:
                    self.logger.warning(f"Skipping {old_path.name}: Target exists ({new_name})")
                    failed += 1
                    continue

                if not dry_run:
                    old_path.rename(new_path)
                    self.logger.debug(f"Renamed: {old_path.name} -> {new_name}")
                else:
                    self.logger.debug(f"[DRY RUN] Would rename: {old_path.name} -> {new_name}")

                success += 1

            except PermissionError:
                self.logger.error(f"Permission denied: {old_path.name}")
                failed += 1
            except OSError as e:
                self.logger.error(f"Failed to rename {old_path.name}: {e}")
                failed += 1

        return success, failed


# Interactive menu for when no command is provided
MENU_OPTIONS = [
    ("xspaces", "Remove spaces from filenames"),
    ("replacer", "Replace text in filenames"),
    ("upper", "Convert to UPPERCASE"),
    ("lower", "Convert to lowercase"),
    ("titlecase", "Convert to Title Case"),
    ("date", "Add date to filenames"),
    ("prefix", "Add prefix to filenames"),
    ("suffix", "Add suffix to filenames"),
    ("number", "Add sequential numbers"),
    ("sanitize", "Remove special characters"),
    ("extension", "Change file extensions"),
    ("restore", "Restore from backup"),
]


def show_interactive_menu(ctx):
    """Display interactive menu and execute selected command."""
    click.echo(BANNER)
    click.echo(TAGLINE)
    click.echo("\n" + "=" * 50)
    click.echo("SELECT AN OPERATION:")
    click.echo("=" * 50)

    for i, (cmd, desc) in enumerate(MENU_OPTIONS, 1):
        click.echo(f"  {i:2}. {desc}")

    click.echo(f"  {len(MENU_OPTIONS) + 1:2}. Exit")
    click.echo("=" * 50)

    while True:
        try:
            choice = click.prompt("\nEnter choice", type=int)

            if choice == len(MENU_OPTIONS) + 1:
                click.echo("Goodbye! Shop smart, shop S-Mart!")
                return

            if 1 <= choice <= len(MENU_OPTIONS):
                cmd_name = MENU_OPTIONS[choice - 1][0]
                click.echo(f"\nRunning: {cmd_name}\n")

                # Get the command and invoke it
                cmd = cli.get_command(ctx, cmd_name)
                if cmd:
                    ctx.invoke(cmd)

                # After command completes, ask if they want to continue
                click.echo("\n" + "=" * 50)
                if not click.confirm("Run another operation?", default=True):
                    click.echo("Groovy! Catch you later.")
                    return

                # Show menu again
                click.echo("\n" + "=" * 50)
                click.echo("SELECT AN OPERATION:")
                click.echo("=" * 50)
                for i, (cmd, desc) in enumerate(MENU_OPTIONS, 1):
                    click.echo(f"  {i:2}. {desc}")
                click.echo(f"  {len(MENU_OPTIONS) + 1:2}. Exit")
                click.echo("=" * 50)
            else:
                click.echo("Invalid choice. Try again.")

        except click.Abort:
            click.echo("\nOperation cancelled.")
            return
        except (ValueError, click.exceptions.BadParameter):
            click.echo("Please enter a valid number.")


# Click CLI Application
@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version information")
@click.option("--log-file", "-l", type=click.Path(), help="Log operations to file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, version, log_file, verbose):
    """Renamomicon Ex-Bulkus - The script of the dead.

    An Evil Dead themed bulk file renaming utility.
    """
    if version:
        click.echo("Renamomicon Ex-Bulkus v2.1.0")
        ctx.exit()

    ctx.ensure_object(dict)
    ctx.obj["log_file"] = log_file
    ctx.obj["verbose"] = verbose

    # Show interactive menu if no command provided
    if ctx.invoked_subcommand is None:
        show_interactive_menu(ctx)


def common_options(func):
    """Decorator for common command options."""
    func = click.option("--directory", "-d", type=click.Path(exists=True),
                       help="Directory to process (opens dialog if not specified)")(func)
    func = click.option("--backup/--no-backup", "-b", default=True,
                       help="Create backup before renaming (default: enabled)")(func)
    func = click.option("--dry-run", is_flag=True,
                       help="Preview changes without applying them")(func)
    func = click.option("--yes", "-y", is_flag=True,
                       help="Skip confirmation prompt")(func)
    func = click.option("--pattern", "-p",
                       help="Regex pattern to filter files")(func)
    func = click.option("--extensions", "-e", multiple=True,
                       help="File extensions to include (e.g., -e .txt -e .pdf)")(func)
    return func


def get_renamex(ctx) -> Renamex:
    """Create Renamex instance from context."""
    return Renamex(
        log_file=ctx.obj.get("log_file"),
        verbose=ctx.obj.get("verbose", False)
    )


def process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform_func, operation_name: str):
    """Common processing logic for rename commands."""
    click.echo(BANNER)

    rx = get_renamex(ctx)

    try:
        # Select directory
        dir_path = rx.select_directory(directory)
        click.echo(f"Processing directory: {dir_path}")

        # Get files
        ext_list = list(extensions) if extensions else None
        files = rx.get_files(dir_path, pattern=pattern, extensions=ext_list)

        if not files:
            click.echo("No files found matching criteria. Hail to the king, baby!")
            return

        click.echo(f"Found {len(files)} file(s)")

        # Generate renames
        renames = transform_func(files)

        if not renames:
            click.echo("No files need renaming. Groovy!")
            return

        # Preview
        rx.preview_rename(renames)

        # Confirmation
        if not yes and not dry_run:
            if not click.confirm("Proceed with renaming?", default=False):
                click.echo("Operation cancelled. Shop smart, shop S-Mart!")
                return

        # Backup
        if backup and not dry_run:
            rx.backup_files([r[0] for r in renames])

        # Execute
        success, failed = rx.execute_rename(renames, dry_run=dry_run)

        # Summary
        if dry_run:
            click.echo(f"\n[DRY RUN] Would rename {success} file(s)")
        else:
            click.echo(f"\nGroovy! Renamed {success} file(s)")
            if failed:
                click.echo(f"Failed: {failed} file(s)")

    except RenamexError as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
    except KeyboardInterrupt:
        click.echo("\nOperation interrupted by user.")
        ctx.exit(1)


@cli.command(name="xspaces")
@common_options
@click.pass_context
def remove_spaces(ctx, directory, backup, dry_run, yes, pattern, extensions):
    """Obliterate spaces from filenames using your trusty boomstick!"""

    def transform(files):
        renames = []
        for f in files:
            if " " in f.name:
                new_name = f.name.replace(" ", "")
                renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "space removal")


@cli.command(name="replacer")
@common_options
@click.option("--find", "-f", prompt="Text to find (case sensitive)",
              help="Text to replace in filenames")
@click.option("--replace", "-r", prompt="Replace with",
              help="Replacement text")
@click.option("--regex", is_flag=True, help="Treat find pattern as regex")
@click.pass_context
def replacer(ctx, directory, backup, dry_run, yes, pattern, extensions, find, replace, regex):
    """Replace part of filenames. Give me some sugar, baby!"""

    def transform(files):
        renames = []
        for f in files:
            stem = f.stem
            ext = f.suffix

            if regex:
                try:
                    new_stem = re.sub(find, replace, stem)
                except re.error as e:
                    click.echo(f"Invalid regex: {e}", err=True)
                    return []
            else:
                new_stem = stem.replace(find, replace)

            if new_stem != stem:
                renames.append((f, new_stem + ext))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "text replacement")


@cli.command(name="upper")
@common_options
@click.pass_context
def uppercase(ctx, directory, backup, dry_run, yes, pattern, extensions):
    """UPgrade filenames to shiny uppercase lettering."""

    def transform(files):
        renames = []
        for f in files:
            new_name = f.stem.upper() + f.suffix
            if new_name != f.name:
                renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "uppercase conversion")


@cli.command(name="lower")
@common_options
@click.pass_context
def lowercase(ctx, directory, backup, dry_run, yes, pattern, extensions):
    """Cut filenames down to size with lowercase."""

    def transform(files):
        renames = []
        for f in files:
            new_name = f.stem.lower() + f.suffix
            if new_name != f.name:
                renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "lowercase conversion")


@cli.command(name="date")
@common_options
@click.option("--delimiter", "-D", default="_",
              help="Delimiter before date (default: _)")
@click.option("--format", "-F", "date_format", default="%Y%m%d",
              help="Date format (default: %%Y%%m%%d)")
@click.option("--prepend", is_flag=True, help="Add date at beginning instead of end")
@click.pass_context
def add_date(ctx, directory, backup, dry_run, yes, pattern, extensions,
             delimiter, date_format, prepend):
    """Add today's date to filenames. Time to tell them what time it is!"""

    date_str = datetime.now().strftime(date_format)

    def transform(files):
        renames = []
        for f in files:
            stem = f.stem
            ext = f.suffix

            if prepend:
                new_stem = f"{date_str}{delimiter}{stem}"
            else:
                new_stem = f"{stem}{delimiter}{date_str}"

            renames.append((f, new_stem + ext))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "date addition")


@cli.command(name="prefix")
@common_options
@click.option("--text", "-t", prompt="Prefix text",
              help="Text to add at the beginning of filenames")
@click.pass_context
def add_prefix(ctx, directory, backup, dry_run, yes, pattern, extensions, text):
    """Add prefix text to filenames."""

    def transform(files):
        renames = []
        for f in files:
            new_name = text + f.name
            renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "prefix addition")


@cli.command(name="suffix")
@common_options
@click.option("--text", "-t", prompt="Suffix text",
              help="Text to add before the extension")
@click.pass_context
def add_suffix(ctx, directory, backup, dry_run, yes, pattern, extensions, text):
    """Add suffix text to filenames (before extension)."""

    def transform(files):
        renames = []
        for f in files:
            new_name = f.stem + text + f.suffix
            renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "suffix addition")


@cli.command(name="number")
@common_options
@click.option("--start", "-s", default=1, help="Starting number (default: 1)")
@click.option("--padding", "-P", default=3, help="Zero-padding width (default: 3)")
@click.option("--template", "-t", default="{name}_{num}",
              help="Naming template. Use {name}, {num}, {ext} (default: {name}_{num})")
@click.pass_context
def add_numbers(ctx, directory, backup, dry_run, yes, pattern, extensions,
                start, padding, template):
    """Add sequential numbers to filenames."""

    def transform(files):
        renames = []
        for i, f in enumerate(files, start=start):
            num_str = str(i).zfill(padding)
            new_stem = template.format(name=f.stem, num=num_str, ext=f.suffix)

            # Handle extension in template
            if "{ext}" in template:
                new_name = new_stem
            else:
                new_name = new_stem + f.suffix

            renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "numbering")


@cli.command(name="titlecase")
@common_options
@click.pass_context
def titlecase(ctx, directory, backup, dry_run, yes, pattern, extensions):
    """Convert filenames to Title Case."""

    def transform(files):
        renames = []
        for f in files:
            new_name = f.stem.title() + f.suffix
            if new_name != f.name:
                renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "title case conversion")


@cli.command(name="sanitize")
@common_options
@click.option("--replacement", "-R", default="_",
              help="Replacement for invalid characters (default: _)")
@click.pass_context
def sanitize(ctx, directory, backup, dry_run, yes, pattern, extensions, replacement):
    """Remove or replace special characters from filenames."""

    # Characters that are problematic across platforms
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'

    def transform(files):
        renames = []
        for f in files:
            new_stem = re.sub(invalid_chars, replacement, f.stem)
            # Remove multiple consecutive replacements
            new_stem = re.sub(f"{re.escape(replacement)}+", replacement, new_stem)
            # Remove leading/trailing replacements
            new_stem = new_stem.strip(replacement)

            new_name = new_stem + f.suffix
            if new_name != f.name:
                renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "filename sanitization")


@cli.command(name="extension")
@common_options
@click.option("--new-ext", "-n", prompt="New extension (include dot, e.g., .txt)",
              help="New file extension")
@click.pass_context
def change_extension(ctx, directory, backup, dry_run, yes, pattern, extensions, new_ext):
    """Change file extensions. Deadites hate this one trick!"""

    if not new_ext.startswith("."):
        new_ext = "." + new_ext

    def transform(files):
        renames = []
        for f in files:
            new_name = f.stem + new_ext
            if new_name != f.name:
                renames.append((f, new_name))
        return renames

    process_command(ctx, directory, backup, dry_run, yes, pattern, extensions,
                    transform, "extension change")


@cli.command(name="restore")
@click.option("--backup-dir", "-b", type=click.Path(exists=True), required=True,
              help="Backup directory to restore from")
@click.option("--target-dir", "-t", type=click.Path(exists=True),
              help="Target directory (default: parent of backup)")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@click.pass_context
def restore_backup(ctx, backup_dir, target_dir, yes):
    """Restore files from a backup directory."""
    click.echo(BANNER)

    backup_path = Path(backup_dir)

    if target_dir:
        target_path = Path(target_dir)
    else:
        target_path = backup_path.parent

    files = list(backup_path.iterdir())
    files = [f for f in files if f.is_file()]

    if not files:
        click.echo("No files found in backup directory.")
        return

    click.echo(f"Backup directory: {backup_path}")
    click.echo(f"Target directory: {target_path}")
    click.echo(f"Files to restore: {len(files)}")

    if not yes:
        if not click.confirm("Proceed with restoration?", default=False):
            click.echo("Operation cancelled.")
            return

    restored = 0
    for f in files:
        dest = target_path / f.name
        try:
            shutil.copy2(f, dest)
            restored += 1
        except Exception as e:
            click.echo(f"Failed to restore {f.name}: {e}", err=True)

    click.echo(f"Groovy! Restored {restored} file(s)")


def main():
    """Entry point for the application."""
    cli(obj={})


if __name__ == "__main__":
    main()