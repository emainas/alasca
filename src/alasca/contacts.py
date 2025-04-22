#!/usr/bin/env python3
import subprocess, sys, argparse

def run_cpptraj(parmfile, trajfile):
    cpp_input = f"""
parm {parmfile}
trajin {trajfile}
nativecontacts name NC1 :170 :1-169 \\
    writecontacts native-contacts.dat \\
    distance 3.0 \\
    skipnative
go
"""
    p = subprocess.run(["cpptraj"], input=cpp_input,
                       text=True, capture_output=True)
    if p.returncode:
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)
    print(p.stdout)

def post_process(dat, contacts_txt, frac_txt, resid_txt, thresh):
    lines = [l for l in open(dat) if not l.startswith("#")]
    open(contacts_txt, "w").writelines(lines)
    filtered = [l for l in lines if float(l.split()[3]) >= thresh]
    open(frac_txt, "w").writelines(filtered)
    res = {l.split()[1].split("_:")[-1].split("@")[0] for l in filtered}
    with open(resid_txt, "w") as f:
        for r in sorted(res, key=int):
            f.write(r + "\n")
    print(f"Wrote {len(res)} residues to {resid_txt}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--parmfile", default="mon.prmtop")
    p.add_argument("--trajfile", default="mon_prod.nc")
    p.add_argument("--frac_thresh", type=float, default=0.5)
    p.add_argument("--contacts_txt", default="contacts2.txt")
    p.add_argument("--frac_txt",    default="fraction.txt")
    p.add_argument("--resid_txt",   default="2-resids.txt")
    args = p.parse_args()

    run_cpptraj(args.parmfile, args.trajfile)
    post_process("native-contacts.dat",
                 args.contacts_txt,
                 args.frac_txt,
                 args.resid_txt,
                 args.frac_thresh)

if __name__ == "__main__":
    main()
