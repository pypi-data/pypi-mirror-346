#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of CLICopti.
#
# Authors: Kyrre Sjobak, Daniel Schulte, Alexej Grudiev, Andrea Latina, Jim Ögren
#
# We have invested a lot of time and effort in creating the CLICopti library,
# please cite it when using it; see the CITATION file for more information.
#
# CLICopti is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CLICopti is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with CLICopti.  If not, see <https://www.gnu.org/licenses/>.

import CLICopti.RFStructure
import numpy as np
import math
import os

import CLICopti

#For numbers set as floating points, calculated from numbers set by floating point,
# or calculated using operations returning floating point (e.g. Python3 standard division operator)
# do not check for equality of result vs expected result but check that the absolute difference 
# is less than a tolerance value. For reference, float64 has a precission of ca 10^-12.
def compareFloat(a : float, b :float) -> bool:
    if not np.allclose(a,b):
        print ("compareFloat:", a, b)
        return False
    else:
        return True

def compareCells_asserter(cell1 : CLICopti.CellParams, cell2 : CLICopti.CellParams):
    assert compareFloat(cell1.h    - cell2.h, 0.0)
    assert compareFloat(cell1.a    - cell2.a, 0.0)
    assert compareFloat(cell1.d_n  - cell2.d_n, 0.0)
    assert compareFloat(cell1.a_n  - cell2.a_n, 0.0)
    assert compareFloat(cell1.f0   - cell2.f0, 0.0)
    assert compareFloat(cell1.psi  - cell2.psi, 0.0)
    assert compareFloat(cell1.Q    - cell2.Q, 0.0)
    assert compareFloat(cell1.vg   - cell2.vg, 0.0)
    assert compareFloat(cell1.rQ   - cell2.rQ, 0.0)
    assert compareFloat(cell1.Es   - cell2.Es, 0.0)
    assert compareFloat(cell1.Hs   - cell2.Hs, 0.0)
    assert math.isnan(cell1.Sc)
    assert math.isnan(cell2.Sc)
    assert compareFloat(cell1.f1mn - cell2.f1mn, 0.0)
    assert compareFloat(cell1.Q1mn - cell2.Q1mn, 0.0)
    assert compareFloat(cell1.A1mn - cell2.A1mn, 0.0)

def printCell_detailed(cell: CLICopti.CellParams):
    print(cell.h)
    print(cell.a)
    print(cell.d_n)
    print(cell.a_n)
    print(cell.f0)
    print(cell.psi)
    print(cell.Q)
    print(cell.vg)
    print(cell.rQ)
    print(cell.Es)
    print(cell.Hs)
    print(cell.Sc)
    print(cell.f1mn)
    print(cell.Q1mn)
    print(cell.A1mn)

def printPeakfields_detailed(pf: CLICopti.RFStructure.return_AccelStructure_getMaxFields, nom:str = "pf"):
    print(f"assert compareFloat({nom}.maxEs, {pf.maxEs}) #[MV/m]") 
    print(f"assert {nom}.maxEs_idx == {pf.maxEs_idx}")
    print(f"assert compareFloat({nom}.maxHs, {pf.maxHs}) #[kA/m]")
    print(f"assert {nom}.maxHs_idx == {pf.maxHs_idx}")
    print(f"assert compareFloat({nom}.maxSc, {pf.maxSc}) #[W/um^2]")
    print(f"assert {nom}.maxSc_idx == {pf.maxSc_idx}")
    print(f"assert compareFloat({nom}.maxPC, {pf.maxPC}) #[MW/mm]")
    print(f"assert {nom}.maxPC_idx == {pf.maxPC_idx}")

def printMaxAllowableBeamTime_detailed(pf: CLICopti.RFStructure.return_AccelStructure_getMaxAllowableBeamTime_detailed, nom:str = "pf"):
    print(f"assert compareFloat({nom}.power, {pf.power}) #[W]") 
    print(f"assert compareFloat({nom}.beamCurrent_pulseShape, {pf.beamCurrent_pulseShape}) #[A]")
    print(f"assert compareFloat({nom}.beamCurrent_loading,    {pf.beamCurrent_loading})    #[A]")
    print(f"assert compareFloat({nom}.powerFraction, {pf.powerFraction})")

    print(f"assert compareFloat({nom}.wastedTime, {pf.wastedTime}) #[s]") 
    print(f"assert compareFloat({nom}.time_E, {pf.time_E}) #[s]") 
    print(f"assert compareFloat({nom}.time_Sc, {pf.time_Sc}) #[s]") 
    print(f"assert compareFloat({nom}.time_dT, {pf.time_dT}) #[s]") 
    print(f"assert compareFloat({nom}.time_PC, {pf.time_PC}) #[s]") 

    print(f"assert compareFloat({nom}.time, {pf.time}) #[s]") 
    print(f"assert {nom}.which == '{pf.which}'") 

    printPeakfields_detailed(pf.maxFields,nom +".maxFields")
    
    print()

def compareFiles(f1 : str, f2 : str) -> bool:
    "Compare a cell list file, line by line. Return True if equal within fTol"
    equal = True

    f1_ = open(f1,'r')
    f2_ = open(f2,'r')

    n = 0
    while True:
        n += 1
        
        l1 = f1_.readline()
        l2 = f2_.readline()

        if l1 == '' and l2 == '':
            #EOF
            break
        if (l1 == '' and l2 != '') or (l2 == '' and l1 != ''):
            print(f'Different on line #{n}: One line was blank')
            print('l1=', l1,)
            print('l2=', l2,)
            print()
            equal = False
            continue

        if l1 == l2:
            #Quick check / headers
            continue
        
        #Check every number
        l1_ = l1.split()
        l2_ = l2.split()
        badline = False
        if len(l1_) != len(l2_):
            print(f'Difference on line #{n}: Unequal token number')
            print('l1=', l1,)
            print('l2=', l2,)
            print()
            badline = True

        for i in range(len(l1_)):
            if badline:
                break

            try:
                d1 = float(l1_[i])
                d2 = float(l2_[i])
            except ValueError:
                print(f'Could not convert token #{i} on one of the lines:')
                print(f'Tokens are "{l1_[i]}" and "{l2_[i]}"')
                print('l1=', l1,)
                print('l2=', l2,)
                print()
                if l1_[i] == l2_[i]:
                    print("ASCII matched, passed")
                else:
                    badline = True
                continue

            if math.isnan(d1) and math.isnan(d2):
                continue

            deq = compareFloat(d1,d2)
            if deq == False:
                badline = True
                break

        if badline:
            equal = False
            print(f'Difference on line #{n}:')
            print('l1=', l1,)
            print('l2=', l2,)
            print()

    return equal

def getAndMakeTestOutputFolderPath(testname : str):
    fDir = os.path.join('Python','tests','data',testname)
    if not os.path.isdir(fDir):
        os.makedirs(fDir)
    
    return fDir
