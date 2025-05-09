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

#This is a port of testStructureLibrary.ipynb which is a port of testStructureLibrary.cpp,
# to the pyTest automatic testing framework
# It tests both the cell databases including interpolation,
# and the various calculation of the RFstructure class

import numpy as np
import math
import os

import CLICopti

import pytest

import CLICopti.RFStructure

from testutils import compareFloat, compareFiles,\
      printCell_detailed, printPeakfields_detailed, printMaxAllowableBeamTime_detailed, \
      getAndMakeTestOutputFolderPath

@pytest.mark.structureLibrary
def test_accelStructure_paramset1():
    #Database filename to load
    print(CLICopti.CellBase.celldatabase_TD_30GHz)

    #Load the database, with variables psi/an/dn
    base = CLICopti.CellBase.CellBase_linearInterpolation(CLICopti.CellBase.celldatabase_TD_30GHz, ["psi","a_n","d_n"])    

    #Create a structure
    acs = CLICopti.RFStructure.AccelStructure_paramSet1(base,25,120, 0.12, 0.015, 0.2)

    acs_f = acs.getCellFirst()
    #printCell_detailed(acs_f)
    assert compareFloat(acs_f.h,    0.0033326936579400807)
    assert compareFloat(acs_f.a,    0.001274755324162081)
    assert compareFloat(acs_f.d_n,  0.2)
    assert compareFloat(acs_f.a_n,  0.1275)
    assert compareFloat(acs_f.f0,   29.985)
    assert compareFloat(acs_f.psi,  120)
    assert compareFloat(acs_f.Q,    3895.0416666666665)
    assert compareFloat(acs_f.vg,   1.9825)
    assert compareFloat(acs_f.rQ,   36267.5)
    assert compareFloat(acs_f.Es,   2.0875000000000004)
    assert compareFloat(acs_f.Hs,   4.264583333333333)
    assert math.isnan  (acs_f.Sc)
    assert compareFloat(acs_f.f1mn, 41.465833333333336)
    assert compareFloat(acs_f.Q1mn, 12.327083333333334)
    assert compareFloat(acs_f.A1mn, 2251.8932049864748)

    acs_m = acs.getCellMid()
    #printCell_detailed(acs_m)
    assert compareFloat(acs_m.h,    0.0033326936579400807)
    assert compareFloat(acs_m.a,    0.0011997697168584292)
    assert compareFloat(acs_m.d_n,  0.2)
    assert compareFloat(acs_m.a_n,  0.12000000000000002)
    assert compareFloat(acs_m.f0,   29.985)
    assert compareFloat(acs_m.psi,  120)
    assert compareFloat(acs_m.Q,    3884.1666666666665)
    assert compareFloat(acs_m.vg,   1.5999999999999999)
    assert compareFloat(acs_m.rQ,   37690.0)
    assert compareFloat(acs_m.Es,   2.05)
    assert compareFloat(acs_m.Hs,   4.208333333333333)
    assert math.isnan  (acs_m.Sc)
    assert compareFloat(acs_m.f1mn, 41.99333333333334)
    assert compareFloat(acs_m.Q1mn, 11.058333333333334)
    assert compareFloat(acs_m.A1mn, 2416.1079313160717)

    acs_l = acs.getCellLast()
    #printCell_detailed(acs_l)
    assert compareFloat(acs_l.h,    0.0033326936579400807)
    assert compareFloat(acs_l.a,    0.0011247841095547773)
    assert compareFloat(acs_l.d_n,  0.2)
    assert compareFloat(acs_l.a_n,  0.1125)
    assert compareFloat(acs_l.f0,   29.985)
    assert compareFloat(acs_l.psi,  120)
    assert compareFloat(acs_l.Q,    3873.2916666666665)
    assert compareFloat(acs_l.vg,   1.2174999999999994)
    assert compareFloat(acs_l.rQ,   39112.5)
    assert compareFloat(acs_l.Es,   2.0125)
    assert compareFloat(acs_l.Hs,   4.152083333333333)
    assert math.isnan  (acs_l.Sc)
    assert compareFloat(acs_l.f1mn, 42.52083333333334)
    assert compareFloat(acs_l.Q1mn, 9.789583333333331)
    assert compareFloat(acs_l.A1mn, 2580.322657645668)


    #print("Length = ", acs.getL(), "[m]")
    assert compareFloat(acs.getL(), 25*0.0033326936579400807)

    #Testing the interpolator
    nPoints = 11

    z = np.linspace(0,acs.getL(), nPoints)
    vg = acs.getInterpolated(z,"vg")

    fDir = getAndMakeTestOutputFolderPath('test_accelStructure_paramset1_30GHz')
    doPlot = True
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        with open(os.path.join(fDir,'PLOTS.txt'),'w') as readme:
            readme.write('Could not import matplotlib.pyplot, so no plots. Sorry!\n')
            readme.close()
            #raise #Re-raises error
            doPlot = False
    if doPlot:
        plt.figure()
        plt.plot(np.asarray(z)*1e3,vg, '+-')
        plt.xlabel('z [mm]')
        plt.ylabel(r'vg [%c]')
        plt.savefig(os.path.join(fDir,f'vg.png'))

    #Testing the integration
    acs.calc_g_integrals(100)
    
    V_UL_1MW = acs.getVoltageUnloaded(1e6)/1e6
    assert V_UL_1MW == 2.646674304556897
    #print("V_UL(1 [MW])", V_UL_1MW, "[MV]")
    
    t_fill = acs.getTfill()*1e9
    assert t_fill == 17.71252877003441
    #print("t_fill =", t_fill, " [ns]")
    
    t_rise = acs.getTrise()*1e9
    print("t_rise =", t_rise, " [ns]")

    acs.writeProfileFile(os.path.join(fDir, "testfile_acs.dat"), 10e6)

    assert compareFiles(os.path.join(fDir, "testfile_acs.dat"), \
                        os.path.join(fDir, "testfile_acs_ref.dat")) \
                        == True
        

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_CLIC502():
    acs502 = CLICopti.RFStructure.AccelStructure_CLIC502(22)

    acs_f = acs502.getCellFirst()
    #printCell_detailed(acs_f)
    assert compareFloat(acs_f.h,    0.010414460158694757)
    assert compareFloat(acs_f.a,    0.003969905997898985)
    assert compareFloat(acs_f.d_n,  0.19971828200029382)
    assert compareFloat(acs_f.a_n,  0.1588331284838393)
    assert compareFloat(acs_f.f0,   11.9942)
    assert compareFloat(acs_f.psi,  150.0)
    assert compareFloat(acs_f.Q,    6364.724646333217)
    assert compareFloat(acs_f.vg,   2.056)
    assert compareFloat(acs_f.rQ,   10305.164006818122)
    assert compareFloat(acs_f.Es,   2.25)
    assert compareFloat(acs_f.Hs,   4.684)
    assert compareFloat(acs_f.Sc,   0.493)
    assert compareFloat(acs_f.f1mn, 15.8236489023112)
    assert compareFloat(acs_f.Q1mn, 16.78249817)
    assert compareFloat(acs_f.A1mn, 77.23885617073837)

    acs_m = acs502.getCellMid()
    #printCell_detailed(acs_m)
    assert compareFloat(acs_m.h,    0.010414460158694757)
    assert compareFloat(acs_m.a,    0.003624931998382552)
    assert compareFloat(acs_m.d_n,  0.18003450901468795)
    assert compareFloat(acs_m.a_n,  0.14503024956018074)
    assert compareFloat(acs_m.f0,   11.9942)
    assert compareFloat(acs_m.psi,  150.0)
    assert compareFloat(acs_m.Q,    6370.440247401987)
    assert compareFloat(acs_m.vg,   1.614)
    assert compareFloat(acs_m.rQ,   11213.610356866677)
    assert compareFloat(acs_m.Es,   2.23)
    assert compareFloat(acs_m.Hs,   4.511)
    assert compareFloat(acs_m.Sc,   0.435)
    assert compareFloat(acs_m.f1mn, 16.08192522809446)
    assert compareFloat(acs_m.Q1mn, 12.975146689999999)
    assert compareFloat(acs_m.A1mn, 94.83341870421668)

    acs_l = acs502.getCellLast()
    #printCell_detailed(acs_l)
    assert compareFloat(acs_l.h,    0.010414460158694757)
    assert compareFloat(acs_l.a,    0.003279940931450201)
    assert compareFloat(acs_l.d_n,  0.16035073602908206)
    assert compareFloat(acs_l.a_n,  0.13122737063652215)
    assert compareFloat(acs_l.f0,   11.9942)
    assert compareFloat(acs_l.psi,  150.0)
    assert compareFloat(acs_l.Q,    6382.94252496176)
    assert compareFloat(acs_l.vg,   1.234)
    assert compareFloat(acs_l.rQ,   12176.119276130432)
    assert compareFloat(acs_l.Es,   2.22)
    assert compareFloat(acs_l.Hs,   4.342)
    assert compareFloat(acs_l.Sc,   0.381)
    assert compareFloat(acs_l.f1mn, 16.340267131209757)
    assert compareFloat(acs_l.Q1mn, 9.16779521)
    assert compareFloat(acs_l.A1mn, 112.42886798529767)

    acs502.calc_g_integrals(1000)

    #Check against old CLIC_502 results
    Pref502 = 74.1942303887e6 #[W]
    V_UL = acs502.getVoltageUnloaded(Pref502)/1e6
    print(f"V_UL({Pref502/1e6} [MW])  =", V_UL, "[MV]")
    assert V_UL == 22.948054336312914

    G_UL = V_UL / acs502.getL()
    print("    average unloaded gradient =", G_UL, "[MV/m]")
    assert G_UL == 100.15818035968607
    print()

    #Consistency checks: 1W -> 1W
    assert compareFloat(acs502.getPowerUnloaded(acs502.getVoltageUnloaded(1.0)), 1.0)
    #Consistency checks: 1V -> 1V
    assert compareFloat(acs502.getVoltageUnloaded(acs502.getPowerUnloaded(1.0)), 1.0)


    dt_bunch = 0.5e-9 #[ns]
    I_beam=CLICopti.Constants.electron_charge*6.8e9/dt_bunch #[A]
    t_beam = 354*dt_bunch #[ns]
    print("I_beam =", I_beam, "[A]")
    assert compareFloat(I_beam, 2.1789599855999997)
    print("dt_bunch =", dt_bunch, "[ns]")
    print("t_beam =", t_beam*1e9, "[ns]")
    assert compareFloat(t_beam, 177e-9)
    print()

    V_LL = acs502.getLoadingVoltage(I_beam)/1e6
    print("Beam loading voltage =", V_LL, "[MV]")
    assert compareFloat(V_LL, 4.615403474889477)

    V_L = acs502.getVoltageLoaded(Pref502, I_beam)/1e6
    print(f"V_L({Pref502/1e6} [MW])  =", V_L, "[MV]")
    assert compareFloat(V_L, 18.332650861423442)

    G_L = V_L / acs502.getL()
    print( "     average loaded gradient =", G_L, "[MV/m]")
    assert compareFloat(G_L, 80.01397088135977)
    print()

    #Should get 74.1942303887 MW
    PL80 = acs502.getPowerLoaded(80e6*acs502.getL(), I_beam)/1e6
    print("Power to achieve 80 [MV/m] loaded gradient =", PL80, " [MW]")
    assert compareFloat(PL80, 74.17353339734548)

    #Efficiency (should get 39.6% total at t_rise=15.3ns)
    eff_ft = acs502.getFlattopEfficiency(Pref502, I_beam)*100
    print("RF to beam efficiency (flat-top) =", eff_ft, r"[%]")
    assert compareFloat(eff_ft, 53.83991780458034)
    eff_total = acs502.getTotalEfficiency(Pref502, I_beam, t_beam)*100
    assert compareFloat(eff_total, 39.259387576113525)
    print("RF to beam efficiency (total   ) =", eff_total, r"[%]")
    t_rise = acs502.getTrise()*1e9
    print("t_rise                           =", t_rise, "[ns]")
    assert compareFloat(t_rise, 17.65599675850891)
    t_fill = acs502.getTfill()*1e9
    print("t_fill =", t_fill, " [ns]")
    assert compareFloat(t_fill, 48.07997136975671)


    #Consistency check; must use a higher value than the beam loading voltage,
    # or else the power gets negative!
    # 10 MW -> 10 MW?
    assert compareFloat(acs502.getPowerLoaded(acs502.getVoltageLoaded(10.0e6,I_beam),I_beam)/1e6, 10.0)
    # 10 MV -> 10 MV?
    assert compareFloat(acs502.getVoltageLoaded(acs502.getPowerLoaded(10.0e6,I_beam),I_beam)/1e6, 10.0)

    #Field profiles

    fDir = getAndMakeTestOutputFolderPath('test_accelStructure_CLIC502')

    ## Unloaded

    acs502.writeProfileFile(os.path.join(fDir, "testfile_acs502.dat"), Pref502)

    assert compareFiles(os.path.join(fDir, "testfile_acs502.dat"), \
                        os.path.join(fDir, "testfile_acs502_ref.dat"))

    maxfield_acs502_UL = acs502.getMaxFields(Pref502)
    print("Unloaded max fields:\n", maxfield_acs502_UL)

    assert compareFloat(maxfield_acs502_UL.maxEs, 226.66721450478047) #[MV/m]
    assert maxfield_acs502_UL.maxEs_idx == 952
    assert compareFloat(maxfield_acs502_UL.maxHs, 454.3338559773985) #[kA/m]
    assert maxfield_acs502_UL.maxHs_idx == 295
    assert compareFloat(maxfield_acs502_UL.maxSc, 4.608709168566826) #[W/um^2]
    assert maxfield_acs502_UL.maxSc_idx == 0
    assert compareFloat(maxfield_acs502_UL.maxPC, 2.9744730785842113) #[MW/mm]
    assert maxfield_acs502_UL.maxSc_idx == 0

    acs502.writeDeltaTprofileFile(os.path.join(fDir, "testfile_acs502_deltaT_unloaded.dat"),\
                                   Pref502, t_beam, I_beam, False)
    assert compareFiles(os.path.join(fDir, "testfile_acs502_deltaT_unloaded.dat"), \
                        os.path.join(fDir, "testfile_acs502_deltaT_unloaded_ref.dat"))

    maxDeltaT_acs502_UL = acs502.getMaxDeltaT(Pref502, t_beam, I_beam, False)
    print(maxDeltaT_acs502_UL)

    assert compareFloat(maxDeltaT_acs502_UL.maxDeltaT, 41.61782914007496) #[K]
    assert maxDeltaT_acs502_UL.maxDeltaT_idx == 295

    ## Loaded

    acs502.writeProfileFile(os.path.join(fDir, "testfile_acs502_loaded.dat"), Pref502, I_beam)

    assert compareFiles(os.path.join(fDir, "testfile_acs502_loaded.dat"), \
                        os.path.join(fDir, "testfile_acs502_loaded_ref.dat"))

    maxfield_acs502_L = acs502.getMaxFields(Pref502, I_beam)
    print("Loaded max fields:\n", maxfield_acs502_L)

    assert compareFloat(maxfield_acs502_L.maxEs, 217.54480159627113) #[MV/m]
    assert maxfield_acs502_L.maxEs_idx == 0
    assert compareFloat(maxfield_acs502_L.maxHs, 452.87993363419287) #[kA/m]
    assert maxfield_acs502_L.maxHs_idx == 0
    assert compareFloat(maxfield_acs502_L.maxSc, 4.608709168566826) #[W/um^2]
    assert maxfield_acs502_L.maxSc_idx == 0
    assert compareFloat(maxfield_acs502_L.maxPC, 2.9744730785842113) #[MW/mm]
    assert maxfield_acs502_L.maxSc_idx == 0

    acs502.writeDeltaTprofileFile(os.path.join(fDir, "testfile_acs502_deltaT_loaded.dat"),\
                                   Pref502, t_beam, I_beam, True)
    assert compareFiles(os.path.join(fDir, "testfile_acs502_deltaT_loaded.dat"), \
                        os.path.join(fDir, "testfile_acs502_deltaT_loaded_ref.dat"))

    maxDeltaT_acs502_L = acs502.getMaxDeltaT(Pref502, t_beam, I_beam, True)
    print(maxDeltaT_acs502_L)

    assert compareFloat(maxDeltaT_acs502_L.maxDeltaT, 41.351891338060796) #[K]
    assert maxDeltaT_acs502_L.maxDeltaT_idx == 0

    ## Time power profile
    acs502.writeTimePowerProfileFile(os.path.join(fDir, "testfile_acs502_tProfile.dat"),\
                                     Pref502, t_beam, I_beam, 5000)
    assert compareFiles(os.path.join(fDir, "testfile_acs502_tProfile.dat"),os.path.join(fDir, "testfile_acs502_tProfile_ref.dat"))

    Pref08 = 0.8*Pref502/1e6
    extraTimePowerAboveFraction = acs502.getExtraTimePowerAboveFraction(Pref502, I_beam, 0.8)*1e9
    totalTimePowerAboveFraction = acs502.getExtraTimePowerAboveFraction(Pref502, I_beam, 0.8)*1e9 + t_beam*1e9
    print("Extra time with power > 0.8*P0 = ", Pref08, "[MW]:\n ",
       extraTimePowerAboveFraction, "[ns], total time = ", totalTimePowerAboveFraction , "[ns]")
    assert compareFloat(Pref08, 59.35538431096)
    assert compareFloat(extraTimePowerAboveFraction, 25.345636160327892)
    assert compareFloat(totalTimePowerAboveFraction, 202.3456361603279)

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_CLIC502_BDconstraints():

    #Creating an AccelStructure502
    acs502 = CLICopti.RFStructure.AccelStructure_CLIC502(22)

    dt_bunch = 0.5e-9 #[ns]
    I_beam=CLICopti.Constants.electron_charge*6.8e9/dt_bunch #[A]

    ## Check BD constraints
    max_Es = 300 #MV/m, at P0 max is 217.54
    max_Sc = 5.0 #W/um^2, at P0 max is 4.6
    print(f"Finding max power at max_Es = {max_Es} [MV/m], max_Sc = {max_Sc} [W/um^2], I_beam = {I_beam} [A]")

    acs502.calc_g_integrals(1000)
    max_P0 = acs502.getMaxAllowablePower(I_beam, max_Es, max_Sc)
    print(" Got max_P0 =", max_P0/1e6, " [MW]")
    assert compareFloat(max_P0/1e6, 71.27896001691923)
    maxFields_L = acs502.getMaxFields(max_P0, I_beam)
    print(" maxFields_L :", maxFields_L)
    maxFields_UL = acs502.getMaxFields(max_P0, 0.0)
    print(" maxFields_UL:", maxFields_UL)

    #Test that return 0.0 works (testing deltaT)
    max_Es_strict = max_Es/10 #MV/m, at P0 max is 217.54
    max_Sc_strict = max_Es/10 #W/um^2, at P0 max is 4.6
    print(f"Finding max power at max_Es = {max_Es_strict} [MV/m], max_Sc = {max_Sc_strict} [W/um^2], I_beam = {I_beam} [A]")

    max_P0_strict = acs502.getMaxAllowablePower(I_beam, max_Es_strict, max_Sc_strict)
    print(" Got max_P0_strict =", max_P0_strict/1e6, " [MW]")
    assert max_P0_strict == 0.0
    maxFields_L_strict = acs502.getMaxFields(max_P0_strict, I_beam)
    print(" maxFields_L_strict :", maxFields_L_strict) #Loading only!
    maxFields_UL_strict = acs502.getMaxFields(max_P0_strict, 0.0)
    print(" maxFields_UL:", maxFields_UL_strict) #Off

    #Get maximum allowable beam time from temperature rise
    max_deltaT = 50
    useLoadedField = True
    print("Finding maximum beam time allowable, max deltaT =", max_deltaT, "[K], power =", max_P0/1e6, "[MW]")
    print(" I_beam =", I_beam, "[A], useLoadedField=",useLoadedField)
    print(" This corresponds to loaded gradient", acs502.getVoltageLoaded(max_P0,I_beam)/acs502.getL()/1e6, "[MV/m]")
    t_beam_max = acs502.getMaxAllowableBeamTime_dT(max_P0, I_beam,useLoadedField)
    print("Got t_beam_max =", t_beam_max*1e9, "[ns]")
    assert compareFloat(t_beam_max, 300.22844374781147e-9)

    #Maximum times at given power
    Pref502 = 74.1942303887e6 #[W]

    print(f"Maximum beam time [ns] at Pref502 = {Pref502/1e6} [MW] and I_Beam = {I_beam} [A]:")
    print(f" Wasted beam pulse      : {acs502.getExtraTimePowerAboveFraction(Pref502, I_beam)*1e9} [ns]")
    assert compareFloat(acs502.getExtraTimePowerAboveFraction(Pref502, I_beam)*1e9, 19.009227120245917)
    print(f" Max beam time from Es  : {acs502.getMaxAllowableBeamTime_E(Pref502,I_beam)*1e9} [ns]")
    assert compareFloat(acs502.getMaxAllowableBeamTime_E(Pref502,I_beam)*1e9, 194.92182198405075)
    print(f" Max beam time from Sc  : {acs502.getMaxAllowableBeamTime_Sc(Pref502,I_beam)*1e9} [ns]")
    assert compareFloat(acs502.getMaxAllowableBeamTime_Sc(Pref502,I_beam)*1e9, 111.74991445744301)
    print(f" Max beam time from dT  : {acs502.getMaxAllowableBeamTime_dT(Pref502,I_beam)*1e9} [ns]")
    assert compareFloat(acs502.getMaxAllowableBeamTime_dT(Pref502,I_beam)*1e9, 270.29731036667727)
    print(f" Max beam time from P/C : {acs502.getMaxAllowableBeamTime_PC(Pref502,I_beam)*1e9} [ns]")
    assert compareFloat(acs502.getMaxAllowableBeamTime_PC(Pref502,I_beam)*1e9, 73.45705077443924)
    print(f" Max beam time, overall : {acs502.getMaxAllowableBeamTime(Pref502,I_beam)*1e9} [ns]")
    assert compareFloat(acs502.getMaxAllowableBeamTime(Pref502,I_beam)*1e9, 73.45705077443924)
    print(f" Max beam time, detailed:\n  {acs502.getMaxAllowableBeamTime_detailed(Pref502,I_beam)} [ns]")

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_CLIC502_WFconstraints():
    #Creating an AccelStructure502
    acs502 = CLICopti.RFStructure.AccelStructure_CLIC502(22)

    fDir = getAndMakeTestOutputFolderPath('test_accelStructure_CLIC502_WFconstraints')

    acs502.writeWakeFile(os.path.join(fDir, "testfile_acs502_wakeFile.dat"), 10.0, 0.0001)
    assert compareFiles(os.path.join(fDir, "testfile_acs502_wakeFile.dat"), os.path.join(fDir, "testfile_acs502_wakeFile_ref.dat"))

    #Just to run through the code from Python and make sure it doesn't crash
    wake_z = np.arange(10.0,step=0.0001) #[m]
    #  wakeFile << "# z[m] Wt[V/pC/mm/m] fabs(Wt) Envelope(Wt) Envelope_detuning(Wt)" << endl;

    wake_Wt            = acs502.getTransverseWakePotential(wake_z)
    wake_envWt         = acs502.getTransverseWakePotentialEnvelope(wake_z)
    wake_envDetuningWt = acs502.getTransverseWakePotentialEnvelope_detuning(wake_z)


    wake_absWt = np.fabs(wake_Wt)

    #Minimum bunch spacing; from paper, limit = 6.3 V/pV/mm/m
    minBunchSpacing = acs502.getMinBunchSpacing(6.3)
    print(f"Minimum bunch spacing = {minBunchSpacing} [cycles]")
    assert minBunchSpacing == 8

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_CLICG():
    "Testing the AccelStructure_CLICG, 24 cells, R05 variety, no database"

    dt_bunch = 0.5e-9 #[ns]
    I_beam = CLICopti.Constants.electron_charge*3.7e9/dt_bunch; #[A]
    print(f" I_beam = {I_beam} [A]")

    #Creating AccelStructure_CLICG; R05 variety, not database
    acsG_R05 = CLICopti.RFStructure.AccelStructure_CLICG(24, True)

    print ("first :", acsG_R05.getCellFirst())
    acsG_R05_f = acsG_R05.getCellFirst()
    #printCell_detailed(acsG_R05_f)
    assert compareFloat(acsG_R05_f.h,    0.008331595215465252)
    assert compareFloat(acsG_R05_f.a,    0.00315)
    assert compareFloat(acsG_R05_f.d_n,  0.20044180697834635)
    assert compareFloat(acsG_R05_f.a_n,  0.12602628582470876)
    assert compareFloat(acsG_R05_f.f0,   11.9942)
    assert compareFloat(acsG_R05_f.psi,  120.0)
    assert compareFloat(acsG_R05_f.Q,    5536.0)
    assert compareFloat(acsG_R05_f.vg,   1.65)
    assert compareFloat(acsG_R05_f.rQ,   14587.0)
    assert compareFloat(acsG_R05_f.Es,   1.95)
    assert compareFloat(acsG_R05_f.Hs,   4.1)
    assert compareFloat(acsG_R05_f.Sc,   0.41)
    assert compareFloat(acsG_R05_f.f1mn, 16.91)
    assert compareFloat(acsG_R05_f.Q1mn, 11.1)
    assert compareFloat(acsG_R05_f.A1mn, 125.0)
    print ("mid   :", acsG_R05.getCellMid())
    print ("last  :", acsG_R05.getCellLast())
    print()

    print("Length = ", acsG_R05.getL(), "[m]")
    print()

    assert compareFloat(acsG_R05.getL(), 0.19995828517116604)

    acsG_R05.calc_g_integrals(500)

    print("t_fill =", acsG_R05.getTfill()*1e9, " [ns]")
    print("t_rise =", acsG_R05.getTrise()*1e9, " [ns]")

    print(f"V24 = {acsG_R05.getVoltageUnloaded(1.0)} [V] (expected 3080 [V])" )
    assert compareFloat(acsG_R05.getVoltageUnloaded(1.0), 3121.892031359909)
    print(f"Pin at 100MV/m = {acsG_R05.getVoltageUnloaded(100e6*acsG_R05.getL())/1e6} [MW] (expected 42.1 [MW]) (unloaded)")
    print(f"Peak fields (unloaded):\n {acsG_R05.getMaxFields(acsG_R05.getPowerUnloaded(100e6*acsG_R05.getL()))}")
    print()

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_general_copy():
    acsG_R05 = CLICopti.RFStructure.AccelStructure_CLICG(24, True)

    acsG_R05_copy = CLICopti.RFStructure.AccelStructure_general.copy_structure(acsG_R05, "AccelStructure_general copy of acsG_R05")

    print ("first :", acsG_R05_copy.getCellFirst())
    acsG_R05_copy_f = acsG_R05_copy.getCellFirst()
    #printCell_detailed(acsG_R05_f)
    assert compareFloat(acsG_R05_copy_f.h,    0.008331595215465252)
    assert compareFloat(acsG_R05_copy_f.a,    0.00315)
    assert compareFloat(acsG_R05_copy_f.d_n,  0.20044180697834635)
    assert compareFloat(acsG_R05_copy_f.a_n,  0.12602628582470876)
    assert compareFloat(acsG_R05_copy_f.f0,   11.9942)
    assert compareFloat(acsG_R05_copy_f.psi,  120.0)
    assert compareFloat(acsG_R05_copy_f.Q,    5536.0)
    assert compareFloat(acsG_R05_copy_f.vg,   1.65)
    assert compareFloat(acsG_R05_copy_f.rQ,   14587.0)
    assert compareFloat(acsG_R05_copy_f.Es,   1.95)
    assert compareFloat(acsG_R05_copy_f.Hs,   4.1)
    assert compareFloat(acsG_R05_copy_f.Sc,   0.41)
    assert compareFloat(acsG_R05_copy_f.f1mn, 16.91)
    assert compareFloat(acsG_R05_copy_f.Q1mn, 11.1)
    assert compareFloat(acsG_R05_copy_f.A1mn, 125.0)

    acsG_R05_copy.calc_g_integrals(500)

    print("V24 =", acsG_R05_copy.getVoltageUnloaded(1.0), " [V] (expected 3080 V)")
    assert compareFloat(acsG_R05_copy.getVoltageUnloaded(1.0), 3121.8920313599074)
    print("Pin at 100 MV/m =", acsG_R05_copy.getPowerUnloaded(100e6*acsG_R05_copy.getL())/1e6,\
        "MW (expected 42.1 MW) (unloaded)")
    print("Peak fields (unloaded):", acsG_R05_copy.getMaxFields(100e6*acsG_R05_copy.getL()))

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_CLICG_noR05():
    "Testing the AccelStructure_CLICG, 24 cells, normal variety, no database"

    acsG = CLICopti.RFStructure.AccelStructure_CLICG(24,False)
    acsG.calc_g_integrals(500)

    ## I should add more stuff here...

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_TD25R05_KEK():
    "Testing the TD24R05 at the KEK frequency, by scaling CLIC_G base cells and using AccelStructure_general"

    #Make database with f0=11.424GHz, just to be used for scaling
    cBase11424 = CLICopti.CellBase.CellBase_compat(CLICopti.CellBase.celldatabase_TD_12GHz_v2,11.424, False, 3)

    acsG_R05 = CLICopti.RFStructure.AccelStructure_CLICG(24, True)

    #Scale a CLIC_G to 11.424 GHz
    KEK_Gfirst = CLICopti.CellParams.CellParams_copy(acsG_R05.getCellFirst())
    cBase11424.scaleCell(KEK_Gfirst)
    print("FIRST =", KEK_Gfirst)
    KEK_Gmid   =  CLICopti.CellParams.CellParams_copy(acsG_R05.getCellMid())
    cBase11424.scaleCell(KEK_Gmid)
    print("MID   =", KEK_Gmid)
    KEK_Glast =  CLICopti.CellParams.CellParams_copy(acsG_R05.getCellLast())
    cBase11424.scaleCell(KEK_Glast)
    print("LAST  =", KEK_Glast)

    h11424 = (KEK_Gfirst.h + KEK_Gmid.h + KEK_Glast.h) /3
    print("h11424 =", h11424, "[m]")

    assert compareFloat(h11424, 0.00874744566993464)

    #Create a new structure using these cells
    acsG_R05_24_KEK = CLICopti.RFStructure.AccelStructure_general(24, KEK_Gfirst,KEK_Gmid,KEK_Glast)
    acsG_R05_24_KEK.calc_g_integrals(500)

    #printCell_detailed(acsG_R05_f)
    acsG_R05_24_KEK_f = acsG_R05_24_KEK.getCellFirst()
    #printCell_detailed(acsG_R05_24_KEK_f)
    assert compareFloat(acsG_R05_24_KEK_f.h,    0.00874744566993464)
    assert compareFloat(acsG_R05_24_KEK_f.a,    0.0033072242647058823)
    assert compareFloat(acsG_R05_24_KEK_f.d_n,  0.20044180697834635)
    assert compareFloat(acsG_R05_24_KEK_f.a_n,  0.12602628582470876)
    assert compareFloat(acsG_R05_24_KEK_f.f0,   11.424)
    assert compareFloat(acsG_R05_24_KEK_f.psi,  120.0)
    assert compareFloat(acsG_R05_24_KEK_f.Q,    5672.475481526157)
    assert compareFloat(acsG_R05_24_KEK_f.vg,   1.65)
    assert compareFloat(acsG_R05_24_KEK_f.rQ,   13893.539210618466)
    assert compareFloat(acsG_R05_24_KEK_f.Es,   1.95)
    assert compareFloat(acsG_R05_24_KEK_f.Hs,   4.1)
    assert compareFloat(acsG_R05_24_KEK_f.Sc,   0.41)
    assert compareFloat(acsG_R05_24_KEK_f.f1mn, 16.10610461723166)
    assert compareFloat(acsG_R05_24_KEK_f.Q1mn, 11.1)
    assert compareFloat(acsG_R05_24_KEK_f.A1mn, 108.00671004706089)

    acsG_R05_24_KEK__P0 = acsG_R05_24_KEK.getPowerUnloaded( 100.0*1e6 * acsG_R05_24_KEK.getL() )
    print(f"acsG_R05_24_KEK__P0/1e6 = {acsG_R05_24_KEK__P0/1e6} [MW]")
    assert compareFloat(acsG_R05_24_KEK__P0/1e6, 44.84848935366418)

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_CLICG_CDR():
    "Standard CLIC_G as in the CDR"

    I_beam = 1.60217646e-19*3.72e9/0.5e-9
    Ncells = 24
    tBeam = 312*0.5e-9 #[s]

    print (f"I_beam = {I_beam} [A], Ncells = {Ncells}")
    base2 = CLICopti.CellBase.CellBase_linearInterpolation_freqScaling(CLICopti.CellBase.celldatabase_TD_30GHz,("psi","a_n","d_n"),11.9942)

    #Use the mm measurements
    acs2_li=CLICopti.RFStructure.AccelStructure_paramSet2(base2,Ncells,120.0,\
                                                          0.110022947942206, 0.016003337882503*2,\
                                                          0.160233420548558, 0.040208386429788*2)
    
    assert compareFloat(acs2_li.getL()*1e3, 199.958285171166)

    acs2_li.calc_g_integrals(500)

    assert compareFloat(acs2_li.getTfill()*1e9,51.37528057546825 )
    assert compareFloat(acs2_li.getTrise()*1e9,17.226188317344217)

    assert compareFloat(acs2_li.getPowerUnloaded(100e6*acs2_li.getL())/1e6, 42.82063603427942) # Pin[MW] at 100 MV/m (unloaded)

    peakFields_UL = acs2_li.getMaxFields(acs2_li.getPowerUnloaded(100e6*acs2_li.getL()))
    #print(peakFields_UL)
    #printPeakfields_detailed(peakFields_UL)
    assert compareFloat(peakFields_UL.maxEs, 213.79282371343498) #[MV/m]
    assert peakFields_UL.maxEs_idx == 325
    assert compareFloat(peakFields_UL.maxHs, 408.2045025696772) #[kA/m]
    assert peakFields_UL.maxHs_idx == 268
    assert compareFloat(peakFields_UL.maxSc, 0.0) #[W/um^2]
    assert peakFields_UL.maxSc_idx == 0
    assert compareFloat(peakFields_UL.maxPC, 2.163528854347456) #[MW/mm]
    assert peakFields_UL.maxPC_idx == 0

    P0 = acs2_li.getPowerLoaded(100e6*acs2_li.getL(),I_beam) #[MW]
    print(f"P0 = {P0} [W]")
    assert compareFloat(P0,58455345.05107197)

    # Max beam time (loaded)
    tmax_L = acs2_li.getMaxAllowableBeamTime_detailed(P0,I_beam)
    #print(tmax_L)
    #printMaxAllowableBeamTime_detailed(tmax_L,'tmax_L')
    assert compareFloat(tmax_L.power, 58455345.05107197) #[W]
    assert compareFloat(tmax_L.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L.beamCurrent_loading,    1.1920192862399999)    #[A]
    assert compareFloat(tmax_L.powerFraction, 0.85)
    assert compareFloat(tmax_L.wastedTime, 1.989463747168534e-08) #[s]
    assert compareFloat(tmax_L.time_E, 1.623354905586208e-07) #[s]
    assert compareFloat(tmax_L.time_Sc, float('inf')) #[s] NOTE must fix manually
    assert compareFloat(tmax_L.time_dT, 2.6967200813726633e-07) #[s]
    assert compareFloat(tmax_L.time_PC, 7.455756402042083e-08) #[s]
    assert compareFloat(tmax_L.time, 7.455756402042083e-08) #[s]
    assert tmax_L.which == 'P'
    assert compareFloat(tmax_L.maxFields.maxEs, 223.43831626556974) #[MV/m]
    assert tmax_L.maxFields.maxEs_idx == 97
    assert compareFloat(tmax_L.maxFields.maxHs, 451.88568963769325) #[kA/m]
    assert tmax_L.maxFields.maxHs_idx == 0
    assert compareFloat(tmax_L.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_L.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L.maxFields.maxPC, 2.9534784492128403) #[MW/mm]
    assert tmax_L.maxFields.maxPC_idx == 0
    
    # Max beam time (loaded pulse, no beam)
    tmax_L_NB = acs2_li.getMaxAllowableBeamTime_detailed(P0,I_beam,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_NB,'tmax_L_NB')
    assert compareFloat(tmax_L_NB.power, 58455345.05107197) #[W]
    assert compareFloat(tmax_L_NB.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L_NB.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_NB.powerFraction, 0.85)
    assert compareFloat(tmax_L_NB.wastedTime, 1.989463747168534e-08) #[s]
    assert compareFloat(tmax_L_NB.time_E, 7.345099369393419e-08) #[s]
    assert compareFloat(tmax_L_NB.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_L_NB.time_dT, 2.0943456003735136e-07) #[s]
    assert compareFloat(tmax_L_NB.time_PC, 7.455756402042083e-08) #[s]
    assert compareFloat(tmax_L_NB.time, 7.345099369393419e-08) #[s]
    assert tmax_L_NB.which == 'E'
    assert compareFloat(tmax_L_NB.maxFields.maxEs, 249.79208938405742) #[MV/m]
    assert tmax_L_NB.maxFields.maxEs_idx == 325
    assert compareFloat(tmax_L_NB.maxFields.maxHs, 476.93956149591673) #[kA/m]
    assert tmax_L_NB.maxFields.maxHs_idx == 268
    assert compareFloat(tmax_L_NB.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_L_NB.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L_NB.maxFields.maxPC, 2.9534784492128403) #[MW/mm]
    assert tmax_L_NB.maxFields.maxPC_idx == 0

    # Max beam time (loaded power, I_beam=0)
    tmax_L_BP2 = acs2_li.getMaxAllowableBeamTime_detailed(P0,0.0,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_BP2, 'tmax_L_BP2')
    assert compareFloat(tmax_L_BP2.power, 58455345.05107197) #[W]
    assert compareFloat(tmax_L_BP2.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_L_BP2.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_BP2.powerFraction, 0.85)
    assert compareFloat(tmax_L_BP2.wastedTime, 5.654313707067154e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_E, 3.6802494094948e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_L_BP2.time_dT, 1.905087458938487e-07) #[s]
    assert compareFloat(tmax_L_BP2.time_PC, 3.790906442143464e-08) #[s]
    assert compareFloat(tmax_L_BP2.time, 3.6802494094948e-08) #[s]
    assert tmax_L_BP2.which == 'E'
    assert compareFloat(tmax_L_BP2.maxFields.maxEs, 249.79208938405742) #[MV/m]
    assert tmax_L_BP2.maxFields.maxEs_idx == 325
    assert compareFloat(tmax_L_BP2.maxFields.maxHs, 476.93956149591673) #[kA/m]
    assert tmax_L_BP2.maxFields.maxHs_idx == 268
    assert compareFloat(tmax_L_BP2.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_L_BP2.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L_BP2.maxFields.maxPC, 2.9534784492128403) #[MW/mm]
    assert tmax_L_BP2.maxFields.maxPC_idx == 0

    # Max beam time (P(G_UL = 100 MV/m))
    tmax_PUL100 = acs2_li.getMaxAllowableBeamTime_detailed(acs2_li.getPowerUnloaded(100e6*acs2_li.getL()), 0.0)
    #printMaxAllowableBeamTime_detailed(tmax_PUL100, 'tmax_PUL100')
    assert compareFloat(tmax_PUL100.power, 42820636.03427939) #[W]
    assert compareFloat(tmax_PUL100.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_PUL100.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_PUL100.powerFraction, 0.85)
    assert compareFloat(tmax_PUL100.wastedTime, 5.654313707067154e-08) #[s]
    assert compareFloat(tmax_PUL100.time_E, 1.8092609098764523e-07) #[s]
    assert compareFloat(tmax_PUL100.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_PUL100.time_dT, 4.0677994363942575e-07) #[s]
    assert compareFloat(tmax_PUL100.time_PC, 1.8374118150598778e-07) #[s]
    assert compareFloat(tmax_PUL100.time, 1.8092609098764523e-07) #[s]
    assert tmax_PUL100.which == 'E'
    assert compareFloat(tmax_PUL100.maxFields.maxEs, 213.79282371343498) #[MV/m]
    assert tmax_PUL100.maxFields.maxEs_idx == 325
    assert compareFloat(tmax_PUL100.maxFields.maxHs, 408.2045025696772) #[kA/m]
    assert tmax_PUL100.maxFields.maxHs_idx == 268
    assert compareFloat(tmax_PUL100.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_PUL100.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_PUL100.maxFields.maxPC, 2.163528854347456) #[MW/mm]
    assert tmax_PUL100.maxFields.maxPC_idx == 0

    assert compareFloat(1.60217646e-19*3.72e9*312 * acs2_li.getVoltageLoaded(P0, I_beam), 3.71832446493312) # Energy to beam [J]
    assert compareFloat(P0 * (acs2_li.getTfill()+ acs2_li.getTrise() + tBeam), 13.129156363106963) # Energy to structure [J]
    assert compareFloat(acs2_li.getTotalEfficiency(P0,I_beam,tBeam)*100, 28.3211225618551) # RF -> beam efficiency [%]

    # Min bunch spacing [cycles] at 6.6 V/pC/mm/m
    assert acs2_li.getMinBunchSpacing(6.6) == 6

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_paramset2_CellbaseCompat():
    "Testing paramset2 with CellBase_Compat"

    I_beam = 1.60217646e-19*3.72e9/0.5e-9
    Ncells = 24
    tBeam = 312*0.5e-9 #[s]

    print (f"I_beam = {I_beam} [A], Ncells = {Ncells}")

    base3=CLICopti.CellBase.CellBase_compat(CLICopti.CellBase.celldatabase_TD_30GHz, 11.9942)
    acs2=CLICopti.RFStructure.AccelStructure_paramSet2(base3,Ncells,120.0,\
                                                       0.110022947942206, 0.016003337882503*2,
                                                       0.160233420548558, 0.040208386429788*2)
    
    assert compareFloat(acs2.getL()*1e3, 199.958285171166)

    acs2.calc_g_integrals(500)

    assert compareFloat(acs2.getTfill()*1e9,56.00612659750887 )
    assert compareFloat(acs2.getTrise()*1e9,20.80032612946625)

    assert compareFloat(acs2.getPowerUnloaded(100e6*acs2.getL())/1e6, 39.98577756969919) # Pin[MW] at 100 MV/m (unloaded)

    peakFields_UL = acs2.getMaxFields(acs2.getPowerUnloaded(100e6*acs2.getL()))
    #print(peakFields_UL)
    #printPeakfields_detailed(peakFields_UL, 'peakFields_UL')
    assert compareFloat(peakFields_UL.maxEs, 209.16091780789293) #[MV/m]
    assert peakFields_UL.maxEs_idx == 468
    assert compareFloat(peakFields_UL.maxHs, 399.65872832016777) #[kA/m]
    assert peakFields_UL.maxHs_idx == 286
    assert compareFloat(peakFields_UL.maxSc, 0.0) #[W/um^2]
    assert peakFields_UL.maxSc_idx == 0
    assert compareFloat(peakFields_UL.maxPC, 2.020296556695442) #[MW/mm]
    assert peakFields_UL.maxPC_idx == 0

    P0 = acs2.getPowerLoaded(100e6*acs2.getL(),I_beam) #[MW]
    print(f"P0 = {P0} [W]")
    assert compareFloat(P0/1e6,55.95627057882986)

    # Max beam time (loaded)
    tmax_L = acs2.getMaxAllowableBeamTime_detailed(P0,I_beam)
    #print(tmax_L)
    #printMaxAllowableBeamTime_detailed(tmax_L,'tmax_L')
    assert compareFloat(tmax_L.power, 55956270.57882982) #[W]
    assert compareFloat(tmax_L.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L.beamCurrent_loading,    1.1920192862399999)    #[A]
    assert compareFloat(tmax_L.powerFraction, 0.85)
    assert compareFloat(tmax_L.wastedTime, 2.195138121356079e-08) #[s]
    assert compareFloat(tmax_L.time_E, 1.5594300671640168e-07) #[s]
    assert compareFloat(tmax_L.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_L.time_dT, 2.316536325890847e-07) #[s]
    assert compareFloat(tmax_L.time_PC, 8.57294713674866e-08) #[s]
    assert compareFloat(tmax_L.time, 8.57294713674866e-08) #[s]
    assert tmax_L.which == 'P'
    assert compareFloat(tmax_L.maxFields.maxEs, 224.3368610339282) #[MV/m]
    assert tmax_L.maxFields.maxEs_idx == 0
    assert compareFloat(tmax_L.maxFields.maxHs, 465.721587418097) #[kA/m]
    assert tmax_L.maxFields.maxHs_idx == 0
    assert compareFloat(tmax_L.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_L.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L.maxFields.maxPC, 2.8272117649550284) #[MW/mm]
    assert tmax_L.maxFields.maxPC_idx == 0
    
    # Max beam time (loaded pulse, no beam)
    tmax_L_NB = acs2.getMaxAllowableBeamTime_detailed(P0,I_beam,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_NB,'tmax_L_NB')
    assert compareFloat(tmax_L_NB.power, 55956270.57882982) #[W]
    assert compareFloat(tmax_L_NB.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L_NB.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_NB.powerFraction, 0.85)
    assert compareFloat(tmax_L_NB.wastedTime, 2.195138121356079e-08) #[s]
    assert compareFloat(tmax_L_NB.time_E, 7.68705189033739e-08) #[s]
    assert compareFloat(tmax_L_NB.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_L_NB.time_dT, 2.1560420870087208e-07) #[s]
    assert compareFloat(tmax_L_NB.time_PC, 8.57294713674866e-08) #[s]
    assert compareFloat(tmax_L_NB.time, 7.68705189033739e-08) #[s]
    assert tmax_L_NB.which == 'E'
    assert compareFloat(tmax_L_NB.maxFields.maxEs, 247.42988127627999) #[MV/m]
    assert tmax_L_NB.maxFields.maxEs_idx == 468
    assert compareFloat(tmax_L_NB.maxFields.maxHs, 472.7819744514265) #[kA/m]
    assert tmax_L_NB.maxFields.maxHs_idx == 286
    assert compareFloat(tmax_L_NB.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_L_NB.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L_NB.maxFields.maxPC, 2.8272117649550284) #[MW/mm]
    assert tmax_L_NB.maxFields.maxPC_idx == 0

    # Max beam time (loaded power, I_beam=0)
    tmax_L_BP2 = acs2.getMaxAllowableBeamTime_detailed(P0,0.0,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_BP2, 'tmax_L_BP2')
    assert compareFloat(tmax_L_BP2.power, 55956270.57882982) #[W]
    assert compareFloat(tmax_L_BP2.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_L_BP2.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_BP2.powerFraction, 0.85)
    assert compareFloat(tmax_L_BP2.wastedTime, 6.224622443634874e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_E, 3.657567568058595e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_L_BP2.time_dT, 1.9300995481149224e-07) #[s]
    assert compareFloat(tmax_L_BP2.time_PC, 4.543462814469865e-08) #[s]
    assert compareFloat(tmax_L_BP2.time, 3.657567568058595e-08) #[s]
    assert tmax_L_BP2.which == 'E'
    assert compareFloat(tmax_L_BP2.maxFields.maxEs, 247.42988127627999) #[MV/m]
    assert tmax_L_BP2.maxFields.maxEs_idx == 468
    assert compareFloat(tmax_L_BP2.maxFields.maxHs, 472.7819744514265) #[kA/m]
    assert tmax_L_BP2.maxFields.maxHs_idx == 286
    assert compareFloat(tmax_L_BP2.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_L_BP2.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L_BP2.maxFields.maxPC, 2.8272117649550284) #[MW/mm]
    assert tmax_L_BP2.maxFields.maxPC_idx == 0

    # Max beam time (P(G_UL = 100 MV/m))
    tmax_PUL100 = acs2.getMaxAllowableBeamTime_detailed(acs2.getPowerUnloaded(100e6*acs2.getL()), 0.0)
    #printMaxAllowableBeamTime_detailed(tmax_PUL100, 'tmax_PUL100')
    assert compareFloat(tmax_PUL100.power, 39985777.56969917) #[W]
    assert compareFloat(tmax_PUL100.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_PUL100.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_PUL100.powerFraction, 0.85)
    assert compareFloat(tmax_PUL100.wastedTime, 6.224622443634874e-08) #[s]
    assert compareFloat(tmax_PUL100.time_E, 2.0857509360703312e-07) #[s]
    assert compareFloat(tmax_PUL100.time_Sc, float('inf')) #[s]
    assert compareFloat(tmax_PUL100.time_dT, 4.416301212252588e-07) #[s]
    assert compareFloat(tmax_PUL100.time_PC, 2.3285304393965917e-07) #[s]
    assert compareFloat(tmax_PUL100.time, 2.0857509360703312e-07) #[s]
    assert tmax_PUL100.which == 'E'
    assert compareFloat(tmax_PUL100.maxFields.maxEs, 209.16091780789293) #[MV/m]
    assert tmax_PUL100.maxFields.maxEs_idx == 468
    assert compareFloat(tmax_PUL100.maxFields.maxHs, 399.65872832016777) #[kA/m]
    assert tmax_PUL100.maxFields.maxHs_idx == 286
    assert compareFloat(tmax_PUL100.maxFields.maxSc, 0.0) #[W/um^2]
    assert tmax_PUL100.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_PUL100.maxFields.maxPC, 2.020296556695442) #[MW/mm]
    assert tmax_PUL100.maxFields.maxPC_idx == 0

    assert compareFloat(1.60217646e-19*3.72e9*312 * acs2.getVoltageLoaded(P0, I_beam), 3.71832446493312) # Energy to beam [J]
    assert compareFloat(P0 * (acs2.getTfill()+ acs2.getTrise() + tBeam), 13.026980861288184) # Energy to structure [J]
    assert compareFloat(acs2.getTotalEfficiency(P0,I_beam,tBeam)*100, 28.543255759150867) # RF -> beam efficiency [%]

    # Min bunch spacing [cycles] at 6.6 V/pC/mm/m
    assert acs2.getMinBunchSpacing(6.6) == 6

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_paramset2_CellbaseCompat_DB1():
    "Testing paramset2_noPsi with CellBase_compat and 12 GHz database / v1"

    I_beam = 1.60217646e-19*3.72e9/0.5e-9
    Ncells = 24
    tBeam = 312*0.5e-9 #[s]

    print (f"I_beam = {I_beam} [A], Ncells = {Ncells}")

    base4 = CLICopti.CellBase.CellBase_compat(CLICopti.CellBase.celldatabase_TD_12GHz_v1, 11.9942, False, 2)
    acs2_DB12v1 = CLICopti.RFStructure.AccelStructure_paramSet2_noPsi \
           (base4, Ncells,\
            0.110022947942206, 0.016003337882503*2,
            0.160233420548558, 0.040208386429788*2)
    
    assert compareFloat(acs2_DB12v1.getL()*1e3, 199.958285171166)

    acs2_DB12v1.calc_g_integrals(500)

    assert compareFloat(acs2_DB12v1.getTfill()*1e9,56.116040235659604 )
    assert compareFloat(acs2_DB12v1.getTrise()*1e9,20.586379892922274)

    assert compareFloat(acs2_DB12v1.getPowerUnloaded(100e6*acs2_DB12v1.getL())/1e6, 41.547022640826576) # Pin[MW] at 100 MV/m (unloaded)

    peakFields_UL = acs2_DB12v1.getMaxFields(acs2_DB12v1.getPowerUnloaded(100e6*acs2_DB12v1.getL()))
    print(peakFields_UL)
    #printPeakfields_detailed(peakFields_UL, 'peakFields_UL')
    assert compareFloat(peakFields_UL.maxEs, 209.4361969576816) #[MV/m]
    assert peakFields_UL.maxEs_idx == 394
    assert compareFloat(peakFields_UL.maxHs, 399.8330154376679) #[kA/m]
    assert peakFields_UL.maxHs_idx == 140
    assert compareFloat(peakFields_UL.maxSc, 3.9470635065624) #[W/um^2]
    assert peakFields_UL.maxSc_idx == 135
    assert compareFloat(peakFields_UL.maxPC, 2.0991839940447448) #[MW/mm]
    assert peakFields_UL.maxPC_idx == 0
    
    P0 = acs2_DB12v1.getPowerLoaded(100e6*acs2_DB12v1.getL(),I_beam) #[MW]
    print(f"P0 = {P0} [W]")
    assert compareFloat(P0/1e6,57.85371331076416)

    # Max beam time (loaded)
    tmax_L = acs2_DB12v1.getMaxAllowableBeamTime_detailed(P0,I_beam)
    #print(tmax_L)
    #printMaxAllowableBeamTime_detailed(tmax_L,'tmax_L')
    assert compareFloat(tmax_L.power, 57853713.31076415) #[W]
    assert compareFloat(tmax_L.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L.beamCurrent_loading,    1.1920192862399999)    #[A]
    assert compareFloat(tmax_L.powerFraction, 0.85)
    assert compareFloat(tmax_L.wastedTime, 2.1902239925313628e-08) #[s]
    assert compareFloat(tmax_L.time_E, 1.3846094648982187e-07) #[s]
    assert compareFloat(tmax_L.time_Sc, 5.8028646249413877e-08) #[s]
    assert compareFloat(tmax_L.time_dT, 2.2677627519967985e-07) #[s]
    assert compareFloat(tmax_L.time_PC, 7.55267022763872e-08) #[s]
    assert compareFloat(tmax_L.time, 5.8028646249413877e-08) #[s]
    assert tmax_L.which == 'S'
    assert compareFloat(tmax_L.maxFields.maxEs, 228.2497097365091) #[MV/m]
    assert tmax_L.maxFields.maxEs_idx == 0
    assert compareFloat(tmax_L.maxFields.maxHs, 467.7907560614718) #[kA/m]
    assert tmax_L.maxFields.maxHs_idx == 0
    assert compareFloat(tmax_L.maxFields.maxSc, 5.430399499086914) #[W/um^2]
    assert tmax_L.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L.maxFields.maxPC, 2.9230876548701206) #[MW/mm]
    assert tmax_L.maxFields.maxPC_idx == 0
    
    # Max beam time (loaded pulse, no beam)
    tmax_L_NB = acs2_DB12v1.getMaxAllowableBeamTime_detailed(P0,I_beam,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_NB,'tmax_L_NB')
    assert compareFloat(tmax_L_NB.power, 57853713.31076415) #[W]
    assert compareFloat(tmax_L_NB.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L_NB.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_NB.powerFraction, 0.85)
    assert compareFloat(tmax_L_NB.wastedTime, 2.1902239925313628e-08) #[s]
    assert compareFloat(tmax_L_NB.time_E, 7.761117370489356e-08) #[s]
    assert compareFloat(tmax_L_NB.time_Sc, 5.519052643408348e-08) #[s]
    assert compareFloat(tmax_L_NB.time_dT, 2.1768854946557506e-07) #[s]
    assert compareFloat(tmax_L_NB.time_PC, 7.55267022763872e-08) #[s]
    assert compareFloat(tmax_L_NB.time, 5.519052643408348e-08) #[s]
    assert tmax_L_NB.which == 'S'
    assert compareFloat(tmax_L_NB.maxFields.maxEs, 247.14248513591733) #[MV/m]
    assert tmax_L_NB.maxFields.maxEs_idx == 394
    assert compareFloat(tmax_L_NB.maxFields.maxHs, 471.8177970669484) #[kA/m]
    assert tmax_L_NB.maxFields.maxHs_idx == 140
    assert compareFloat(tmax_L_NB.maxFields.maxSc, 5.496236938616346) #[W/um^2]
    assert tmax_L_NB.maxFields.maxSc_idx == 135
    assert compareFloat(tmax_L_NB.maxFields.maxPC, 2.9230876548701206) #[MW/mm]
    assert tmax_L_NB.maxFields.maxPC_idx == 0

    # Max beam time (loaded power, I_beam=0)
    tmax_L_BP2 = acs2_DB12v1.getMaxAllowableBeamTime_detailed(P0,0.0,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_BP2, 'tmax_L_BP2')
    assert compareFloat(tmax_L_BP2.power, 57853713.31076415) #[W]
    assert compareFloat(tmax_L_BP2.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_L_BP2.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_BP2.powerFraction, 0.85)
    assert compareFloat(tmax_L_BP2.wastedTime, 6.229195420353629e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_E, 3.72214594266709e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_Sc, 1.480081215586082e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_dT, 1.9513598239148923e-07) #[s]
    assert compareFloat(tmax_L_BP2.time_PC, 3.5136987998164534e-08) #[s]
    assert compareFloat(tmax_L_BP2.time, 1.480081215586082e-08) #[s]
    assert tmax_L_BP2.which == 'S'
    assert compareFloat(tmax_L_BP2.maxFields.maxEs, 247.14248513591733) #[MV/m]
    assert tmax_L_BP2.maxFields.maxEs_idx == 394
    assert compareFloat(tmax_L_BP2.maxFields.maxHs, 471.8177970669484) #[kA/m]
    assert tmax_L_BP2.maxFields.maxHs_idx == 140
    assert compareFloat(tmax_L_BP2.maxFields.maxSc, 5.496236938616346) #[W/um^2]
    assert tmax_L_BP2.maxFields.maxSc_idx == 135
    assert compareFloat(tmax_L_BP2.maxFields.maxPC, 2.9230876548701206) #[MW/mm]
    assert tmax_L_BP2.maxFields.maxPC_idx == 0

    # Max beam time (P(G_UL = 100 MV/m))
    tmax_PUL100 = acs2_DB12v1.getMaxAllowableBeamTime_detailed(acs2_DB12v1.getPowerUnloaded(100e6*acs2_DB12v1.getL()), 0.0)
    #printMaxAllowableBeamTime_detailed(tmax_PUL100, 'tmax_PUL100')
    assert compareFloat(tmax_PUL100.power, 41547022.64082655) #[W]
    assert compareFloat(tmax_PUL100.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_PUL100.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_PUL100.powerFraction, 0.85)
    assert compareFloat(tmax_PUL100.wastedTime, 6.229195420353629e-08) #[s]
    assert compareFloat(tmax_PUL100.time_E, 2.064005937586041e-07) #[s]
    assert compareFloat(tmax_PUL100.time_Sc, 1.4586341969943092e-07) #[s]
    assert compareFloat(tmax_PUL100.time_dT, 4.407130112887896e-07) #[s]
    assert compareFloat(tmax_PUL100.time_PC, 2.0077238828510965e-07) #[s]
    assert compareFloat(tmax_PUL100.time, 1.4586341969943092e-07) #[s]
    assert tmax_PUL100.which == 'S'
    assert compareFloat(tmax_PUL100.maxFields.maxEs, 209.4361969576816) #[MV/m]
    assert tmax_PUL100.maxFields.maxEs_idx == 394
    assert compareFloat(tmax_PUL100.maxFields.maxHs, 399.8330154376679) #[kA/m]
    assert tmax_PUL100.maxFields.maxHs_idx == 140
    assert compareFloat(tmax_PUL100.maxFields.maxSc, 3.9470635065624) #[W/um^2]
    assert tmax_PUL100.maxFields.maxSc_idx == 135
    assert compareFloat(tmax_PUL100.maxFields.maxPC, 2.0991839940447448) #[MW/mm]
    assert tmax_PUL100.maxFields.maxPC_idx == 0

    assert compareFloat(1.60217646e-19*3.72e9*312 * acs2_DB12v1.getVoltageLoaded(P0, I_beam), 3.7183244649331195) # Energy to beam [J]
    assert compareFloat(P0 * (acs2_DB12v1.getTfill()+ acs2_DB12v1.getTrise() + tBeam), 13.462699100839972) # Energy to structure [J]
    assert compareFloat(acs2_DB12v1.getTotalEfficiency(P0,I_beam,tBeam)*100, 27.61945756257097) # RF -> beam efficiency [%]

    # Min bunch spacing [cycles] at 6.6 V/pC/mm/m
    assert acs2_DB12v1.getMinBunchSpacing(6.6) == 6

    #Trigger a failure and a printout
    #assert False


@pytest.mark.structureLibrary
def test_paramset2_CellbaseCompat_DB2():
    "Testing paramset2_noPsi with CellBase_Compat and 12 GHz DB / v2"

    I_beam = 1.60217646e-19*3.72e9/0.5e-9
    Ncells = 24
    tBeam = 312*0.5e-9 #[s]

    print (f"I_beam = {I_beam} [A], Ncells = {Ncells}")

    base5 = CLICopti.CellBase.CellBase_compat(CLICopti.CellBase.celldatabase_TD_12GHz_v2, 11.9942, False, 2)
    acs2_DB12v2 = CLICopti.RFStructure.AccelStructure_paramSet2_noPsi \
               (base5, Ncells,\
                0.110022947942206, 0.016003337882503*2,
                0.160233420548558, 0.040208386429788*2)

    
    assert compareFloat(acs2_DB12v2.getL()*1e3, 199.958285171166)

    acs2_DB12v2.calc_g_integrals(500)

    assert compareFloat(acs2_DB12v2.getTfill()*1e9,56.12765311368474 )
    assert compareFloat(acs2_DB12v2.getTrise()*1e9,20.515780832722882)

    assert compareFloat(acs2_DB12v2.getPowerUnloaded(100e6*acs2_DB12v2.getL())/1e6, 41.579148652665396) # Pin[MW] at 100 MV/m (unloaded)

    peakFields_UL = acs2_DB12v2.getMaxFields(acs2_DB12v2.getPowerUnloaded(100e6*acs2_DB12v2.getL()))
    print(peakFields_UL)
    #printPeakfields_detailed(peakFields_UL, 'peakFields_UL')
    assert compareFloat(peakFields_UL.maxEs, 210.02995389773972) #[MV/m]
    assert peakFields_UL.maxEs_idx == 394
    assert compareFloat(peakFields_UL.maxHs, 400.48279259613315) #[kA/m]
    assert peakFields_UL.maxHs_idx == 122
    assert compareFloat(peakFields_UL.maxSc, 3.9237251548225753) #[W/um^2]
    assert peakFields_UL.maxSc_idx == 177
    assert compareFloat(peakFields_UL.maxPC, 2.100801988520487) #[MW/mm]
    assert peakFields_UL.maxPC_idx == 0
    
    P0 = acs2_DB12v2.getPowerLoaded(100e6*acs2_DB12v2.getL(),I_beam) #[MW]
    print(f"P0 = {P0} [W]")
    assert compareFloat(P0/1e6, 57.89564255691098)

    # Max beam time (loaded)
    tmax_L = acs2_DB12v2.getMaxAllowableBeamTime_detailed(P0,I_beam)
    #print(tmax_L)
    #printMaxAllowableBeamTime_detailed(tmax_L,'tmax_L')
    assert compareFloat(tmax_L.power, 57895642.55691097) #[W]
    assert compareFloat(tmax_L.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L.beamCurrent_loading,    1.1920192862399999)    #[A]
    assert compareFloat(tmax_L.powerFraction, 0.85)
    assert compareFloat(tmax_L.wastedTime, 2.1880956049733234e-08) #[s]
    assert compareFloat(tmax_L.time_E, 1.6152719415381015e-07) #[s]
    assert compareFloat(tmax_L.time_Sc, 6.336718125410813e-08) #[s]
    assert compareFloat(tmax_L.time_dT, 2.2273265411615614e-07) #[s]
    assert compareFloat(tmax_L.time_PC, 7.533717941280613e-08) #[s]
    assert compareFloat(tmax_L.time, 6.336718125410813e-08) #[s]
    assert tmax_L.which == 'S'
    assert compareFloat(tmax_L.maxFields.maxEs, 223.19848459947423) #[MV/m]
    assert tmax_L.maxFields.maxEs_idx == 14
    assert compareFloat(tmax_L.maxFields.maxHs, 469.5647260058544) #[kA/m]
    assert tmax_L.maxFields.maxHs_idx == 0
    assert compareFloat(tmax_L.maxFields.maxSc, 5.315062271630061) #[W/um^2]
    assert tmax_L.maxFields.maxSc_idx == 0
    assert compareFloat(tmax_L.maxFields.maxPC, 2.925198926660397) #[MW/mm]
    assert tmax_L.maxFields.maxPC_idx == 0
    
    # Max beam time (loaded pulse, no beam)
    tmax_L_NB = acs2_DB12v2.getMaxAllowableBeamTime_detailed(P0,I_beam,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_NB,'tmax_L_NB')
    assert compareFloat(tmax_L_NB.power, 57895642.55691097) #[W]
    assert compareFloat(tmax_L_NB.beamCurrent_pulseShape, 1.1920192862399999) #[A]
    assert compareFloat(tmax_L_NB.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_NB.powerFraction, 0.85)
    assert compareFloat(tmax_L_NB.wastedTime, 2.1880956049733234e-08) #[s]
    assert compareFloat(tmax_L_NB.time_E, 7.59706147291554e-08) #[s]
    assert compareFloat(tmax_L_NB.time_Sc, 5.660706455184635e-08) #[s]
    assert compareFloat(tmax_L_NB.time_dT, 2.160210768538127e-07) #[s]
    assert compareFloat(tmax_L_NB.time_PC, 7.533717941280613e-08) #[s]
    assert compareFloat(tmax_L_NB.time, 5.660706455184635e-08) #[s]
    assert tmax_L_NB.which == 'S'
    assert compareFloat(tmax_L_NB.maxFields.maxEs, 247.8371349039937) #[MV/m]
    assert tmax_L_NB.maxFields.maxEs_idx == 394
    assert compareFloat(tmax_L_NB.maxFields.maxHs, 472.57310708976985) #[kA/m]
    assert tmax_L_NB.maxFields.maxHs_idx == 122
    assert compareFloat(tmax_L_NB.maxFields.maxSc, 5.463473794348739) #[W/um^2]
    assert tmax_L_NB.maxFields.maxSc_idx == 177
    assert compareFloat(tmax_L_NB.maxFields.maxPC, 2.925198926660397) #[MW/mm]
    assert tmax_L_NB.maxFields.maxPC_idx == 0
    
    # Max beam time (loaded power, I_beam=0)
    tmax_L_BP2 = acs2_DB12v2.getMaxAllowableBeamTime_detailed(P0,0.0,0.0)
    #printMaxAllowableBeamTime_detailed(tmax_L_BP2, 'tmax_L_BP2')
    assert compareFloat(tmax_L_BP2.power, 57895642.55691097) #[W]
    assert compareFloat(tmax_L_BP2.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_L_BP2.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_L_BP2.powerFraction, 0.85)
    assert compareFloat(tmax_L_BP2.wastedTime, 6.228238736350162e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_E, 3.5569183415387e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_Sc, 1.6205633238077958e-08) #[s]
    assert compareFloat(tmax_L_BP2.time_dT, 1.935101965950209e-07) #[s]
    assert compareFloat(tmax_L_BP2.time_PC, 3.493574809903774e-08) #[s]
    assert compareFloat(tmax_L_BP2.time, 1.6205633238077958e-08) #[s]
    assert tmax_L_BP2.which == 'S'
    assert compareFloat(tmax_L_BP2.maxFields.maxEs, 247.8371349039937) #[MV/m]
    assert tmax_L_BP2.maxFields.maxEs_idx == 394
    assert compareFloat(tmax_L_BP2.maxFields.maxHs, 472.57310708976985) #[kA/m]
    assert tmax_L_BP2.maxFields.maxHs_idx == 122
    assert compareFloat(tmax_L_BP2.maxFields.maxSc, 5.463473794348739) #[W/um^2]
    assert tmax_L_BP2.maxFields.maxSc_idx == 177
    assert compareFloat(tmax_L_BP2.maxFields.maxPC, 2.925198926660397) #[MW/mm]
    assert tmax_L_BP2.maxFields.maxPC_idx == 0
    
    # Max beam time (P(G_UL = 100 MV/m))
    tmax_PUL100 = acs2_DB12v2.getMaxAllowableBeamTime_detailed(acs2_DB12v2.getPowerUnloaded(100e6*acs2_DB12v2.getL()), 0.0)
    #printMaxAllowableBeamTime_detailed(tmax_PUL100, 'tmax_PUL100')
    assert compareFloat(tmax_PUL100.power, 41579148.652665384) #[W]
    assert compareFloat(tmax_PUL100.beamCurrent_pulseShape, 0.0) #[A]
    assert compareFloat(tmax_PUL100.beamCurrent_loading,    0.0)    #[A]
    assert compareFloat(tmax_PUL100.powerFraction, 0.85)
    assert compareFloat(tmax_PUL100.wastedTime, 6.228238736350161e-08) #[s]
    assert compareFloat(tmax_PUL100.time_E, 2.0188466991482163e-07) #[s]
    assert compareFloat(tmax_PUL100.time_Sc, 1.4960945319541384e-07) #[s]
    assert compareFloat(tmax_PUL100.time_dT, 4.3746143969585306e-07) #[s]
    assert compareFloat(tmax_PUL100.time_PC, 2.00174602900422e-07) #[s]
    assert compareFloat(tmax_PUL100.time, 1.4960945319541384e-07) #[s]
    assert tmax_PUL100.which == 'S'
    assert compareFloat(tmax_PUL100.maxFields.maxEs, 210.02995389773972) #[MV/m]
    assert tmax_PUL100.maxFields.maxEs_idx == 394
    assert compareFloat(tmax_PUL100.maxFields.maxHs, 400.48279259613315) #[kA/m]
    assert tmax_PUL100.maxFields.maxHs_idx == 122
    assert compareFloat(tmax_PUL100.maxFields.maxSc, 3.9237251548225753) #[W/um^2]
    assert tmax_PUL100.maxFields.maxSc_idx == 177
    assert compareFloat(tmax_PUL100.maxFields.maxPC, 2.100801988520487) #[MW/mm]
    assert tmax_PUL100.maxFields.maxPC_idx == 0

    assert compareFloat(1.60217646e-19*3.72e9*312 * acs2_DB12v2.getVoltageLoaded(P0, I_beam), 3.71832446493312) # Energy to beam [J]
    assert compareFloat(P0 * (acs2_DB12v2.getTfill()+ acs2_DB12v2.getTrise() + tBeam), 13.469041094973546) # Energy to structure [J]
    assert compareFloat(acs2_DB12v2.getTotalEfficiency(P0,I_beam,tBeam)*100, 27.606452743846376) # RF -> beam efficiency [%]

    # Min bunch spacing [cycles] at 6.6 V/pC/mm/m
    assert acs2_DB12v2.getMinBunchSpacing(6.6) == 6

    #Trigger a failure and a printout
    #assert False

@pytest.mark.structureLibrary
def test_accelStructure_getterFunctions():
    "Testing the getter functions with AccelStructure_CLICG, 24 cells, R05 variety, no database"

    dt_bunch = 0.5e-9 #[ns]
    I_beam=CLICopti.Constants.electron_charge*6.8e9/dt_bunch #[A]
    t_beam = 354*dt_bunch #[ns]

    G      = 100e6

    Npoints = 500

    fDir = getAndMakeTestOutputFolderPath('test_accelStructure_getterFunctions')

    #Creating AccelStructure_CLICG; R05 variety, not database
    acsG_R05 = CLICopti.RFStructure.AccelStructure_CLICG(24, True)
    acsG_R05.calc_g_integrals(Npoints)

    L  = acsG_R05.getL()
    P0 = acsG_R05.getPowerUnloaded(G*L)
    P0_L = acsG_R05.getPowerLoaded(G*L,I_beam)

    #Field profiles
    Z = acsG_R05.getZ_all()
    Ez_UL = acsG_R05.getEz_unloaded_all(P0)
    Ez_L = acsG_R05.getEz_loaded_all(P0_L,I_beam)

    deltaT_all = acsG_R05.getDeltaT_all(P0_L, t_beam, I_beam)

    #Dump to file and compare
    with open(os.path.join(fDir,'testfile_fieldProfile.dat'),'w') as f:
        f.write("# Z Ez_UL, Ez_L deltaT_all\n")
        for i in range(Npoints):
            f.write(f"{Z[i]} {Ez_UL[i]} {Ez_L[i]} {deltaT_all[i]}\n")
    assert compareFiles(os.path.join(fDir,'testfile_fieldProfile.dat'), os.path.join(fDir,'testfile_fieldProfile_ref.dat'))

    #Cell parameters
    zIdx = np.arange(0, Npoints)
    with pytest.raises(KeyError):
        a_n   = acsG_R05.getInterpolated_zidx(zIdx, "a_n")
    vg   = acsG_R05.getInterpolated_zidx(zIdx, "vg")
    with pytest.raises(TypeError):
        vg_   = acsG_R05.getInterpolated_zidx(zIdx.astype(float), "vg")
    #Also test accessing with single number
    vg_i = acsG_R05.getInterpolated_zidx(Npoints//2, "vg")
    assert compareFloat(vg_i, 1.199178517355352)
    #Float!
    with pytest.raises(TypeError):
        vg_i_ = acsG_R05.getInterpolated_zidx(Npoints/2, "vg")
    #Out of range
    with pytest.raises(ValueError):
        vg_i_ = acsG_R05.getInterpolated_zidx(Npoints, "vg")
    with pytest.raises(ValueError):
        vg_i_ = acsG_R05.getInterpolated_zidx(-1, "vg")
    with pytest.raises(ValueError):
        vg_i = acsG_R05.getInterpolated_zidx(zIdx-1, "vg")

    vg_0 = acsG_R05.getInterpolatedZero("vg")
    assert compareFloat(vg_0, 1.6500000000000001)
    with pytest.raises(KeyError):
        vg_0_ = acsG_R05.getInterpolatedZero("a_n")

    #Dump to file and compare
    with open(os.path.join(fDir,'testfile_cellProfileIdxd.dat'),'w') as f:
        f.write("# zIdx vg \n")
        for i in range(Npoints):
            f.write(f"{zIdx[i]} {vg[i]}\n")
    assert compareFiles(os.path.join(fDir,'testfile_cellProfileIdxd.dat'), os.path.join(fDir,'testfile_cellProfileIdxd_ref.dat'))

    #Pulse shape
    NT = 200
    t = np.linspace(0,2*t_beam,NT)

    P_t1 = acsG_R05.getP_t(t_beam/2,P0_L, t_beam, I_beam)
    assert compareFloat(P_t1, 73146673.00942664)
    P_t  = acsG_R05.getP_t(t,P0_L, t_beam, I_beam)

    #Dump to file and compare
    with open(os.path.join(fDir,'testfile_pulseShape.dat'),'w') as f:
        f.write("# t P_t \n")
        for i in range(NT):
            f.write(f"{t[i]} {P_t[i]}\n")
    assert compareFiles(os.path.join(fDir,'testfile_pulseShape.dat'), os.path.join(fDir,'testfile_pulseShape_ref.dat'))


    #Trigger a failure and a printout
    #assert False
