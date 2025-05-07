"""Replacer

Replace a target string with a replacement string.
"""

import os
import re
import click
from typing import Dict, List, Tuple, Optional

def replace_in_file(file_path: str, replacements: Dict[str, str], dry_run: bool = False) -> int:
    """
    Replace text in a single file according to the replacements dictionary.
    
    Args:
        file_path: Path to the file
        replacements: Dictionary of {search_text: replacement_text}
        dry_run: If True, only print what would be changed without making changes
    
    Returns:
        Number of replacements made
    """
    try:
        with open(file_path, 'r', errors='replace') as f:
            content = f.read()
        
        original_content = content
        replacement_count = 0
        
        # Apply each replacement in the dictionary
        for search_text, replace_text in replacements.items():
            # Use count to track number of replacements
            count_before = content.count(search_text)
            content = content.replace(search_text, replace_text)
            replacement_count += count_before - content.count(search_text)
        
        # Only write to the file if changes were made and not in dry-run mode
        if content != original_content and not dry_run:
            with open(file_path, 'w') as f:
                f.write(content)
        
        return replacement_count
    
    except Exception as e:
        click.echo(f"Error processing {file_path}: {e}", err=True)
        return 0

def is_binary(file_path: str) -> bool:
    """
    Check if a file is binary (vs text).
    
    Args:
        file_path: Path to file
    
    Returns:
        True if the file is likely binary
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk  # Simple heuristic: if null bytes, likely binary
    except Exception:
        return True  # If we can't read it, consider it binary

def process_directory(directory: str, 
                      replacements: Dict[str, str], 
                      extensions: Optional[List[str]] = None, 
                      exclude: Optional[List[str]] = None, 
                      dry_run: bool = False) -> Tuple[int, int, int]:
    """
    Recursively process files in a directory and its subdirectories.
    
    Args:
        directory: Directory to search
        replacements: Dictionary of {search_text: replacement_text}
        extensions: List of file extensions to process (None for all)
        exclude: List of directory or file patterns to exclude
        dry_run: If True, only print what would be changed without making changes
    
    Returns:
        Tuple of (files_processed, files_modified, total_replacements)
    """
    files_processed = 0
    files_modified = 0
    total_replacements = 0
    
    # Compile exclude patterns if provided
    exclude_patterns = None
    if exclude:
        exclude_patterns = [re.compile(pattern) for pattern in exclude]
    
    # Walk through directory
    for root, dirs, files in os.walk(directory):
        # Filter out excluded directories
        if exclude_patterns:
            dirs[:] = [d for d in dirs if not any(pattern.search(os.path.join(root, d)) for pattern in exclude_patterns)]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip excluded files
            if exclude_patterns and any(pattern.search(file_path) for pattern in exclude_patterns):
                continue
            
            # Filter by extension if specified
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue
            
            try:
                # Skip binary files
                if is_binary(file_path):
                    continue
                
                files_processed += 1
                
                # Process the file
                replacements_made = replace_in_file(file_path, replacements, dry_run)
                
                if replacements_made > 0:
                    files_modified += 1
                    total_replacements += replacements_made
                    
                    status = "Would modify" if dry_run else "Modified"
                    click.echo(f"{status}: {file_path} ({replacements_made} replacements)")
            
            except Exception as e:
                click.echo(f"Error processing {file_path}: {e}", err=True)
    
    return files_processed, files_modified, total_replacements

@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-r', '--replace', nargs=2, multiple=True, required=True,
              help='Pair of "search_text replacement_text" (can specify multiple times)')
@click.option('-e', '--ext', multiple=True,
              help='File extensions to process (can specify multiple times)')
@click.option('-x', '--exclude', multiple=True,
              help='Patterns to exclude (can specify multiple times)')
@click.option('--dry-run', is_flag=True,
              help='Print what would be changed without making changes')
def main(directory, replace, ext, exclude, dry_run):
    """Recursively replace text in files within DIRECTORY.
    
    Example: 
    
        python text_replacer.py /path/to/dir -r "old" "new" -r "Old" "New"
    """
    # Create replacements dictionary from tuples
    replacements = {search: replace for search, replace in replace}
    
    # Make extensions lowercase for case-insensitive matching
    extensions = [e.lower() if not e.startswith('.') else e for e in ext] if ext else None
    
    # Process directory
    click.echo(click.style(f"{'DRY RUN: ' if dry_run else ''}Processing directory: {directory}", fg="green"))
    click.echo(click.style(f"Replacements:", fg="blue"))
    for search, replace in replacements.items():
        click.echo(f"  '{search}' → '{replace}'")
    
    if extensions:
        click.echo(click.style(f"Extensions filter: {', '.join(extensions)}", fg="blue"))
    if exclude:
        click.echo(click.style(f"Exclusions: {', '.join(exclude)}", fg="blue"))
    
    with click.progressbar(length=1, label='Processing files') as bar:
        files_processed, files_modified, total_replacements = process_directory(
            directory, replacements, extensions, exclude, dry_run
        )
        bar.update(1)
    
    # Print summary
    action = "Would modify" if dry_run else "Modified"
    click.echo("\nSummary:")
    click.echo(f"Files processed: {files_processed}")
    click.echo(f"Files {action.lower()}: {files_modified}")
    click.echo(f"Total replacements: {total_replacements}")

if __name__ == "__main__":
    main()
