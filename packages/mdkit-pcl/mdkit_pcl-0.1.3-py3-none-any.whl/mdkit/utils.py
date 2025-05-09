# mdkit/utils.py
import os
import periodictable
import math

def calculate_molecular_weight(pdb_file):
    """计算单个分子的质量"""
    total_mass = 0.0
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                element_symbol = line[76:78].strip()
                try:
                    element = getattr(periodictable, element_symbol)
                    total_mass += element.mass
                except AttributeError:
                    print(f"Warning: Unknown element {element_symbol} in PDB file {pdb_file}.")
    return total_mass

def calculate_total_mass(pdb_files, num_molecules):
    """计算体系中所有分子的总质量"""
    total_mass = 0.0
    for pdb_file, num in zip(pdb_files, num_molecules):
        molecular_weight = calculate_molecular_weight(pdb_file)
        total_mass += molecular_weight * num
    return total_mass

def calculate_box_size(pdb_files, num_molecules, target_density):
    """根据目标密度计算盒子尺寸"""
    total_mass = calculate_total_mass(pdb_files, num_molecules)
    total_mass_g = total_mass * 1.66053906660e-24
    volume_cm3 = total_mass_g / target_density
    volume_ang3 = volume_cm3 / 1e-24
    box_length = volume_ang3 ** (1/3)
    box_length = math.ceil(box_length / 10) * 10
    return [box_length, box_length, box_length]