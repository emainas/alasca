# Alasca

A thin Python wrapper around AmberTools’ \`cpptraj\` to:
1. compute non‑native contacts  
2. filter by occupancy ≥ 0.5  
3. list residue IDs for downstream alanine scanning  

> **Note:** Alasca invokes AmberTools’ \`cpptraj\` binary—you must have AmberTools installed.  
> Download AmberTools here: https://ambermd.org/AmberTools.php

## Quickstart

```bash
module load amber/24
export AMBERHOME=\$(dirname "\$(dirname "\$(which cpptraj)")")
export PATH="\$AMBERHOME/bin:\$PATH"

module load anaconda
conda create -n alasca-env python=3.11
conda activate alasca-env 
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .

alasca --help
alasca --parmfile mon.prmtop --trajfile mon_prod.nc --frac_thresh 0.5
```
