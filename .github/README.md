# Welcome to CMS tt+ALPs analysis

This repository contains analysis code based on [tea](cern.ch/tea) for Long-Lived Axion Like Particles (ALPs) produced in tt̄ events.

For code documentation, visit our [GitHub Wiki](https://github.com/jniedzie/tea_ttalps/wiki).

The notes for the analysis can be found in [CodiMD](https://codimd.web.cern.ch/s/v0JB7craB).

## Setup

- Create a directory and clone the repo:
```bash
mkdir tea_ttalps
cd tea_ttalps
git clone git@github.com:jniedzie/tea_ttalps.git .
```

- Register tea as a submodule and update it to the latest version:
```bash
git rm tea
git submodule add git@github.com:jniedzie/tea.git tea
./tea/update.sh
```

- build, assuming you already have a conda environment for tea (if not, visit [code documentation](https://github.com/jniedzie/tea_ttalps/wiki) or [tea website](cern.ch/tea) for more details):
```bash
conda activate tea
./tea/build.sh
```

Now you can run apps from the `bin` directory.
