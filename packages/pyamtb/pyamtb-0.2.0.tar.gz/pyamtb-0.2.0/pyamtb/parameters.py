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
        # Always initialize default parameters first
        self._initialize_default_parameters()
        
        if config_file is not None:
            # If a config file is provided, read it and override defaults
            try:
                self.tbparas = read_parameters(config_file)
                self._initialize_parameters_from_file()
                self._validate_kpath_dimensions()
            except FileNotFoundError:
                print(f"Warning: Configuration file '{config_file}' not found. Using default parameters.")
            except Exception as e:
                print(f"Error reading configuration file '{config_file}': {e}. Using default parameters.")
        else:
            # If no config file, ensure k-path validation runs on defaults
            self._validate_kpath_dimensions()

    def _initialize_default_parameters(self):
        """Initialize parameters with default values."""
        self.a0 = 1.0
        self.t0 = 1.0
        self.t0_distance = 2.0
        self.sigma_z = np.array([[1, 0], [0, -1]])
        self.min_distance = 0.1 # Used for distance-based hopping
        self.max_distance = 2.6 # Used for distance-based hopping
        self.onsite_energy = [0.0] # Default to a single value if not specified per atom
        self.dimk = 2
        self.dimr = 3
        self.nspin = 2
        self.hopping_decay = 1.0 # Used for distance-based hopping
        self.same_atom_negative_coupling = False # Used for distance-based hopping
        self.magnetic_moment = 0.0
        self.magnetic_order = "" # Empty means no magnetism applied this way
        self.use_elements = [] # Default to using all elements from POSCAR
        self.savedir = "."
        self.poscar = "POSCAR"
        self.output_filename = "model"
        self.output_format = "png"
        self.kpath_filename = None
        self.kpath = [[0, 0], [0.5, 0], [0.5, 0.5], [0.0, 0.5], [0.0, 0.0], [0.5, 0.5]] # Default 2D path
        self.klabel = ["G", "X", "M", "Y", "G", "M"]
        self.num_k_points = 100
        self.max_R_range = 1 # Search range for neighbors in distance-based and SK
        self.is_print_tb_model_hop = True
        self.is_check_flat_bands = True
        self.is_print_tb_model = True
        self.is_black_degenerate_bands = True
        self.ylim = [-1, 1]
        self.energy_threshold = 1e-5
        self.is_report_kpath = False

        # Slater-Koster specific parameters
        self.use_slater_koster = False # Switch between distance-based and SK
        # Example: {"Fe": [[0, 1, 2, 3], [-8.0, 2.0, 2.0, 2.0]], "O": [[0], [-15.0]]}
        # Orbitals: 0=s, 1=px, 2=py, 3=pz, 4=dxy, 5=dyz, 6=dzx, 7=dx2y2, 8=d3z2r2
        self.orbital_definitions = {}
        # Example: {"Fe-O": {"sps": 1.5, ...}, "Fe-Fe": {...}}
        self.slater_koster_params = {}
        # Example: {"Fe": 0.05, "O": 0.01}
        self.soc_params = {}
        self.apply_soc_onsite_p = True # Whether to apply p-orbital SOC
        self.apply_soc_onsite_d = True # Whether to apply d-orbital SOC

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

    def _initialize_parameters_from_file(self):
        """Initialize all parameters from the configuration file, overriding defaults."""
        # Update only the parameters present in the loaded tbparas dictionary
        
        # Lattice and distance parameters
        self.poscar = self.tbparas.get("poscar_filename", self.poscar)
        self.a0 = self.tbparas.get("lattice_constant", self.a0)
        self.t0 = self.tbparas.get("t0", self.t0)
        self.t0_distance = self.tbparas.get("t0_distance", self.t0_distance)
        
        # Physical parameters
        # self.sigma_z remains default np.array([[1, 0], [0, -1]])
        self.min_distance = self.tbparas.get("min_distance", self.min_distance)
        self.max_distance = self.tbparas.get("max_distance", self.max_distance)
        self.onsite_energy = self.tbparas.get("onsite_energy", self.onsite_energy)
        
        # Model dimensions - ensure these are integers
        self.dimk = int(self.tbparas.get("dimk", self.dimk))
        self.dimr = int(self.tbparas.get("dimr", self.dimr))
        self.nspin = int(self.tbparas.get("nspin", self.nspin))
        
        # Hopping parameters
        self.hopping_decay = self.tbparas.get("hopping_decay", self.hopping_decay)
        self.same_atom_negative_coupling = self.tbparas.get("same_atom_negative_coupling", self.same_atom_negative_coupling)
        
        # Magnetic parameters
        self.magnetic_moment = self.tbparas.get("magnetic_moment", self.magnetic_moment)
        self.magnetic_order = self.tbparas.get("magnetic_order", self.magnetic_order)
        
        # Element selection
        self.use_elements = self.tbparas.get("use_elements", self.use_elements)
        
        # Output parameters
        self.savedir = self.tbparas.get("savedir", self.savedir)
        self.output_filename = self.tbparas.get("output_filename", self.output_filename)
        self.output_format = self.tbparas.get("output_format", self.output_format)
        
        # k-path parameters
        kpath_filename_from_file = self.tbparas.get("kpath_filename")
        if kpath_filename_from_file is not None:
            self.kpath, self.klabel = read_kpath(kpath_filename_from_file)
            self.kpath_filename = kpath_filename_from_file
        else:
            # Only override default kpath/klabel if kpath_filename is not specified
            self.kpath = self.tbparas.get("kpath", self.kpath)
            self.klabel = self.tbparas.get("klabel", self.klabel)
            
        self.is_report_kpath = self.tbparas.get("is_report_kpath", self.is_report_kpath)
        self.num_k_points = int(self.tbparas.get("nkpt", self.num_k_points))
        
        # Plot parameters
        self.ylim = self.tbparas.get("ylim", self.ylim)
        
        # Neighbor parameters
        self.max_R_range = int(self.tbparas.get("max_R_range", self.max_R_range))

        # Other parameters
        self.is_print_tb_model_hop = self.tbparas.get("is_print_tb_model_hop", self.is_print_tb_model_hop)
        self.is_check_flat_bands = self.tbparas.get("is_check_flat_bands", self.is_check_flat_bands)
        self.is_print_tb_model = self.tbparas.get("is_print_tb_model", self.is_print_tb_model)
        self.is_black_degenerate_bands = self.tbparas.get("is_black_degenerate_bands", self.is_black_degenerate_bands)
        self.energy_threshold = self.tbparas.get("energy_threshold", self.energy_threshold)

        # Slater-Koster parameters
        self.use_slater_koster = self.tbparas.get("use_slater_koster", self.use_slater_koster)
        self.orbital_definitions = self.tbparas.get("orbital_definitions", self.orbital_definitions)
        self.slater_koster_params = self.tbparas.get("slater_koster_params", self.slater_koster_params)
        self.soc_params = self.tbparas.get("soc_params", self.soc_params)
        self.apply_soc_onsite_p = self.tbparas.get("apply_soc_onsite_p", self.apply_soc_onsite_p)
        self.apply_soc_onsite_d = self.tbparas.get("apply_soc_onsite_d", self.apply_soc_onsite_d)

    def get_maglist(self, num_atoms_used: Optional[int] = None) -> List[float]:
        """
        Convert magnetic order string to list of magnetic moments.
        Requires the number of atoms to ensure correct length.
        
        Args:
            num_atoms_used (int, optional): The actual number of atoms being used in the model.
                                             If None, will try to infer, but might be inaccurate.

        Returns:
            List[float]: List of magnetic moments matching the number of atoms.
        """
        num_atoms = num_atoms_used

        if num_atoms is None:
            # Attempt to infer if not provided (less reliable)
            if self.use_slater_koster and self.orbital_definitions:
                # This inference is generally incorrect as orbital_definitions is per element type
                warnings.warn("Inferring atom count from orbital_definitions for magnetism is unreliable. Provide num_atoms_used to get_maglist.")
                # Trying to guess based on keys might be slightly better, but still bad
                num_atoms = len(self.orbital_definitions.keys()) # Still likely wrong
            elif not self.use_slater_koster:
                # For distance-based, infer from onsite_energy length ONLY IF it was likely broadcast
                # This check assumes read_parameters correctly broadcasted a single value or validated the length
                num_atoms = len(self.onsite_energy)
                warnings.warn("Inferring atom count from onsite_energy length for magnetism. Provide num_atoms_used to get_maglist for accuracy.")
            else:
                 warnings.warn("Cannot determine atom count for magnetism. Returning empty list.")
                 return []

        # If magnetic_order is provided, use it directly, otherwise generate zeros
        if self.magnetic_order and len(self.magnetic_order) > 0:
            if len(self.magnetic_order) != num_atoms:
                warnings.warn(f"Length of magnetic_order ('{self.magnetic_order}', {len(self.magnetic_order)}) does not match number of atoms ({num_atoms}). Magnetism list might be truncated or padded.")
                # Truncate or pad with zeros to match num_atoms
                mag_list = [self.magnetic_moment if c == '+' else -self.magnetic_moment if c == '-' else 0 
                            for c in self.magnetic_order]
                if len(mag_list) > num_atoms:
                    return mag_list[:num_atoms]
                else:
                    return mag_list + [0.0] * (num_atoms - len(mag_list))
            else:
                # Length matches
                return [self.magnetic_moment if c == '+' else -self.magnetic_moment if c == '-' else 0 
                        for c in self.magnetic_order]
        elif num_atoms > 0:
            # Return zeros if no magnetic order string is given
            return [0.0] * num_atoms
        else:
            # Return empty list if atom count is zero or couldn't be determined
            return []

# Create a global instance using the default constructor (which now handles defaults correctly)
# params = Parameters() 