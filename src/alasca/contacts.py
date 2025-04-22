#!/usr/bin/env python3
import subprocess
import sys

def run_cpptraj(parmfile, trajfile):
    """Run cpptraj to compute non-native contacts."""
    cpp_input = f"""
parm {parmfile}
trajin {trajfile}
nativecontacts name NC1 :170 :1-169 \\
    writecontacts native-contacts.dat \\
    distance 3.0 \\
    skipnative
go
"""
    proc = subprocess.run(
        ["cpptraj"], input=cpp_input,
        text=True, capture_output=True
    )
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        sys.exit(proc.returncode)
    print(proc.stdout)

def post_process(dat, contacts_txt, frac_txt, resid_txt, thresh):
    """Strip headers, filter by fraction, and extract 2nd-group residue IDs."""
    lines = [l for l in open(dat) if not l.startswith("#")]
    with open(contacts_txt, "w") as f:
        f.writelines(lines)

    filtered = [l for l in lines if float(l.split()[3]) >= thresh]
    with open(frac_txt, "w") as f:
        f.writelines(filtered)

    resids = {
        l.split()[1].split("_:")[-1].split("@")[0]
        for l in filtered
    }
    with open(resid_txt, "w") as f:
        for r in sorted(resids, key=int):
            f.write(r + "\n")

    print(f"Wrote {len(resids)} residues to {resid_txt}")

def run(parmfile, trajfile, frac_thresh=0.5,
        contacts_txt="contacts2.txt",
        frac_txt="fraction.txt",
        resid_txt="2-resids.txt"):
    """
    Entry point for the `alasca contacts` subcommand.

    Parameters
    ----------
    parmfile : str
        Amber topology file (.prmtop)
    trajfile : str
        Amber trajectory file (.nc)
    frac_thresh : float
        minimum contact fraction to report
    contacts_txt : str
        filename for the stripped native-contacts output
    frac_txt : str
        filename for the filtered fraction output
    resid_txt : str
        filename for the residue-ID list
    """
    run_cpptraj(parmfile, trajfile)
    post_process("native-contacts.dat",
                 contacts_txt, frac_txt, resid_txt, frac_thresh)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="alasca contacts")
    parser.add_argument("--parmfile",    default="mon.prmtop")
    parser.add_argument("--trajfile",    default="mon_prod.nc")
    parser.add_argument("--frac_thresh", type=float, default=0.5)
    parser.add_argument("--contacts_txt",default="contacts2.txt")
    parser.add_argument("--frac_txt",    default="fraction.txt")
    parser.add_argument("--resid_txt",   default="2-resids.txt")
    args = parser.parse_args()

    run(
        parmfile    = args.parmfile,
        trajfile    = args.trajfile,
        frac_thresh = args.frac_thresh,
        contacts_txt= args.contacts_txt,
        frac_txt    = args.frac_txt,
        resid_txt   = args.resid_txt,
    )

