# src/alasca/cli.py
#!/usr/bin/env python3
import argparse
from .contacts import main as contacts_main
from .mutate import main as mutate_main

def main():
    parser = argparse.ArgumentParser(prog="alasca")
    subs = parser.add_subparsers(dest="cmd", required=True)

    c = subs.add_parser("contacts", help="run non-native contact analysis from config")
    c.add_argument("-i", "--config", required=True, help="YAML config file")
    m = subs.add_parser("mutate", help="perform alanine mutations from config")
    m.add_argument("-i", "--config", required=True, help="YAML config file")

    args = parser.parse_args()
    if args.cmd == "contacts":
        contacts_main(args.config)
    elif args.cmd == "mutate":
        mutate_main(args.config)

if __name__ == "__main__":
    main()
