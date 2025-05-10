"""
Author: Anoop Ajaya Kumar Nair
Date: 2023-10-24
Description: Code calculates:
    - Eight and Four charge distributions for field gradient generation
    - Two charge distributions for field generation

Contact Details:
- Email: mailanoopanair@gmail.com
- Company: University of Iceland
- Job Title: Doctoral researcher
"""


import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d')

def PosGenDiagFun(posarr,a,q):
    pos = np.array(posarr)
    pos1 = pos[0]
    pos2 = pos[1]
    
    x1 = pos1                        # +2q
    x2 = pos1                        #  -q
    x3 = pos1                        #  -q
    x4 = pos1                        # +2q

    x5 = pos1 -  (2.0**(1.0/3.0))*a  # +q
    x6 = pos1 -  a                   # -q
    x7 = pos1 +  a                   # -q
    x8 = pos1 +  (2.0**(1.0/3.0))*a  # +q


    y1 = pos2 +   2*a                # +2q
    y2 = pos2 +  (2.0**(1.0/3.0))*a  #  -q
    y3 = pos2 -  (2.0**(1.0/3.0))*a  #  -q
    y4 = pos2 -   2*a                # +2q

    y5 = pos2                        # +q
    y6 = pos2                        # -q
    y7 = pos2                        # -q
    y8 = pos2                        # +q

    chargepostions = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5],[x6,y6],[x7,y7],[x8,y8]])
    charges = np.array([+2*q,-q,-q,+2*q,+q,-q,-q,+q])

    return chargepostions, charges


def PosGenNonDiagFun(posarr,a,q):

    pos = np.array(posarr)
    pos1 = pos[0]
    pos2 = pos[1]

    x1 = pos1 - a                       #  -q
    x2 = pos1 + a                       #  +q
    x3 = pos1 - a                       #  +q
    x4 = pos1 + a                       #  -q


    y1 = pos2 +  (2.0**(1.0/2.0))*a     #  -q   
    y2 = pos2 +  (2.0**(1.0/2.0))*a     #  +q 
    y3 = pos2 -  (2.0**(1.0/2.0))*a     #  +q 
    y4 = pos2 -  (2.0**(1.0/2.0))*a     #  -q   

    chargepostions = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
    charges = np.array([-q,+q,+q,-q])

    return chargepostions, charges

def PosGenDpole(posarr,a,q):

    pass
    pos = np.array(posarr)
    pos1 = pos[0]

    x1 = pos1 + a  #  -q
    x2 = pos1 - a  #  +q

    chargepostions = np.array([[x1],[x2]])
    charges = np.array([-q,+q])

    return chargepostions, charges



def Vxx(posarr,a,q):

    pos = np.array(posarr)
    # print(pos)
    PosVal = np.array([pos[0],pos[1]])
    # print(PosVal)
    chargepostions, charges = PosGenDiagFun(PosVal,a,q)
    chargepostions = np.hstack((chargepostions,np.ones((8,1))*pos[2]))
    return chargepostions, charges

def Vyy(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[1],pos[2]])
    chargepostions, charges = PosGenDiagFun(PosVal,a,q)
    chargepostions = np.hstack((np.ones((8,1))*pos[0],chargepostions))
    return chargepostions, charges

def Vzz(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[2],pos[0]])
    chargepostions, charges = PosGenDiagFun(PosVal,a,q)
    chargepostions = np.hstack((chargepostions[:,1].reshape(8,1),np.ones((8,1))*pos[1],chargepostions[:,0].reshape(8,1)))
    return chargepostions, charges

def Vxy(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[0],pos[1]])
    chargepostions, charges = PosGenNonDiagFun(PosVal,a,q)
    chargepostions = np.hstack((chargepostions,np.ones((4,1))*pos[2]))
    return chargepostions, charges


def Vyz(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[1],pos[2]])
    chargepostions, charges = PosGenNonDiagFun(PosVal,a,q)
    chargepostions = np.hstack((np.ones((4,1))*pos[0],chargepostions))
    return chargepostions, charges


def Vzx(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[0],pos[2]])
    chargepostions, charges = PosGenNonDiagFun(PosVal,a,q)
    chargepostions = np.hstack((chargepostions[:,0].reshape(4,1),np.ones((4,1))*pos[1],chargepostions[:,1].reshape(4,1)))
    return chargepostions, charges


def Vx(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[0]])
    chargepostions, charges = PosGenDpole(PosVal,a,q)
    chargepostions = np.hstack((chargepostions[:,0].reshape(2,1),np.ones((2,1))*pos[1],np.ones((2,1))*pos[2]))
    return chargepostions, charges


def Vy(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[1]])
    chargepostions, charges = PosGenDpole(PosVal,a,q)
    chargepostions = np.hstack((np.ones((2,1))*pos[0],chargepostions[:,0].reshape(2,1),np.ones((2,1))*pos[2]))
    return chargepostions, charges


def Vz(posarr,a,q):

    pos = np.array(posarr)
    PosVal = np.array([pos[2]])
    chargepostions, charges = PosGenDpole(PosVal,a,q)
    chargepostions = np.hstack((np.ones((2,1))*pos[0],np.ones((2,1))*pos[1],chargepostions[:,0].reshape(2,1)))
    return chargepostions, charges



def Vij(posarr,a, Fstrength,component):



    if component == 'xx':
        q = 2.0*(a**3)*Fstrength/3.0
        chargepostions, charges = Vxx(posarr,a,q)


    if component == 'yy':
        q = 2.0*(a**3)*Fstrength/3.0
        chargepostions, charges = Vyy(posarr,a,q)


    if component == 'zz':
        q = 2.0*(a**3)*Fstrength/3.0
        chargepostions, charges = Vzz(posarr,a,q)


    if component == 'xy':
        q = (((3**0.5)*a)**3)*Fstrength/(4.0*(2**0.5))
        chargepostions, charges = Vxy(posarr,a,q)


    if component == 'xz':
        q = (((3**0.5)*a)**3)*Fstrength/(4.0*(2**0.5))
        chargepostions, charges = Vzx(posarr,a,q)


    if component == 'yz':
        q = (((3**0.5)*a)**3)*Fstrength/(4.0*(2**0.5))
        chargepostions, charges = Vyz(posarr,a,q)


    return chargepostions, charges


def Vi(posarr,a, Fstrength,component):


    if component == 'x':
        q = (a**2)*Fstrength/2.0
        chargepostions, charges = Vx(posarr,a,q)

    if component == 'y':
        q = (a**2)*Fstrength/2.0
        chargepostions, charges = Vy(posarr,a,q)

    if component == 'z':
        q = (a**2)*Fstrength/2.0
        chargepostions, charges = Vz(posarr,a,q)

    return chargepostions, charges


