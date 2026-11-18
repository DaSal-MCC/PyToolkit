from contextlib import redirect_stdout
import io
import argparse

def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            print(f.read())
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return ""

def capture_report(path):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(f"Analyzing {path}")
    print(buffer.getvalue())
    return buffer.getvalue()



def build_parser():
    parser = argparse.ArgumentParser(description="Contextlib tester")
    sub = parser.add_subparsers(dest="command", required=True)
    sRead = sub.add_parser("safeRead", help="Attempt to view a file, and get an error if it fails.")
    sRead.add_argument("-w", "--wordlist", required=True, help="Txt file with list of words")
    cReport = sub.add_parser("captureReport", help="Analyze a file and print it's values.")
    cReport.add_argument("-w", "--wordlist", required=True, help="Txt file with list of words")
    return parser

def main():
    args = build_parser().parse_args()
    if args.command == "safeRead":
        safe_read(args.wordlist)
    if args.command == "captureReport":
        capture_report(args.wordlist)

if __name__ == "__main__":
    main()