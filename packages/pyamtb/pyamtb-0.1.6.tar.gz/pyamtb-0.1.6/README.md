# PyAMTB

A Python package for tight-binding model calculations for altermagnets.

## Introduction

PyAMTB (Python Altermagnet Tight Binding) is built on top of the PythTB package, providing specialized tight-binding model calculations for altermagnets. It extends PythTB's capabilities by adding direct support for POSCAR structure files and altermagnet-specific features.

## Features

- Tight-binding model calculations for altermagnets
- Support for various lattice structures
- Band structure calculations
- Easy configuration through TOML files
- Command-line interface for quick calculations

## Installation

### From PyPI

```bash
pip install pyamtb
```

### From source

```bash
git clone https://github.com/ooteki-teo/pyamtb.git
cd pyamtb
pip install -e .
```

## Usage

### Command Line Interface

The package provides a command-line interface for easy calculations:

```bash
# Show help and available commands
pyamtb --help

# Calculate distances between atoms
pyamtb distance -p POSCAR 

# create a template.toml file
pyamtb template 

# Calculate band structure using configuration file
pyamtb calculate -c config.toml -p POSCAR

```

### Configuration

The package uses TOML files for configuration. Here's an example configuration file (`config.toml`):

```toml
poscar_filename = "CrSb.vasp" # POSCAR filename / POSCAR文件名
output_filename = "CrSb" # Output band structure filename (default png format) / 输出能带图文件名，默认png格式
output_format = "png" # Output format (default png) / 输出格式，默认png格式
savedir = "." # Save directory / 保存路径

# Model parameters / 建模参数
use_elements = ["Cr", "Sb"] # Elements to model / 需要建模的元素
t0 = 1.0                # Reference hopping strength / 参考跃迁强度
t0_distance = 2.74749 # Reference hopping distance for t0 / 参考跃迁距离，指定t0的距离
hopping_decay = 2       # Hopping decay coefficient / 跃迁衰减系数，
# t = t0*exp(-hopping_decay*(r-t0_distance)/t0_distance)
onsite_energy = [0.0, 0.0, 0.0, 0.0] # On-site energy for each atom / 每个原子的在位能
min_distance = 0.1      # Minimum hopping distance / 最小跃迁距离，小于这个距离不考虑跃迁
max_distance = 5      # Maximum hopping distance / 最大跃迁距离，超出此距离不考虑跃迁
max_R_range = 2       # Maximum number of neighbor sites, R search range / 最大相邻格点数, R的搜寻范围
dimk = 3                # k-space dimension / k空间维度
dimr = 3                # r-space dimension, keep it to 3 for POSCAR / r空间维度， 一般不要改，因为POSCAR都是3维的

# Magnetic parameters / 磁性参数
nspin = 2 # Spin (1 for no spinor, 2 for spinor) / 自旋，1表示没有自旋，2表示有自旋
magnetic_moment = 1  # Magnetic moment / 磁矩大小
magnetic_order = "+-00" # Magnetic order (+ up, - down, 0 none) / 磁序，+表示向上，-表示向下，0表示没有磁性

# Define k-point path / 定义k点路径
kpath_filename = "KPATH.in" # KPATH filename / KPATH文件名, if defined, kpath and klabel will be ommited
nkpt=1000 # Number of k-points / 定义k点数目


# Other parameters / 其他参数
is_print_tb_model_hop = true # Print tight-binding model hopping info / 是否打印紧束缚模型信息
is_print_tb_model = true # Print tight-binding model / 是否打印紧束缚模型
is_check_flat_bands = true # Check for flat bands / 是否检查平带
is_black_degenerate_bands = true # Black degenerate bands / 是否用黑色画简并带
is_report_kpath = true # Report k-path / 是否报告k点路径
energy_threshold = 1e-5 # 简并能带判断阈值
```

### Python API

You can also use the package in your Python code:

```python
from pyamtb import Parameters, calculate_band_structure, create_pythtb_model

# Load parameters from TOML file
params = Parameters("config.toml")

# Create pythtb tight-binding model
model = create_pythtb_model("POSCAR", params)  # this is pythtb tb_model, you may use it for furthur study.

# Calculate band structure
calculate_band_structure(model, params)
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{pyamtb,
  author = {Dinghui Wang, Junting Zhang, Yu Xie},
  title = {PyAMTB: A Python package for tight-binding model calculations},
  year = {2025},
  url = {https://github.com/ooteki-teo/pyamtb.git}
}
``` 