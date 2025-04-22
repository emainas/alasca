<p align="center">
  <img src="assets/logo.png" width="120" alt="Alasca Logo">
</p>

<p align="center">
  <a href="https://pypi.org/project/alasca/">
    <img src="https://img.shields.io/pypi/v/alasca.svg" alt="PyPI version">
  </a>
  <a href="https://github.com/emainas/alasca/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/emainas/alasca/python-publish.yml?branch=main"
         alt="Build Status">
  </a>
  <a href="https://github.com/emainas/alasca/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/emainas/alasca.svg" alt="License">
  </a>
</p>

# Alasca

A thin Python wrapper around AmberTools’ `cpptraj` to:
1. compute non‑native contacts  
2. filter by occupancy ≥ 0.5  
3. list residue IDs for downstream alanine scanning  

> **Note:** Alasca invokes AmberTools’ `cpptraj` binary—you must have AmberTools installed.  
> Download AmberTools here: https://ambermd.org/AmberTools.php

## Quickstart

```bash
module load my-amber-module
export AMBERHOME=$(dirname "$(dirname "$(which cpptraj)")")
export PATH="$AMBERHOME/bin:$PATH"

module load anaconda
conda create -n alasca-env python=3.11
conda activate alasca-env
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .

alasca --help
alasca contacts -i config/contacts.yaml
```
