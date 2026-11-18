import argparse
from collections import Counter, defaultdict

def word_stats(words):
    with open(words) as words:#*
        counter = Counter(w.lower().strip(".,!?") for w in words if w)
        by_prefix = defaultdict(list)
        for w in counter:
            by_prefix[w[0]].append(w)
            if len(by_prefix) == 5:
                break
        print(counter)
        print(by_prefix)
        return counter, by_prefix

def build_parser(): #*
    parser = argparse.ArgumentParser(description="Counter and dict word displayer")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("count", help="View text file for counting")
    analyze.add_argument("-w", "--wordlist", required=True, help="Txt file with list of words")
    return parser

def main(): #*
    args = build_parser().parse_args()
    if args.command == "count":
        word_stats(args.wordlist)

if __name__ == "__main__": #*
    main()