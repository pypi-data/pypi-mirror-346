from pyscf import gto
from ase.io import read
from .poltensor import Pols

def create_pyscf_mol(xyz_file, basis="augccpvqz"):
    """Create a PySCF molecule object from an XYZ file.
    
    Args:
        xyz_file (str): Path to the XYZ file
        basis (str): Basis set to use (default: augccpvqz)
        
    Returns:
        tuple: (molecule, mol) where molecule is an ASE Atoms object and mol is a PySCF Mole object
    """
    mol = gto.Mole()
    molecule = read(xyz_file)
    mol.atom = xyz_file
    mol.basis = basis
    mol.build()
    return molecule, mol

def calculate_polarizabilities(molecule, mol, irrep=True):
    """Calculate polarizabilities using PySCF.
    
    Args:
        molecule: ASE Atoms object
        mol: PySCF Mole object
        irrep (bool): Whether to use irreducible representation (default: True)
        
    Returns:
        tuple: (Aijk, Cijkl) polarizability tensors
    """
    pols = Pols(molecule, mol, irrep=irrep)
    Aijk = pols.calcAijk()
    Cijkl = pols.calcCijkl()
    return Aijk, Cijkl