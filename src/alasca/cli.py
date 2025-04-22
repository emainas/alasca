#!/usr/bin/env python3
import argparse
from .contacts import run as contacts_run
# from .other    import main as other_run   # uncomment when you add other.py

def main():
    parser = argparse.ArgumentParser(prog="alasca")
    subs = parser.add_subparsers(dest="cmd", required=True)

    # ── contacts ───────────────────────────────────────
    c = subs.add_parser("contacts", help="run non‑native contact analysis")
    c.add_argument("--parmfile",    default="mon.prmtop")
    c.add_argument("--trajfile",    default="mon_prod.nc")
    c.add_argument("--frac_thresh", type=float, default=0.5)
    c.add_argument("--contacts_txt",default="contacts2.txt")
    c.add_argument("--frac_txt",    default="fraction.txt")
    c.add_argument("--resid_txt",   default="2-resids.txt")

    # ── other (example) ────────────────────────────────
    # o = subs.add_parser("other", help="run the other workflow")
    # o.add_argument("--foo", required=True)

    args = parser.parse_args()

    if args.cmd == "contacts":
        contacts_run(
            parmfile    = args.parmfile,
            trajfile    = args.trajfile,
            frac_thresh = args.frac_thresh,
            contacts_txt= args.contacts_txt,
            frac_txt    = args.frac_txt,
            resid_txt   = args.resid_txt,
        )
    # elif args.cmd == "other":
    #     other_run(args.foo)

if __name__ == "__main__":
    main()
