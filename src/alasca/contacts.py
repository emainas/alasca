#!/usr/bin/env python3
import subprocess
import sys
import yaml
import argparse
import os


def load_config(path):
    """Load YAML config file into a dict."""
    with open(path) as f:
        return yaml.safe_load(f)


def run_cpptraj(parmfile, trajfile, ligand_mask, protein_mask, distance, result_dir):
    """Invoke cpptraj with masks and distance from config, writing output to result_dir."""
    os.makedirs(result_dir, exist_ok=True)
    dat_path = os.path.join(result_dir, "native-contacts.dat")
    cpp_input = f"""
parm {parmfile}
trajin {trajfile}
nativecontacts name NC1 {ligand_mask} {protein_mask} \
    writecontacts {dat_path} \
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
    return dat_path


def post_process(dat_path, contacts_txt, frac_txt, resid_txt, frac_thresh, result_dir):
    """Strip headers, filter by fraction, and extract 2nd-group residue IDs into result_dir."""
    os.makedirs(result_dir, exist_ok=True)
    with open(dat_path) as f:
        lines = [l for l in f if not l.startswith("#")]

    contacts_out = os.path.join(result_dir, contacts_txt)
    with open(contacts_out, "w") as f:
        f.writelines(lines)

    filtered = [l for l in lines if float(l.split()[3]) >= frac_thresh]
    frac_out = os.path.join(result_dir, frac_txt)
    with open(frac_out, "w") as f:
        f.writelines(filtered)

    resids = {l.split()[1].split("_:")[-1].split("@")[0] for l in filtered}
    resid_out = os.path.join(result_dir, resid_txt)
    with open(resid_out, "w") as f:
        for r in sorted(resids, key=int):
            f.write(r + "\n")

    print(f"Wrote {len(resids)} residues to {resid_out}")


def main():
    """Entry point for 'alasca contacts' subcommand using a YAML config."""
    parser = argparse.ArgumentParser(prog="alasca contacts")
    parser.add_argument(
        "-i", "--config", required=True,
        help="Path to YAML config file"
    )
    parser.add_argument(
        "--slurm", choices=["yes","no"], default=None,
        help="Override Slurm submission: yes|no (default=from config)"
    )
    args = parser.parse_args()
    cfg = load_config(args.config)

    # determine result directory from config filename
    base = os.path.splitext(os.path.basename(args.config))[0]
    result_dir = os.path.join("result", base)

    use_slurm = args.slurm if args.slurm is not None else cfg.get("slurm", "no")
    if use_slurm.lower() == "yes":
        # optionally handle SLURM here or defer
        print("SLURM submission not yet implemented")
        sys.exit(0)

    # load config values
    parmfile     = cfg["parmfile"]
    trajfile     = cfg["trajfile"]
    ligand_mask  = cfg["ligand_mask"]
    protein_mask = cfg["protein_mask"]
    distance     = cfg.get("distance", 3.0)
    frac_thresh  = cfg.get("fraction", 0.5)
    contacts_txt = cfg.get("contacts_txt", "contacts2.txt")
    frac_txt     = cfg.get("fraction_txt", "fraction.txt")
    resid_txt    = cfg.get("resid_txt", "2-resids.txt")

    # run analysis
    dat_path = run_cpptraj(
        parmfile, trajfile, ligand_mask,
        protein_mask, distance, result_dir
    )
    post_process(
        dat_path,
        contacts_txt, frac_txt, resid_txt,
        frac_thresh, result_dir
    )

if __name__ == "__main__":
    main()
