#!/usr/bin/env python3
import subprocess
import sys
import yaml
import os


def load_config(path):
    """Load YAML config file into a dict."""
    with open(path) as f:
        return yaml.safe_load(f)


def renumber_pdb(input_pdb, output_pdb):
    """Ensure atom numbering in PDB is sequential."""
    with open(input_pdb) as fin, open(output_pdb, 'w') as fout:
        n = 1
        for line in fin:
            if line.startswith(('ATOM','HETATM')):
                fout.write(f"{line[:6]}{n:5d}{line[11:]}" )
                n += 1
            else:
                fout.write(line)
    print(f"Renumbered PDB written to {output_pdb}")


def run_mutation(pdbfile, resid, result_dir, mutation_resname):
    """Run cpptraj to mutate a single residue to the specified amino acid."""
    os.makedirs(result_dir, exist_ok=True)
    mutated_name = f"mutated_{resid}.pdb"
    out_path = os.path.join(result_dir, mutated_name)
    cpp_input = f"""
parm {pdbfile}
loadcrd {pdbfile} name edited
change crdset edited resname from :{resid} to {mutation_resname}
crdaction edited strip :{resid}&!(@N,CA,C,O,CB)
crdout edited {out_path}
go
"""
    proc = subprocess.run(["cpptraj"], input=cpp_input,
                          text=True, capture_output=True)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
    else:
        print(f"Wrote mutated PDB: {out_path}")


def main(config_path):
    """Entry point: load config and perform renumbering and mutations."""
    cfg = load_config(config_path)

    # Directories
    initial_dir = cfg.get("initial_dir", "initial_files")
    base = os.path.splitext(os.path.basename(config_path))[0]
    result_dir = os.path.join("result", base, "mutations")

    # Config parameters
    pdbfile_name     = cfg["pdbfile"]
    resid_file       = cfg["resid_file"]
    mutation_resname = cfg.get("mutation_resname", "ALA")

    # Full paths
    pdbfile      = os.path.join(initial_dir, pdbfile_name)
    renumbered_pdb = os.path.join(result_dir, f"{os.path.splitext(pdbfile_name)[0]}_renumbered.pdb")

    # Step 1: renumber PDB
    renumber_pdb(pdbfile, renumbered_pdb)

    # Step 2: load residue list
    with open(resid_file) as f:
        residues = [line.strip() for line in f if line.strip()]

    # Step 3: run mutations for each residue
    for resid in residues:
        run_mutation(renumbered_pdb, resid, result_dir, mutation_resname)

# Note: invoked via the `alasca mutate` console script in cli.py

