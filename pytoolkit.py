#!/usr/bin/env python3
# MARK: - pytoolkit.py
#argParse.py
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description="PyToolkit text utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze", help="Analyze a text file")
    analyze.add_argument("-f", "--file", required=True, help="Input file")
    analyze.add_argument("-v", "--verbose", action="store_true")
    return parser

def analyze_file(path, verbose=False):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    print(f"Words: {len(words)}")
    if verbose:
        print(f"Characters: {len(text)}")

# MARK: - pytoolkit.py
#counterAndDict.py
#made with some code from the argparse assignment, labeled with #*

from collections import Counter, defaultdict

def word_stats(words):
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

# MARK: - pytoolkit.py
#contextMod.py
from contextlib import redirect_stdout
import io

def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            fileList = f.read()
            print(fileList)
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return ""

def capture_report(path):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")
    print(buffer.getvalue())
    return buffer.getvalue()

# MARK: - pytoolkit.py
#functools.py

from functools import lru_cache, partial, wraps

@lru_cache(maxsize=32)
def cached_word_count(text):
    with open(text) as text:
        words = text.read()
        print(len(words.split()))
        return len(words.split())

def log_call(fn):
    @wraps(fn) #commenting this out returns wrapper instead of call_log
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    print(wrapper)
    return wrapper

@log_call
def call_log():
    print("Calling all logs...")

analyze_short = partial(analyze_file, verbose=False)

# MARK: - pytoolkit.py
#ilib.py

import importlib

def load_plugin(name):
    module = importlib.import_module(f"pytoolkit.plugins.{name}")
    return module.apply

#MARK: - Call all functions with main()

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
        

if __name__ == "__main__":
    main()
