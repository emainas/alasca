#!/usr/bin/env python3
import subprocess
import sys
import yaml
import argparse


def load_config(path):
    """Load YAML config file into a dict."""
    with open(path) as f:
        return yaml.safe_load(f)


def run_cpptraj(parmfile, trajfile, ligand_mask, protein_mask, distance):
    """Invoke cpptraj with masks and distance from config."""
    cpp_input = f"""
parm {parmfile}
trajin {trajfile}
nativecontacts name NC1 {ligand_mask} {protein_mask} \
    writecontacts native-contacts.dat \
    distance {distance} \
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


def post_process(dat, contacts_txt, frac_txt, resid_txt, frac_thresh):
    """Strip headers, filter by fraction, and extract 2nd-group residue IDs."""
    lines = [l for l in open(dat) if not l.startswith("#")]
    with open(contacts_txt, "w") as f:
        f.writelines(lines)

    filtered = [l for l in lines if float(l.split()[3]) >= frac_thresh]
    with open(frac_txt, "w") as f:
        f.writelines(filtered)

    resids = {l.split()[1].split("_:")[-1].split("@")[0] for l in filtered}
    with open(resid_txt, "w") as f:
        for r in sorted(resids, key=int):
            f.write(r + "\n")
    print(f"Wrote {len(resids)} residues to {resid_txt}")


def main(config_path=None):
    """Entry point for 'alasca contacts' subcommand using a YAML config."""
    parser = argparse.ArgumentParser(prog="alasca contacts")
    parser.add_argument(
        "-i", "--config", required=True,
        help="Path to YAML config file"
    )
    args = parser.parse_args() if config_path is None else argparse.Namespace(config=config_path)
    cfg = load_config(args.config)

    # Required
    parmfile     = cfg["parmfile"]
    trajfile     = cfg["trajfile"]
    ligand_mask  = cfg["ligand_mask"]
    protein_mask = cfg["protein_mask"]

    # Optional with defaults
    distance     = cfg.get("distance", 3.0)
    frac_thresh  = cfg.get("fraction", 0.5)
    contacts_txt = cfg.get("contacts_txt", "contacts2.txt")
    frac_txt     = cfg.get("fraction_txt", "fraction.txt")
    resid_txt    = cfg.get("resid_txt", "2-resids.txt")

    run_cpptraj(parmfile, trajfile, ligand_mask, protein_mask, distance)
    post_process(
        "native-contacts.dat",
        contacts_txt,
        frac_txt,
        resid_txt,
        frac_thresh
    )


if __name__ == "__main__":
    main()
