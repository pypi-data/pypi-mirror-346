import unittest
import numpy as np
import os
from pyamtb import tight_binding_model
from pyamtb import read_datas

class TestTightBindingModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_poscar = "test_VTe2/VTe2_Lieb.vasp"
        self.tbparas = read_datas.read_parameters()

    def test_read_poscar(self):
        """Test reading POSCAR file."""
        poscar_data = tight_binding_model.read_poscar(self.test_poscar)
        self.assertIsNotNone(poscar_data)
        self.assertIn('lattice', poscar_data)
        self.assertIn('coords', poscar_data)
        self.assertIn('elements', poscar_data)

    def test_calculate_distance(self):
        """Test distance calculation."""
        poscar_data = tight_binding_model.read_poscar(self.test_poscar)
        coord1 = poscar_data['coords'][0]
        coord2 = poscar_data['coords'][1]
        distance = tight_binding_model.calculate_distance(coord1, coord2, poscar_data['lattice'])
        self.assertIsInstance(distance, float)
        self.assertGreater(distance, 0)

    def test_hopping_strength(self):
        """Test hopping strength calculation."""
        distance = 3.0
        reference_distance = 2.0
        t0 = 1.0
        t = tight_binding_model.hopping_strength(distance, reference_distance, t0)
        self.assertIsInstance(t, float)
        self.assertLess(t, t0)  # Hopping strength should decrease with distance

    def test_create_pythtb_model(self):
        """Test model creation."""
        model = tight_binding_model.create_pythtb_model(
            poscar_filename=self.test_poscar,
            element_to_model=["V", "Te"],
            t0=1.0,
            max_neighbors=1
        )
        self.assertIsNotNone(model)

if __name__ == '__main__':
    unittest.main() 