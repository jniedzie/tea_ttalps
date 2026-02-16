# Welcome to CMS tt+ALPs analysis

This repository contains analysis code based on [tea](cern.ch/tea) for Long-Lived Axion Like Particles (ALPs) produced in tt̄ events.

For code documentation, visit our [GitHub Wiki](https://github.com/jniedzie/tea_ttalps/wiki).

The notes for the analysis can be found in [CodiMD](https://codimd.web.cern.ch/s/v0JB7craB).

## Setup

- Create a directory and clone the repo:
```bash
mkdir tea_ttalps
cd tea_ttalps
git clone --recursive git@github.com:jniedzie/tea_ttalps.git
```
- build, assuming you already have a conda environment for tea (if not, visit the [tea website](https://jniedzie.github.io/tea/docs/prerequisites/) for more details):
```bash
conda activate tea
source tea/build.sh
```

Now you can run apps from the `bin` directory.
