import re
import os
import sys
import argparse
from typing import List, Dict, Any, Union, Iterator, Optional, Pattern, Tuple
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore, Style
import fnmatch

class GrepyMatch:
    """Represents a single match found by grepy."""

    def __init__(self, filename: str, line_number: int, line: str, match: str, column: int):
        self.filename = filename
        self.line_number = line_number
        self.line = line
        self.match = match
        self.column = column

    def __str__(self) -> str:
        return f"{self.filename}:{self.line_number}:{self.column}: {self.line}"

class Grepy:
    """A grep-like tool with enhanced features."""

    def __init__(self):
        colorama.init()

    def search_file(self, filename: str, pattern: Pattern, options: Dict[str, Any]) -> List[GrepyMatch]:
        """Search for pattern in a single file."""
        if not os.path.isfile(filename):
            if options.get('verbose'):
                print(f"Warning: {filename} is not a file or cannot be accessed", file=sys.stderr)
            return []

        try:
            with open(filename, 'r', encoding='utf-8', errors='replace') as file:
                matches = []
                lines = file.readlines()
                for line_number, line in enumerate(lines, start=1):
                    if options.get('invert_match'):
                        if not pattern.search(line):
                            matches.append(GrepyMatch(filename, line_number, line.rstrip(), "", 0))
                        continue

                    for match in pattern.finditer(line):
                        if options.get('match_word') and not (
                            (match.start() == 0 or not line[match.start()-1].isalnum()) and
                            (match.end() == len(line) or not line[match.end()].isalnum())
                        ):
                            continue

                        matches.append(GrepyMatch(
                            filename, line_number, line.rstrip(), match.group(0), match.start() + 1
                        ))

                        if options.get('first_match_only'):
                            break

                return matches
        except Exception as e:
            if options.get('verbose'):
                print(f"Error reading {filename}: {str(e)}", file=sys.stderr)
            return []

    def search_directory(self, directory: str, pattern: Pattern, options: Dict[str, Any]) -> List[GrepyMatch]:
        """Recursively search directory for files matching pattern."""
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            if options.get('exclude_dir'):
                dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, pattern) for pattern in options.get('exclude_dir'))]

            for filename in filenames:
                if options.get('include') and not any(fnmatch.fnmatch(filename, pattern) for pattern in options.get('include')):
                    continue
                if options.get('exclude') and any(fnmatch.fnmatch(filename, pattern) for pattern in options.get('exclude')):
                    continue

                file_path = os.path.join(root, filename)
                matches.extend(self.search_file(file_path, pattern, options))

                if options.get('max_results') and len(matches) >= options.get('max_results'):
                    return matches[:options.get('max_results')]

        return matches

    def search(self, pattern_str: str, paths: List[str], options: Dict[str, Any] = None) -> List[GrepyMatch]:
        """Search for pattern in specified paths."""
        if options is None:
            options = {}

        # Compile regex pattern
        try:
            flags = re.IGNORECASE if options.get('ignore_case') else 0
            flags |= re.MULTILINE if options.get('multiline') else 0
            pattern = re.compile(pattern_str, flags)
        except re.error as e:
            raise ValueError(f"Invalid regular expression: {str(e)}")

        all_matches = []

        # Use thread pool for parallel processing if specified
        if options.get('parallel') and len(paths) > 1:
            with ThreadPoolExecutor(max_workers=options.get('workers', os.cpu_count())) as executor:
                futures = []
                for path in paths:
                    if os.path.isdir(path) and options.get('recursive'):
                        futures.append(executor.submit(self.search_directory, path, pattern, options))
                    elif os.path.isfile(path):
                        futures.append(executor.submit(self.search_file, path, pattern, options))

                for future in futures:
                    all_matches.extend(future.result())
        else:
            for path in paths:
                if os.path.isdir(path):
                    if options.get('recursive'):
                        all_matches.extend(self.search_directory(path, pattern, options))
                    elif options.get('verbose'):
                        print(f"Skipping directory {path} (use -r for recursive search)", file=sys.stderr)
                elif os.path.isfile(path):
                    all_matches.extend(self.search_file(path, pattern, options))
                else:
                    if options.get('verbose'):
                        print(f"Warning: {path} does not exist or is not accessible", file=sys.stderr)

        # Sort results if requested
        if options.get('sort_by_filename'):
            all_matches.sort(key=lambda m: (m.filename, m.line_number))

        # Limit results if max_results is set
        if options.get('max_results') and len(all_matches) > options.get('max_results'):
            all_matches = all_matches[:options.get('max_results')]

        return all_matches

    def format_match(self, match: GrepyMatch, options: Dict[str, Any], context_lines: List[str] = None) -> str:
        """Format a match according to the specified options."""
        result = ""

        # Show filename if multiple files or explicitly requested
        if options.get('show_filename'):
            result += f"{match.filename}:"

        # Show line number if requested
        if options.get('line_numbers'):
            result += f"{match.line_number}:"

        # Show column if requested
        if options.get('show_column'):
            result += f"{match.column}:"

        # Add padding if we added any prefix
        if result:
            result += " "

        # Format the line with highlighted match
        if options.get('highlight') and match.match:
            before = match.line[:match.column-1]
            highlight = match.line[match.column-1:match.column-1+len(match.match)]
            after = match.line[match.column-1+len(match.match):]
            result += f"{before}{Fore.RED}{Style.BRIGHT}{highlight}{Style.RESET_ALL}{Fore.RESET}{after}"
        else:
            result += match.line

        # Add context lines if requested
        if context_lines:
            result += "\n" + "\n".join(context_lines)

        return result

    def print_results(self, matches: List[GrepyMatch], options: Dict[str, Any]) -> None:
        """Print formatted search results."""
        for match in matches:
            context_lines = []
            if options.get('context_lines'):
                context = options.get('context_lines')
                start = max(1, match.line_number - context)
                end = match.line_number + context
                with open(match.filename, 'r', encoding='utf-8', errors='replace') as file:
                    lines = file.readlines()
                    context_lines = [line.rstrip() for line in lines[start-1:end] if line.rstrip() != match.line]
            print(self.format_match(match, options, context_lines))

        if options.get('summary'):
            print(f"\n{Fore.BLUE}Found {len(matches)} matches{Fore.RESET}")

    def anarchy(self):
        """Prints 'Prabh - Kesar'."""
        print("Prabh - Kesar")

def main():
    parser = argparse.ArgumentParser(description='Grepy - Enhanced grep-like tool')

    # Pattern and file inputs
    parser.add_argument('pattern', nargs='?', help='Pattern to search for')
    parser.add_argument('paths', nargs='*', default=['.'], help='Files or directories to search')

    # Common grep options
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Case insensitive search')
    parser.add_argument('-r', '--recursive', action='store_true', help='Search directories recursively')
    parser.add_argument('-v', '--invert-match', action='store_true', help='Show lines that do not match')
    parser.add_argument('-n', '--line-numbers', action='store_true', help='Show line numbers')
    parser.add_argument('-w', '--word', dest='match_word', action='store_true', help='Match whole words only')
    parser.add_argument('-m', '--max-count', dest='max_results', type=int, help='Stop after NUM matches')

    # Enhanced features
    parser.add_argument('-p', '--parallel', action='store_true', help='Use parallel processing')
    parser.add_argument('--workers', type=int, default=os.cpu_count(), help='Number of worker threads for parallel processing')
    parser.add_argument('--highlight', action='store_true', help='Highlight matching text')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    parser.add_argument('--sort', dest='sort_by_filename', action='store_true', help='Sort results by filename')
    parser.add_argument('--column', dest='show_column', action='store_true', help='Show column number of match')
    parser.add_argument('--first-only', dest='first_match_only', action='store_true', help='Only show first match per file')
    parser.add_argument('--summary', action='store_true', help='Show summary of matches')
    parser.add_argument('--multiline', action='store_true', help='Enable multiline regex matching')
    parser.add_argument('--include', action='append', help='Only search files matching GLOB')
    parser.add_argument('--exclude', action='append', help='Skip files matching GLOB')
    parser.add_argument('--exclude-dir', action='append', help='Skip directories matching GLOB')
    parser.add_argument('--filename', dest='show_filename', action='store_true', help='Always show filename')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--context', dest='context_lines', type=int, default=0, help='Show NUM lines of context around matches')
    parser.add_argument('--anarchy', action='store_true', help='Prints "Prabh - Kesar"')

    args = parser.parse_args()

    # Disable colors if requested or if output is not a tty
    if args.no_color or not sys.stdout.isatty():
        colorama.deinit()
        args.highlight = False

    # Convert args to options dict
    options = vars(args)

    # Always show filename if searching multiple paths
    if len(args.paths) > 1 and not options.get('show_filename'):
        options['show_filename'] = True

    try:
        grepy = Grepy()
        if args.anarchy:
            grepy.anarchy()
        else:
            if not args.pattern:
                parser.error("Pattern is required unless using --anarchy")
            matches = grepy.search(args.pattern, args.paths, options)
            grepy.print_results(matches, options)

            # Exit with appropriate status code
            sys.exit(0 if matches else 1)
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("Search interrupted by user", file=sys.stderr)
        sys.exit(130)

if __name__ == '__main__':
    main()
