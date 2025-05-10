from pyscf import gto
from ase.io import read
from poltensor import Pols

mol = gto.Mole()
molecule = read("monomerA.xyz")
mol.atom = "monomerA.xyz" 
mol.basis = "augccpvqz"
mol.build()

pols = Pols(molecule,mol, irrep=True)

# print(pols.calcAijk())
print(pols.calcCijkl())