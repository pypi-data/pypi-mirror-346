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

#This is a port of testCellLibrary.ipynb which is a port of testCellLibrary.cpp,
# to the pyTest automatic testing framework
# It tests both the functionality of CellParams, the scaling routines,
# and the cell databases including interpolation

import numpy as np
import math
import os

import CLICopti

import pytest

import CLICopti.CellParams

from testutils import compareFloat, compareCells_asserter, printCell_detailed, compareFiles

@pytest.mark.cellBase
def test_CellBase_linearInterpolation():
    base = CLICopti.CellBase.CellBase_linearInterpolation(CLICopti.CellBase.celldatabase_TD_30GHz, ("psi", "a_n", "d_n"))
    #base.printGrid()

    #Testing Cell Arithmetic
    c000 = base.getCellGrid([0,0,0])
    #print("c000 :",c000)
    #printCell_detailed(c000)
    assert compareFloat(c000.h,    0.0033326936579400807)
    assert compareFloat(c000.a,    0.000699865668167417)
    assert compareFloat(c000.d_n,  0.1)
    assert compareFloat(c000.a_n,  0.07)
    assert compareFloat(c000.f0,   29.985)
    assert compareFloat(c000.psi,  120)
    assert compareFloat(c000.Q,    4041)
    assert compareFloat(c000.vg,   0.32)
    assert compareFloat(c000.rQ,   50345)
    assert compareFloat(c000.Es,   1.8)
    assert compareFloat(c000.Hs,   3.6)
    assert math.isnan  (c000.Sc)
    assert compareFloat(c000.f1mn, 45.32)
    assert compareFloat(c000.Q1mn, 6.7)
    assert compareFloat(c000.A1mn, 3044.3262828242455)
    
    c001 = base.getCellGrid((0,0,1))
    #print("c001 :",c001)
    #printCell_detailed(c001)
    assert compareFloat(c001.h,    0.0033326936579400807)
    assert compareFloat(c001.a,    0.000699865668167417)
    assert compareFloat(c001.d_n,  0.25)
    assert compareFloat(c001.a_n,  0.07)
    assert compareFloat(c001.f0,   29.985)
    assert compareFloat(c001.psi,  120)
    assert compareFloat(c001.Q,    3718)
    assert compareFloat(c001.vg,   0.12)
    assert compareFloat(c001.rQ,   45470)
    assert compareFloat(c001.Es,   1.7)
    assert compareFloat(c001.Hs,   4.1)
    assert math.isnan  (c001.Sc)
    assert compareFloat(c001.f1mn, 44.77)
    assert compareFloat(c001.Q1mn, 7.8)
    assert compareFloat(c001.A1mn, 3101.5546298958175)

    c001_2 = c001*2
    assert compareFloat(c001_2.h,    2*0.0033326936579400807)
    assert compareFloat(c001_2.a,    2*0.000699865668167417)
    assert compareFloat(c001_2.d_n,  2*0.25)
    assert compareFloat(c001_2.a_n,  2*0.07)
    assert compareFloat(c001_2.f0,   2*29.985)
    assert compareFloat(c001_2.psi,  2*120)
    assert compareFloat(c001_2.Q,    2*3718)
    assert compareFloat(c001_2.vg,   2*0.12)
    assert compareFloat(c001_2.rQ,   2*45470)
    assert compareFloat(c001_2.Es,   2*1.7)
    assert compareFloat(c001_2.Hs,   2*4.1)
    assert math.isnan  (c001_2.Sc)
    assert compareFloat(c001_2.f1mn, 2*44.77)
    assert compareFloat(c001_2.Q1mn, 2*7.8)
    assert compareFloat(c001_2.A1mn, 2*3101.5546298958175)

    c001_2_ = 2*c001
    assert compareFloat(c001_2_.h,    2*0.0033326936579400807)
    assert compareFloat(c001_2_.a,    2*0.000699865668167417)
    assert compareFloat(c001_2_.d_n,  2*0.25)
    assert compareFloat(c001_2_.a_n,  2*0.07)
    assert compareFloat(c001_2_.f0,   2*29.985)
    assert compareFloat(c001_2_.psi,  2*120)
    assert compareFloat(c001_2_.Q,    2*3718)
    assert compareFloat(c001_2_.vg,   2*0.12)
    assert compareFloat(c001_2_.rQ,   2*45470)
    assert compareFloat(c001_2_.Es,   2*1.7)
    assert compareFloat(c001_2_.Hs,   2*4.1)
    assert math.isnan  (c001_2_.Sc)
    assert compareFloat(c001_2_.f1mn, 2*44.77)
    assert compareFloat(c001_2_.Q1mn, 2*7.8)
    assert compareFloat(c001_2_.A1mn, 2*3101.5546298958175)

    c001_2o = c001/2
    assert compareFloat(c001_2o.h,    0.0033326936579400807 / 2)
    assert compareFloat(c001_2o.a,    0.000699865668167417 / 2)
    assert compareFloat(c001_2o.d_n,  0.25 / 2)
    assert compareFloat(c001_2o.a_n,  0.07 / 2)
    assert compareFloat(c001_2o.f0,   29.985 / 2)
    assert compareFloat(c001_2o.psi,  120 / 2)
    assert compareFloat(c001_2o.Q,    3718 / 2)
    assert compareFloat(c001_2o.vg,   0.12 / 2)
    assert compareFloat(c001_2o.rQ,   45470 / 2)
    assert compareFloat(c001_2o.Es,   1.7 / 2)
    assert compareFloat(c001_2o.Hs,   4.1 / 2)
    assert math.isnan  (c001_2o.Sc)
    assert compareFloat(c001_2o.f1mn, 44.77 / 2)
    assert compareFloat(c001_2o.Q1mn, 7.8 / 2)
    assert compareFloat(c001_2o.A1mn, 3101.5546298958175 / 2)


    c000_p_001 = c000 + c001
    assert compareFloat(c000_p_001.h,    0.0033326936579400807 + 0.0033326936579400807)
    assert compareFloat(c000_p_001.a,    0.000699865668167417 + 0.000699865668167417)
    assert compareFloat(c000_p_001.d_n,  0.1 + 0.25)
    assert compareFloat(c000_p_001.a_n,  0.07 + 0.07)
    assert compareFloat(c000_p_001.f0,   29.985 + 29.985)
    assert compareFloat(c000_p_001.psi,  120 + 120)
    assert compareFloat(c000_p_001.Q,    4041 + 3718)
    assert compareFloat(c000_p_001.vg,   0.32 + 0.12)
    assert compareFloat(c000_p_001.rQ,   50345 + 45470)
    assert compareFloat(c000_p_001.Es,   1.8 + 1.7)
    assert compareFloat(c000_p_001.Hs,   3.6 + 4.1)
    assert math.isnan  (c000_p_001.Sc)
    assert compareFloat(c000_p_001.f1mn, 45.32 + 44.77)
    assert compareFloat(c000_p_001.Q1mn, 6.7 + 7.8)
    assert compareFloat(c000_p_001.A1mn, 3044.3262828242455 + 3101.5546298958175)

    c000_m_001 = c000 - c001
    assert compareFloat(c000_m_001.h,    0.0033326936579400807 - 0.0033326936579400807)
    assert compareFloat(c000_m_001.a,    0.000699865668167417 - 0.000699865668167417)
    assert compareFloat(c000_m_001.d_n,  0.1 - 0.25)
    assert compareFloat(c000_m_001.a_n,  0.07 - 0.07)
    assert compareFloat(c000_m_001.f0,   29.985 - 29.985)
    assert compareFloat(c000_m_001.psi,  120 - 120)
    assert compareFloat(c000_m_001.Q,    4041 - 3718)
    assert compareFloat(c000_m_001.vg,   0.32 - 0.12)
    assert compareFloat(c000_m_001.rQ,   50345 - 45470)
    assert compareFloat(c000_m_001.Es,   1.8 - 1.7)
    assert compareFloat(c000_m_001.Hs,   3.6 - 4.1)
    assert math.isnan  (c000_m_001.Sc)
    assert compareFloat(c000_m_001.f1mn, 45.32 - 44.77)
    assert compareFloat(c000_m_001.Q1mn, 6.7 - 7.8)
    assert compareFloat(c000_m_001.A1mn, 3044.3262828242455 - 3101.5546298958175)

    #TODO: Also test (c000+c001)*0.5 and (c000+c001)/2

    #Test that interpolation works as expected
    for Ipsi in range(2):
        for Ian in range(5):
            for Idn in range(3):
                Idex = (Ipsi, Ian, Idn)
                #print("Grid idx =", Idex)

                t = base.getCellGrid(Idex)
                #print("Cell at grid:", t)

                dIdx = [t.psi,t.a_n,t.d_n]
                #print("Coordinates:", dIdx)

                t2 = base.getCellInterpolated(dIdx)
                #print ("Cell at coords:", t2)

                compareCells_asserter(t,t2)
                
                #print()

    #Trigger a failure and a printout
    #assert False

@pytest.mark.cellBase
def test_CellBase_linearInterpolation_freqScaling():
    f0_2 = 11.9942 #[GHz]
    base2 = CLICopti.CellBase.CellBase_linearInterpolation_freqScaling(CLICopti.CellBase.celldatabase_TD_30GHz, ("psi", "a_n", "d_n"), f0_2)

    #Get the grid point directly
    b000 = base2.getCellGrid((0,0,0))
    print("b000 grid         :", b000)

    base2.scaleCell(b000)
    print("scaled explicitly :", b000)

    #Directly call the scaler function
    b000_sf = CLICopti.CellParams.scaleCell(b000,f0_2)
    print("scaled directly   :", b000_sf)

    #Get the 
    dIdex = [b000.psi, b000.a_n, b000.d_n]
    a000 = base2.getCellInterpolated(dIdex)
    print("Interpolated and internally scaled :")
    print("                   ",a000)

    compareCells_asserter(b000,b000_sf)
    compareCells_asserter(b000,a000)

    #Trigger a failure and a printout
    #assert False

@pytest.mark.cellBase
def test_CellBase_copyCell():
    #Explicit copying of the cellParams object
    f0_2 = 11.9942 #[GHz]
    base2 = CLICopti.CellBase.CellBase_linearInterpolation_freqScaling(CLICopti.CellBase.celldatabase_TD_30GHz, ("psi", "a_n", "d_n"), f0_2)

    #Get the grid point directly
    b000 = base2.getCellGrid((0,0,0))
    print("b000 grid         :", b000)
    
    #Other ways of calling getCellGrid:
    b000_1 = base2.getCellGrid([0,0,0])
    compareCells_asserter(b000, b000_1)
    b000_2 = base2.getCellGrid(np.asarray([0,0,0], int))
    compareCells_asserter(b000, b000_2)
    #This should fail
    with pytest.raises(TypeError):
        #Wrong data type on last one
        b000_f1 = base2.getCellGrid([0,0,0.0])
    with pytest.raises(TypeError):
        #Wrong data type of array
        b000_f2 = base2.getCellGrid(np.asarray([0,0,0],float))
    with pytest.raises(TypeError):
        # Wrong number of indices
        b000_f3 = base2.getCellGrid([0,0,0,0])


    base2.scaleCell(b000)
    print("scaled explicitly :", b000)

    print("Original f0 in in orignal object       :", b000.f0)
    b0 = CLICopti.CellParams.CellParams_copy(b000)
    b0.f0 = 0
    print("f0 in copy after zeroing it            :",b0.f0)
    print("f0 in orignal after zeroing f0 in copy :", b000.f0)

    compareFloat(b0.f0,0.0)
    compareFloat(b000.f0, f0_2)

    #Trigger a failure and a printout
    #assert False

@pytest.mark.cellBase
def test_CellBase_linearInterpolation_freqScaling():

    f0_2 = 11.9942 #[GHz]

    base3 = CLICopti.CellBase.CellBase_compat(CLICopti.CellBase.celldatabase_TD_30GHz, f0_2)
    base3.printGrid()

    psi_list=[120,150,130]
    #Testing interpolation
    for psi in psi_list:
        print("Testing at psi =",psi)
        for a_n in np.linspace(0.07,0.23,23-7+1):
            for d_n in np.linspace(0.1,0.4,4-1+1):
                dIdex = (psi,a_n,d_n)
                print(dIdex, '\n\t', base3.getCellInterpolated(dIdex))
        print()
    
    #Make plots
    def _contourPlot(data,title, fname):
        plt.figure()
        plt.contourf(a_n,d_n,rQ,20)
        plt.colorbar()
        plt.title(title)

        mg,_ = base3.getGrid_meshgrid()
        plt.scatter(mg[1],mg[2], marker='*', color='red')
        
        print(f"Writing file '{fname}'")
        plt.savefig(fname)
    
    fDir = os.path.join('Python','tests','data','test_CellBase_linearInterpolation_freqScaling')
    if not os.path.isdir(fDir):
        os.makedirs(fDir)

    doPlot = True
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        with open(os.path.join(fDir,'PLOTS.txt'),'w') as readme:
            readme.write('Could not import matplotlib.pyplot, so no plots. Sorry!\n')
            readme.close()
            #raise #Re-raises error
            doPlot = False

    dbFile = open(os.path.join(fDir,'DB.txt'),'w')

    for psi in psi_list:
        a_n,d_n = np.meshgrid(np.linspace(0.07,0.23,10), np.linspace(0.1,0.4,10))
        rQ = np.zeros_like(a_n)
        Q  = np.zeros_like(a_n)
        vg = np.zeros_like(a_n)

        for a_n_i_, a_n_ in enumerate(a_n[0,:]):
            for d_n_i_, d_n_ in enumerate(d_n[:,0]):
                cell3 = base3.getCellInterpolated([psi,a_n_,d_n_])

                rQ[d_n_i_,a_n_i_] = cell3.rQ
                Q [d_n_i_,a_n_i_] = cell3.Q
                vg[d_n_i_,a_n_i_] = cell3.vg

                dbFile.write(f'{cell3.h} {cell3.a} {cell3.d_n} {cell3.a_n} {cell3.f0} {cell3.psi} ')
                dbFile.write(f'{cell3.Q} {cell3.vg} {cell3.rQ} {cell3.Es} {cell3.Hs} {cell3.Sc} ')
                dbFile.write(f'{cell3.f1mn} {cell3.Q1mn} {cell3.A1mn}\n')

        if doPlot:
            _contourPlot(rQ,f'rQ, psi={psi}',os.path.join(fDir,f'rQ_{psi}.png'))
            _contourPlot( Q, f'Q, psi={psi}',os.path.join(fDir,f'Q_{psi}.png'))
            _contourPlot(vg,f'vg, psi={psi}',os.path.join(fDir,f'vg_{psi}.png'))

    dbFile.close()
    
    assert compareFiles(os.path.join(fDir,'DB.txt'),os.path.join(fDir,'DB_ref.txt')) == True


