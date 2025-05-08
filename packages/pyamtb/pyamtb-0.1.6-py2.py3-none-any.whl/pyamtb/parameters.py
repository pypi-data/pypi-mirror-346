"""
Parameters class for tight-binding model calculations.
"""

import numpy as np
import tomlkit
from typing import List, Dict, Any, Optional
from .read_datas import read_parameters, read_kpath
import os
import warnings

class Parameters:
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize parameters from configuration file.
        
        Args:
            config_file (str, optional): Path to the configuration file. If None, uses default parameters.
        """
        if config_file is None:
            # 使用默认配置
            self._initialize_default_parameters()
        else:
            self.tbparas = read_parameters(config_file)
            self._initialize_parameters()
            self._validate_kpath_dimensions()

    def _initialize_default_parameters(self):
        """Initialize parameters with default values."""
        self.a0 = 1.0
        self.t0 = 1.0
        self.t0_distance = 2.0
        self.sigma_z = np.array([[1, 0], [0, -1]])
        self.mindist = 0.1
        self.maxdistance = 2.6
        self.onsite_energy = [0.0, 0.0, 0.0]
        self.dimk = 2
        self.dimr = 3
        self.nspin = 2
        self.lambda_ = 1.0
        self.same_atom_negative_coupling = False
        self.magnetic_moment = 0.1
        self.magnetic_order = "+-0"
        self.use_elements = ["Mn", "N"]
        self.savedir = "."
        self.poscar = "POSCAR"
        self.output_filename = "model"
        self.output_format = "png"
        self.kpath_filename = None
        self.kpath = [[0, 0], [0.5, 0], [0.5, 0.5], [0.0, 0.5], [0.0, 0.0], [0.5, 0.5]]
        self.klabel = ["G", "X", "M", "Y", "G", "M"]
        self.num_k_points = 100
        self.max_R_range = 2
        self.is_print_tb_model_hop = True
        self.is_check_flat_bands = True
        self.is_print_tb_model = True
        self.is_black_degenerate_bands = True
        self.ylim = [-1, 1]
        self.energy_threshold = 1e-5
        self.is_report_kpath = False
    
    def _validate_kpath_dimensions(self):
        """
        Validate and adjust k-path dimensions based on dimk value.
        Removes extra dimensions from k-path points if dimk is less than the k-path point dimensions.
        """
        if not self.kpath:
            return
            
        # Convert kpath points to numpy array for easier slicing
        kpath_array = np.array(self.kpath)
        
        # Get current k-path dimensions
        current_dims = kpath_array.shape[1]
        
        # Check if dimensions need to be adjusted
        if current_dims > self.dimk:
            # Slice kpath to keep only dimk dimensions
            self.kpath = kpath_array[:, :self.dimk].tolist()
        elif current_dims < self.dimk:
            warnings.warn(f"K-path has fewer dimensions than dimk, padding with zeros")
            # Pad with zeros if k-path has fewer dimensions than dimk
            padded_kpath = np.pad(kpath_array, 
                                ((0, 0), (0, self.dimk - current_dims)),
                                mode='constant',
                                constant_values=0)
            self.kpath = padded_kpath.tolist()

    def _initialize_parameters(self):
        """Initialize all parameters from the configuration file."""
        # Lattice and distance parameters
        self.poscar = self.tbparas["poscar_filename"]
        self.a0 = self.tbparas["lattice_constant"]
        self.t0 = self.tbparas["t0"]
        self.t0_distance = self.tbparas["t0_distance"]
        
        # Physical parameters
        self.sigma_z = np.array([[1, 0], [0, -1]])
        self.min_distance = self.tbparas["min_distance"]
        self.max_distance = self.tbparas["max_distance"]
        self.onsite_energy = self.tbparas["onsite_energy"]
        
        # Model dimensions - ensure these are integers
        self.dimk = int(self.tbparas["dimk"])
        self.dimr = int(self.tbparas["dimr"])
        self.nspin = int(self.tbparas["nspin"])
        
        # Hopping parameters
        self.hopping_decay = self.tbparas["hopping_decay"]
        self.same_atom_negative_coupling = self.tbparas["same_atom_negative_coupling"]
        
        # Magnetic parameters
        self.magnetic_moment = self.tbparas["magnetic_moment"]
        self.magnetic_order = self.tbparas["magnetic_order"]
        
        # Element selection
        self.use_elements = self.tbparas["use_elements"]
        
        # Output parameters
        self.savedir = self.tbparas["savedir"]
        self.output_filename = self.tbparas["output_filename"]
        self.output_format = self.tbparas["output_format"]
        
        # k-path parameters
        if self.tbparas.get("kpath_filename") is not None:
            self.kpath, self.klabel = read_kpath(self.tbparas["kpath_filename"])
            self.kpath_filename = self.tbparas["kpath_filename"]
        else:
            self.kpath = self.tbparas["kpath"]
            self.klabel = self.tbparas["klabel"]
        self.is_report_kpath = self.tbparas["is_report_kpath"]
        self.num_k_points = int(self.tbparas["nkpt"])
        
        # Plot parameters
        self.ylim = self.tbparas["ylim"]
        
        # Neighbor parameters
        self.max_R_range = int(self.tbparas["max_R_range"])

        # other parameters
        self.is_print_tb_model_hop = self.tbparas["is_print_tb_model_hop"]
        self.is_check_flat_bands = self.tbparas["is_check_flat_bands"]
        self.is_print_tb_model = self.tbparas["is_print_tb_model"]
        self.is_black_degenerate_bands = self.tbparas["is_black_degenerate_bands"]
        self.energy_threshold = self.tbparas["energy_threshold"]

    def get_maglist(self) -> List[float]:
        """
        Convert magnetic order string to list of magnetic moments.
        
        Returns:
            List[float]: List of magnetic moments
        """
        return [self.magnetic_moment if c == '+' else -self.magnetic_moment if c == '-' else 0 
                for c in self.magnetic_order]

# Create a global instance with default parameters
params = Parameters() 