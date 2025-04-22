#!/usr/bin/env python3
import subprocess, sys

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

