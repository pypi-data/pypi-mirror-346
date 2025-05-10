"""
Author: Anoop Ajaya Kumar Nair
Date: 2023-10-24
Description: Code calculates:
    - Dipole Quadrupole polarizability tensor
    - Quadrupole Quadrupole polarizability tensor

Contact Details:
- Email: mailanoopanair@gmail.com
- Company: University of Iceland
- Job Title: Doctoral researcher
"""

from pyscf import qmmm, scf
from qdist import Vi, Vij
from ase.units import Bohr, Ha
import numpy as np
from momtensor import Quadrupole



def calc_Pertb_DP(mol_system, 
                  mol_COM, 
                  mol_xc_func, 
                  box_dim, 
                  field_component, 
                  field_strength):

    charge_postions, charge_mag = Vij(mol_COM,
                                      box_dim, 
                                      field_strength,
                                      field_component)
    
    mf = qmmm.mm_charge(scf.RKS(mol_system), 
                        charge_postions, 
                        charge_mag,
                        unit='AU')
    mf.xc = mol_xc_func
    mf.kernel()
    dp_mom = mf.dip_moment()
    return dp_mom


def calc_Pertb_QP(mol_system, 
                  mol_COM, 
                  mol_xc_func, 
                  box_dim, 
                  field_component, 
                  field_strength):

    charge_postions, charge_mag =Vi(mol_COM,
                                    box_dim, 
                                    field_strength,
                                    field_component)
    
    mf = qmmm.mm_charge(scf.RKS(mol_system), 
                        charge_postions, 
                        charge_mag,
                        unit='AU')
    mf.xc = mol_xc_func
    mf.kernel()
    qp_mom = Quadrupole(mol_system,mf)
    return qp_mom





def calc_FFPertb_Qpole(mol_system, 
                       mol_COM, 
                       mol_xc_func, 
                       box_dim, 
                       field_component, 
                       field_strength):
    charge_postions, charge_mag = Vij(mol_COM,
                                        box_dim, 
                                        field_strength,
                                        field_component)
    mf = qmmm.mm_charge(scf.RKS(mol_system), 
                        charge_postions, 
                        charge_mag,
                        unit='AU')
    mf.xc = mol_xc_func
    mf.kernel()
    qp_mom = Quadrupole(mol_system,mf)
    return qp_mom






class Pols:

    def __init__(   self,
                    mol_struct,
                    mol_system, 
                    mol_xc_func = "pbe",
                    box_dim = 14,
                    field_strength_F = 0.486/Ha*Bohr,
                    field_strength_FF = 0.0486/Ha*Bohr*Bohr,
                    irrep=False):

        self.mol_struct          =  mol_struct
        self.mol_system          = mol_system
        self.box_dim             = box_dim
        self.mol_COM             = self.mol_struct.get_center_of_mass()
        self.field_strength_FF   = field_strength_FF
        self.mol_xc_func         = mol_xc_func
        self.CONST_DPtoAU        = 0.393456/(self.field_strength_FF)
        self.field_strength_F    = field_strength_F
        self.field_strength_ref  = 0.0
        self.field_x             = 'x'
        self.field_y             = 'y'
        self.field_z             = 'z'
        self.field_xx            = "xx"
        self.field_xy            = "xy"
        self.field_xz            = "xz"
        self.field_yy            = 'yy'
        self.field_yz            = 'yz'
        self.field_zz            = 'zz'
        self.irrep               = irrep


    def calcAijk(self):
        print("calc AIJK")
        # Ai,xx 
        self.DP_XX  = calc_Pertb_DP(self.mol_system, 
                                self.mol_COM, 
                                self.mol_xc_func, 
                                self.box_dim, 
                                self.field_xx, 
                                self.field_strength_FF)

        # Ai,yy
        self.DP_YY = calc_Pertb_DP(self.mol_system, 
                                self.mol_COM, 
                                self.mol_xc_func, 
                                self.box_dim, 
                                self.field_yy, 
                                self.field_strength_FF)

        # Ai,zz
        self.DP_ZZ = calc_Pertb_DP(self.mol_system, 
                                self.mol_COM, 
                                self.mol_xc_func, 
                                self.box_dim, 
                                self.field_zz, 
                                self.field_strength_FF)

        # Q0
        self.QP_REF = calc_Pertb_QP(self.mol_system, 
                            self.mol_COM, 
                            self.mol_xc_func, 
                            self.box_dim, 
                            self.field_x, 
                            self.field_strength_ref)


        # Aij,x
        self.QP_X = calc_Pertb_QP(self.mol_system, 
                            self.mol_COM, 
                            self.mol_xc_func, 
                            self.box_dim, 
                            self.field_x, 
                            self.field_strength_F)
        

        # Aij,y
        self.QP_Y = calc_Pertb_QP(self.mol_system, 
                            self.mol_COM, 
                            self.mol_xc_func, 
                            self.box_dim, 
                            self.field_y, 
                            self.field_strength_F)

        # Aij,z
        self.QP_Z = calc_Pertb_QP(self.mol_system, 
                            self.mol_COM, 
                            self.mol_xc_func, 
                            self.box_dim, 
                            self.field_z, 
                            self.field_strength_F)

        AiXX = (self.DP_XX-self.DP_YY)*self.CONST_DPtoAU
        AiYY = (self.DP_YY-self.DP_ZZ)*self.CONST_DPtoAU
        AiZZ = (self.DP_ZZ-self.DP_XX)*self.CONST_DPtoAU
        AijX = (self.QP_X-self.QP_REF)/(self.field_strength_F)
        AijY = (self.QP_Y-self.QP_REF)/(self.field_strength_F)
        AijZ = (self.QP_Z-self.QP_REF)/(self.field_strength_F)


        # Irreducible representation


        self.DQ_IJK_IRREP = np.zeros((18))
        self.DQ_IJK_IRREP[[0,6,12]]     = AiXX
        self.DQ_IJK_IRREP[[3,9,15]]     = AiYY
        self.DQ_IJK_IRREP[[5,11,17]]    = AiZZ
        self.DQ_IJK_IRREP[[1,2,4]] = AijX[[0,0,1],[1,2,2]]
        self.DQ_IJK_IRREP[[7,8,10]] = AijY[[0,0,1],[1,2,2]]
        self.DQ_IJK_IRREP[[13,14,16]] = AijZ[[0,0,1],[1,2,2]]



        # Full matrix representation
        self.DQ_IJK = np.zeros((3,3,3))
        self.DQ_IJK[:,0,0] = AiXX
        self.DQ_IJK[:,1,1] = AiYY
        self.DQ_IJK[:,2,2] = AiZZ
        self.DQ_IJK[0,[0,0,1],[1,2,2]] = AijX[[0,0,1],[1,2,2]]
        self.DQ_IJK[1,[0,0,1],[1,2,2]] = AijY[[0,0,1],[1,2,2]]
        self.DQ_IJK[2,[0,0,1],[1,2,2]] = AijZ[[0,0,1],[1,2,2]]
        self.DQ_IJK[0,[1,2,2],[0,0,1]] = AijX[[0,0,1],[1,2,2]]
        self.DQ_IJK[1,[1,2,2],[0,0,1]] = AijY[[0,0,1],[1,2,2]]
        self.DQ_IJK[2,[1,2,2],[0,0,1]] = AijZ[[0,0,1],[1,2,2]]

        if self.irrep == True:
            np.save("H2O_mono_AIJK_Trrep.npy",np.round(-self.DQ_IJK_IRREP,4))
            return np.round(self.DQ_IJK_IRREP,4)
        else:
            np.save("H2O_mono_AIJK.npy",np.round(-self.DQ_IJK,4))
            return np.round(self.DQ_IJK,4)





    def calcCijkl(self):

        self.QQ_IJKL = np.zeros((3,3,3,3))

        # QP_REF
        self.QP_REF = calc_FFPertb_Qpole(self.mol_system, 
                                         self.mol_COM, 
                                         self.mol_xc_func, 
                                         self.box_dim, 
                                         self.field_xx, 
                                         self.field_strength_ref)

        # Cij,xx
        self.QP_XX = calc_FFPertb_Qpole(self.mol_system, 
                                 self.mol_COM, 
                                 self.mol_xc_func, 
                                 self.box_dim, 
                                 self.field_xx, 
                                 self.field_strength_FF)

        # Cij,yy
        self.QP_YY = calc_FFPertb_Qpole(self.mol_system, 
                                 self.mol_COM, 
                                 self.mol_xc_func, 
                                 self.box_dim, 
                                 self.field_yy, 
                                 self.field_strength_FF)

        # Cij,zz
        self.QP_ZZ = calc_FFPertb_Qpole(self.mol_system, 
                                 self.mol_COM, 
                                 self.mol_xc_func, 
                                 self.box_dim, 
                                 self.field_zz, 
                                 self.field_strength_FF)

        # Cij,xy
        self.QP_XY = calc_FFPertb_Qpole(self.mol_system, 
                                 self.mol_COM, 
                                 self.mol_xc_func, 
                                 self.box_dim, 
                                 self.field_xy, 
                                 self.field_strength_FF)

        # Cij,xz
        self.QP_XZ = calc_FFPertb_Qpole(self.mol_system, 
                                 self.mol_COM, 
                                 self.mol_xc_func, 
                                 self.box_dim, 
                                 self.field_xz, 
                                 self.field_strength_FF)

        # Cij,yz
        self.QP_YZ = calc_FFPertb_Qpole(self.mol_system, 
                                 self.mol_COM, 
                                 self.mol_xc_func, 
                                 self.box_dim, 
                                 self.field_yz, 
                                 self.field_strength_FF)

        Cijxx = (self.QP_XX - self.QP_YY)/(3*self.field_strength_FF)
        Cijyy = (self.QP_YY - self.QP_ZZ)/(3*self.field_strength_FF)
        Cijzz = (self.QP_ZZ - self.QP_XX)/(3*self.field_strength_FF)
        Cijxy = (self.QP_XY - self.QP_REF)/self.field_strength_FF
        Cijyz = (self.QP_YZ - self.QP_REF)/self.field_strength_FF
        Cijxz = (self.QP_XZ - self.QP_REF)/self.field_strength_FF
        Cxyxy = Cijxy[0,1]/2.0
        Cxyyz = Cijyz[0,1]
        Cxzyz = Cijyz[0,2]
        Cyzyz = Cijyz[1,2]/2.0
        Cxyxz = Cijxz[0,1]
        Cxzxz = Cijxz[0,2]/2.0
        Cijxx   = (self.QP_XX-self.QP_REF)/self.field_strength_FF
        Cijyy   = (self.QP_YY-self.QP_REF)/self.field_strength_FF
        Cijxxyy = (self.QP_XX-self.QP_YY)/self.field_strength_FF
        Cxxxx =  -Cijxxyy[0,0]/3.0
        Cxxyy =  -Cijxxyy[1,1]/3.0
        Cxxzz =  -Cijxxyy[2,2]/3.0
        Cyyyy =  +Cxxyy - Cijyy[1,1]
        Cyyzz =  +Cxxzz - Cijyy[2,2]
        Czzzz =  +Cxxzz + Cijxx[2,2]

        # Irreducible representation
        self.QQ_IJKL_IRREP = np.zeros(21)
        self.QQ_IJKL_IRREP[0]   = round(float(Cxxxx),5)
        self.QQ_IJKL_IRREP[1]   = round(float(Cijxx[0,1]),5)
        self.QQ_IJKL_IRREP[2]   = round(float(Cijxx[0,2]),5)
        self.QQ_IJKL_IRREP[3]   = round(float(Cxxyy),5)
        self.QQ_IJKL_IRREP[4]   = round(float(Cijxx[1,2]),5)
        self.QQ_IJKL_IRREP[5]   = round(float(Cxxzz),5)
        self.QQ_IJKL_IRREP[6]   = round(float(Cxyxy),5)
        self.QQ_IJKL_IRREP[7]   = round(float(Cxyxz),5)
        self.QQ_IJKL_IRREP[8]   = round(float(Cijyy[0,1]),5)
        self.QQ_IJKL_IRREP[9]   = round(float(Cxyyz),5)
        self.QQ_IJKL_IRREP[10]  = round(float(Cijzz[0,1]),5)
        self.QQ_IJKL_IRREP[11]  = round(float(Cxzxz),5)
        self.QQ_IJKL_IRREP[12]  = round(float(Cijyy[0,2]),5)
        self.QQ_IJKL_IRREP[13]  = round(float(Cxzyz),5)
        self.QQ_IJKL_IRREP[14]  = round(float(Cijzz[0,2]),5)
        self.QQ_IJKL_IRREP[15]  = round(float(Cyyyy),5)
        self.QQ_IJKL_IRREP[16]  = round(float(Cijyy[1,2]),5)
        self.QQ_IJKL_IRREP[17]  = round(float(Cyyzz),5)
        self.QQ_IJKL_IRREP[18]  = round(float(Cyzyz),5)
        self.QQ_IJKL_IRREP[19]  = round(float(Cijzz[1,2]),5)
        self.QQ_IJKL_IRREP[20]  = round(float(Czzzz),5)

 
        self.QQ_IJKL[0,0,0,0] = self.QQ_IJKL_IRREP[0]
        self.QQ_IJKL[[0,1,0,0],
                     [1,0,0,0],
                     [0,0,0,1],
                     [0,0,1,0]] = self.QQ_IJKL_IRREP[1]
        self.QQ_IJKL[[0,2,0,0],
                     [2,0,0,0],
                     [0,0,0,2],
                     [0,0,2,0]] = self.QQ_IJKL_IRREP[2]
        self.QQ_IJKL[[1,0],
                     [1,0],
                     [0,1],
                     [0,1]] = self.QQ_IJKL_IRREP[3]
        self.QQ_IJKL[[1,2,0,0],
                     [2,1,0,0],
                     [0,0,1,2],
                     [0,0,2,1]] = self.QQ_IJKL_IRREP[4]
        self.QQ_IJKL[[2,0],
                     [2,0],
                     [0,2],
                     [0,2]] = self.QQ_IJKL_IRREP[5]
        self.QQ_IJKL[[0,0,1,1],
                     [1,1,0,0],
                     [0,1,0,1],
                     [1,0,1,0]] = self.QQ_IJKL_IRREP[6]
        self.QQ_IJKL[[0,0,2,2,0,1,0,1],
                     [2,2,0,0,1,0,1,0],
                     [0,1,0,1,0,0,2,2],
                     [1,0,1,0,2,2,0,0]] = self.QQ_IJKL_IRREP[7]
        self.QQ_IJKL[[1,1,0,1],
                     [1,1,1,0],
                     [0,1,1,1],
                     [1,0,1,1]] = self.QQ_IJKL_IRREP[8]
        self.QQ_IJKL[[1,1,2,2,0,1,0,1],
                     [2,2,1,1,1,0,1,0],
                     [0,1,0,1,1,1,2,2],
                     [1,0,1,0,2,2,1,1]] = self.QQ_IJKL_IRREP[9]
        self.QQ_IJKL[[2,2,0,1],
                     [2,2,1,0],
                     [0,1,2,2],
                     [1,0,2,2]] = self.QQ_IJKL_IRREP[10]
        self.QQ_IJKL[[0,0,2,2],
                     [2,2,0,0],
                     [0,2,0,2],
                     [2,0,2,0]] = self.QQ_IJKL_IRREP[11]
        self.QQ_IJKL[[1,1,0,2],
                     [1,1,2,0],
                     [0,2,1,1],
                     [2,0,1,1]] = self.QQ_IJKL_IRREP[12]
        self.QQ_IJKL[[1,1,2,2,0,2,0,2],
                     [2,2,1,1,2,0,2,0],
                     [0,2,0,2,1,1,2,2],
                     [2,0,2,0,2,2,1,1]] = self.QQ_IJKL_IRREP[13]
        self.QQ_IJKL[[2,2,0,2],
                     [2,2,2,0],
                     [0,2,2,2],
                     [2,0,2,2]] = self.QQ_IJKL_IRREP[14]
        self.QQ_IJKL[1,1,1,1] = self.QQ_IJKL_IRREP[15]
        self.QQ_IJKL[[1,2,1,1],
                     [2,1,1,1],
                     [1,1,1,2],
                     [1,1,2,1]] = self.QQ_IJKL_IRREP[16]
        self.QQ_IJKL[[2,1],
                     [2,1],
                     [1,2],
                     [1,2]] = self.QQ_IJKL_IRREP[17]
        self.QQ_IJKL[[1,1,2,2],
                     [2,2,1,1],
                     [1,2,1,2],
                     [2,1,2,1]] = self.QQ_IJKL_IRREP[18]
        self.QQ_IJKL[[2,2,1,2],
                     [2,2,2,1],
                     [1,2,2,2],
                     [2,1,2,2]] = self.QQ_IJKL_IRREP[19]
        self.QQ_IJKL[2,2,2,2] = self.QQ_IJKL_IRREP[20]

        if self.irrep == True:
            np.save("H2O_mono_CIJKL_Trrep.npy",np.round(-self.QQ_IJKL_IRREP,4))
            return np.round(-self.QQ_IJKL_IRREP,4)
        else:
            np.save("H2O_mono_CIJKL.npy",np.round(-self.QQ_IJKL,4))
            return np.round(-self.QQ_IJKL,4)
