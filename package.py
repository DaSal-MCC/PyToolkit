#!/usr/bin/env python3
# MARK: - pytoolkit.py
#Insert into cli.py

import argparse
from . import stats
from .stats import (word_stats, analyze_file, safe_read, capture_report, cached_word_count, \
log_call, call_log, analyze_short, load_plugin, read_lines, count_lines, parse_log_line)

def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    return parser

def main():
    args = build_parser().parse_args()
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: {args.file} not found")
        return ""
    
    if args.command == "analyze":
        analyze_file(args.file, args.verbose)
        word_stats(args.file)
        safe_read(args.file)
        capture_report(args.file)
        cached_word_count(args.file)
        call_log()
        print(call_log.__name__)
        analyze_short(args.file)
        load_plugin("uppercase")
        count_lines(args.file)
        words = text.split()
        for prefix, group in prefix_groups(words):
            print
        word_pairs(args.file)
        parse_log_line(args.file)

if __name__ == "__main__":
    main()

# MARK: - pytoolkit.py
#Insert into stats.py
#made with some code from the argparse assignment, labeled with #*
from collections import Counter, defaultdict
from collections.abc import Iterator

def word_stats(words: list[str]) -> tuple[Counter, dict]:
    """Prints the 5 most common words in a file, and how many times they appear, together 
    as a list."""
    with open(words) as words:#*
        text = words.read()#*
        words = text.split()
        counter = Counter(w.lower().strip(".,!?") for w in words if w)
        by_prefix = defaultdict(list)
        for w in counter:
            by_prefix[w[0]].append(w)
        print(counter.most_common(5))
        print(by_prefix)
        return counter, by_prefix

def analyze_file(path: str, verbose=False) -> str:
    """Prints the number of words in a file, along with the total characters if verbose is 
    true."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    print(f"Words: {len(words)}")
    if verbose:
        print(f"Characters: {len(text)}")

# MARK: - pytoolkit.py

from contextlib import redirect_stdout
import io

def safe_read(path: str) -> str:
    """Prints out each line in a file."""
    try:
        with open(path, encoding="utf-8") as f:
            fileList = f.read()
            print(fileList)
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return ""

def capture_report(path: str) -> io:
    """Prints the StringIO buffer from the analyzed file"""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")
    print(buffer.getvalue())
    return buffer.getvalue()

# MARK: - pytoolkit.py

from functools import lru_cache, partial, wraps

@lru_cache(maxsize=32)
def cached_word_count(text: str) -> int:
    """Prints only the number of words in a file"""
    with open(text) as text:
        words = text.read()
        print(len(words.split()))
        return len(words.split())

def log_call(fn: function) -> str:
    """Main function that prints function args"""
    @wraps(fn) #commenting this out returns wrapper instead of call_log
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    print(wrapper)
    return wrapper

@log_call
def call_log() -> str:
    """Wrapped function that prints a statement and also calls the log_call function"""
    print("Calling all logs...")

analyze_short = partial(analyze_file, verbose=False)

# MARK: - pytoolkit.py

import importlib

def load_plugin(name: str) -> str:
    """Loads a .py file from the plugins folder"""
    module = importlib.import_module(f"pytoolkit.plugins.{name}")
    return module.apply("hello")

# MARK: - pytoolkit.py

def read_lines(path: str) -> Iterator[str]:
    """Yield stripped lines from a text file."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

def count_lines(path: str) -> int:
    """Counts the number of yielded lines from the read_lines function."""
    print(sum(1 for _ in read_lines(path)))
    return sum(1 for _ in read_lines(path))

# MARK: - pytoolkit.py

from itertools import groupby, combinations

def prefix_groups(words: str) -> Iterator[str, list[str]]:
    """Prints a list of letter prefixes, then the list of words that start with 
    those prefixes."""
    for prefix, group in groupby(sorted(words), key=lambda w: w[0]):
        grouped = list(group)
        print(prefix, grouped)
        yield prefix, list(group)


def word_pairs(words: str, n=2) -> list:
    """Prints every possible pair of letters taken from the file name."""
    val = list(combinations(words[:6], n))
    print (val)
    return val

# MARK: - pytoolkit.py

import re

LOG_PATTERN = re.compile(
    r"(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<msg>.*)"
)

def parse_log_line(line: str) -> str:
    """Prints all errors and warnings in a line, or 'none' if there aren't any in a line.
    Then, it prints the total amount of errors and warnings."""
    err_count = 0

    try: #taken from safe_read()
        with open(line, encoding="utf-8") as f:
            for text in f:
                m = LOG_PATTERN.match(text)
                if m:
                    err_count = err_count + 1
                print(m.groupdict()) if m else print("None")
    except FileNotFoundError:
        print("Error: Could not find file or file does not exist")
    print(f"Total errors and warnings: {err_count}")
    return ""
    #return m.groupdict() if m else None