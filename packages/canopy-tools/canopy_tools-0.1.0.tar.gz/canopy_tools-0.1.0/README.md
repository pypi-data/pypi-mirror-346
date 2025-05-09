[![Docs Status](https://readthedocs.org/projects/canopy-tools/badge/?version=latest)](https://canopy-tools.readthedocs.io/en/latest/?badge=latest)

<img src="https://codebase.helmholtz.cloud/canopy/canopy/-/raw/main/docs/_static/canopylogo_small.png" alt="Canopy Logo" width="300" height="auto">

**canopy** is an open source python project designed to support research in the field of vegetation dynamics and climate modelling by providing tools for **analysing** and **visualising** Dynamic Global Vegetation Model (**DGVM**) **outputs**. 

# Installation

```bash
# Clone git repo
git clone https://codebase.helmholtz.cloud/canopy/canopy.git
cd canopy

# Create a conda environment
conda create --name canopy python=3.13
conda activate canopy

# Install the python libraries with conda using requirements file
conda install --file docs/requirements.txt --channel conda-forge
```

# Documentation

You can find the canopy documentation on [canopy-tools.readthedocs.io](https://canopy-tools.readthedocs.io/en/latest/index.html)

### How to use

You can use canopy in two modes:

- [Interactive mode](https://canopy-tools.readthedocs.io/en/latest/quick_start.html#interactive-mode), an intuitive and flexible mode, to analyse data and generate figures using python functions.

- [JSON mode](https://canopy-tools.readthedocs.io/en/latest/quick_start.html#json-mode), a easy-to-use and fast mode, to generate figures using a structured JSON configuration file.

### Technical documentation

- [Spatial Reduction Operations](https://canopy-tools.readthedocs.io/en/latest/technical_documentation.html#spatial-reduction-operations)

# Issue, questions or suggestions

If you find any bug, please report it on our [github issues](https://codebase.helmholtz.cloud/canopy/canopy/-/issues).

If you have any questions or suggestions, you can also reach the cano**py** community through [our mattermost](https://mattermost.imk-ifu.kit.edu/lpj-guess/channels/canopy---help-desk).

# Authors

This project is being developed by David M. Belda & Adrien Damseaux from the [Global Land Ecosystem Modelling Group](https://lemg.imk-ifu.kit.edu/) at the [Karlsruhe Institute of Technology](https://www.kit.edu/).