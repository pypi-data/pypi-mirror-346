# cutflow_compare

## Overview
`cutflow_compare` is a Python package designed to compare cutflow histograms from ROOT files. It provides a straightforward command-line interface for users to analyze and visualize differences in cutflow data across different regions.

## Features
- Compare cutflow histograms from multiple ROOT files.
- Generate a CSV report of the comparison results.
- Easy to use with command-line arguments for file input and region selection.

## Installation
You can install the package using pip:

```
pip install cutflow_compare
```

## Usage

After installation, you can use the command-line tool directly:

```
cutflow_compare --files histoOut-compared.root histoOut-reference.root -r region1 region2 region3
```

Or, if running from source:

```
python cutflow_compare.py --files histoOut-compared.root histoOut-reference.root -r region1 region2 region3
```

### Note: 
Make sure the same regions are present in both files with the same name.

### Arguments
- `--files`: List of input ROOT files to compare.
- `--regions`: List of regions to compare within the cutflow histograms.

## Example
```bash
cutflow_compare --files histoOut-compared.root histoOut-reference.root -r WZ
```

This command will compare the specified regions in the two provided ROOT files and output the results to `cutflow_comparison_result.csv`.

## Requirements

- Python 3.6+
- [ROOT](https://root.cern/) (must be installed separately, e.g., via conda: `conda install -c conda-forge root`)
- pandas

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## Acknowledgments
This package utilizes the ROOT framework for data analysis and visualization.
