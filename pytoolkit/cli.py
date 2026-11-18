#!/usr/bin/env python3
#python -m pytoolkit.cli analyze -f sample.txt
# MARK: - pytoolkit.py
#argParse.py
import argparse
from . import stats
from .stats import (word_stats, analyze_file, safe_read, capture_report, cached_word_count, \
log_call, call_log, analyze_short, load_plugin, read_lines, count_lines, prefix_groups, \
word_pairs, parse_log_line)

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
        print("Press any key to proceed with the command.")
        answer = input()

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
