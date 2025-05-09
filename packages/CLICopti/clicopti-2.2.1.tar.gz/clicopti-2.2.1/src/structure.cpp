/*
 *  This file is part of CLICopti.
 *
 *  Authors: Kyrre Sjobak, Daniel Schulte, Alexej Grudiev, Andrea Latina, Jim Ögren
 *
 *  We have invested a lot of time and effort in creating the CLICopti library,
 *  please cite it when using it; see the CITATION file for more information.
 *
 *  CLICopti is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  CLICopti is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with CLICopti.  If not, see <https://www.gnu.org/licenses/>.
 */

#include "structure.h"
#include "cellParams.h"

#include <cstdlib>
#include <cstddef>
#include <cmath>
#include <cfloat>
#include <fstream>
#include <sstream>
#include <limits>

using namespace std;


/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Article references mentioned in this code: See structure.h  *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/** ** Helper functions for return structs ** **/
std::ostream& operator<< (std::ostream &out, const return_AccelStructure_getMaxFields& maxFields) {
  out << "maxEs=" << maxFields.maxEs << "[MV/m]@idx="   << maxFields.maxEs_idx << ", "
      << "maxHs=" << maxFields.maxHs << "[kA/m]@idx="   << maxFields.maxHs_idx << ", "
      << "maxSc=" << maxFields.maxSc << "[W/um^2]@idx=" << maxFields.maxSc_idx << ", "
      << "maxPC=" << maxFields.maxPC << "[MW/mm]@idx="  << maxFields.maxPC_idx;
  return out;
}
std::ostream& operator<< (std::ostream &out, const return_AccelStructure_getMaxDeltaT& maxDeltaT) {
  out << "maxDeltaT=" << maxDeltaT.maxDeltaT << "[K]@idx="   << maxDeltaT.maxDeltaT_idx;
  return out;
}

std::ostream& operator<< (std::ostream &out, const return_AccelStructure_getMaxAllowableBeamTime_detailed& timeData) {
  out << "power=" << timeData.power/1e6 << "[MW], "
      << "beamCurrent_pulseShape=" << timeData.beamCurrent_pulseShape << "[A], "
      << "beamCurrent_loading=" << timeData.beamCurrent_loading << "[A], "
      << "powerFraction=" << timeData.powerFraction << ", "
      << "wastedTime=" << timeData.wastedTime*1e9 << "[ns], "
      << "maxFields={" << timeData.maxFields << "}, "
      << "time_E=" << timeData.time_E*1e9 << "[ns], "
      << "time_Sc=" << timeData.time_Sc*1e9 << "[ns], "
      << "time_dT=" << timeData.time_dT*1e9 << "[ns], "
      << "time_PC=" << timeData.time_PC*1e9 << "[ns], "
      << "time=" << timeData.time*1e9 << "[ns], "
      << "which='" << timeData.which << "'";
  return out;
}

/** ** AccelStructure implementation ** **/

AccelStructure::~AccelStructure() {
  prune_integrals();
  pruneCells();
  pruneWakePrecalc();
}
void AccelStructure::initializeBase() {
  createCells();

  double deltaH = fabs(cellFirst->h - cellMid->h) +
    fabs(cellFirst->h - cellLast->h) +
    fabs(cellMid->h - cellLast->h);
  const double deltaH_tol = 1e-6;
  if (deltaH > deltaH_tol) {
    std::stringstream ss;
    ss << "Error in AccelStructure::initializeBase(): Total sum of differences in h = "
       << deltaH << " m > tolerance " << deltaH_tol << " m. Cells are:" << endl
       << *cellFirst << endl
       << *cellMid << endl
       << *cellLast << endl
       << "This is most likely a bug in the program or the database.";
    throw AccelStructureInternalError(ss.str());
  }
  double h_ave = (cellFirst->h + cellMid->h + cellLast->h)/3.0;
  cellFirst->h = h_ave;
  cellMid->h   = h_ave;
  cellLast->h  = h_ave;

  L = N*cellFirst->h; //[m]

  omega = 2*M_PI*(cellFirst->f0 + cellMid->f0 + cellLast->f0)*1e9/3.0; // [Hz]

  this->psi = cellFirst->psi;
  double deltaPsi = fabs(cellFirst->psi - cellMid->psi) +
    fabs(cellFirst->psi - cellLast->psi) +
    fabs(cellMid->psi - cellLast->psi);
  if (deltaPsi > 1e-10) {
    std::stringstream ss;
    ss << "Error in AccelStructure::initializeBase():" << endl
       << "Total sum of differences in psi greater than tolerance 1e-10." << endl
       << "Phase advances are:" << endl
       << "cellFirst: " << cellFirst->psi << " [deg]" << endl
       << "cellMid  : " << cellMid->psi   << " [deg]" << endl
       << "cellLast : " << cellLast->psi  << " [deg]" << endl
       << "This is most likely a bug.";
    throw AccelStructureInternalError(ss.str());
  }

};

const bool AccelStructure::doPrecalculate = true;

void AccelStructure::populateCellsInterpolated() {
  if (cellsInterpolated != NULL) {
    throw AccelStructureInternalError("CellsInterpolated is not NULL?");
  }
  if (cell0 != NULL) {
    throw AccelStructureInternalError("cell0 is not NULL?");
  }
  if (z == NULL) {
    throw AccelStructureInternalError("z is NULL?");
  }

  //Note: DON't interpolate things which aren't used (at the moment) - the speed gain could be lost.
  //  The downside of this is that it makes getInterpolated_zidx and getInterpolatedZero UNSAFE to call
  //  for the not-set fields.
  //  There is no assertion to catch this, as it would also make things slower. Use valgrind!

  cell0 = new CellParams();
  //cell0->h    = getInterpolated(0.0,offsetof(struct CellParams, h));
  //cell0->a    = getInterpolated(0.0,offsetof(struct CellParams, a));
  //cell0->d_n  = getInterpolated(0.0,offsetof(struct CellParams, d_n));
  //cell0->a_n  = getInterpolated(0.0,offsetof(struct CellParams, a_n));
  //cell0->f0   = getInterpolated(0.0,offsetof(struct CellParams, f0));
  //cell0->psi  = getInterpolated(0.0,offsetof(struct CellParams, psi));
  //cell0->Q    = getInterpolated(0.0,offsetof(struct CellParams, Q));
  cell0->vg   = getInterpolated(0.0,offsetof(struct CellParams, vg));
  cell0->rQ   = getInterpolated(0.0,offsetof(struct CellParams, rQ));
  //cell0->Es   = getInterpolated(0.0,offsetof(struct CellParams, Es));
  //cell0->Hs   = getInterpolated(0.0,offsetof(struct CellParams, Hs));
  //cell0->Sc   = getInterpolated(0.0,offsetof(struct CellParams, Sc));
  //cell0->f1mn = getInterpolated(0.0,offsetof(struct CellParams, f1mn));
  //cell0->Q1mn = getInterpolated(0.0,offsetof(struct CellParams, Q1mn));
  //cell0->A1mn = getInterpolated(0.0,offsetof(struct CellParams, A1mn));

  cellsInterpolated = new CellParams[z_numPoints];
  for (size_t i = 0; i < z_numPoints; i++) {
    //cellsInterpolated[i].h    = getInterpolated(z[i],offsetof(struct CellParams, h));
    cellsInterpolated[i].a    = getInterpolated(z[i],offsetof(struct CellParams, a));
    //cellsInterpolated[i].d_n  = getInterpolated(z[i],offsetof(struct CellParams, d_n));
    //cellsInterpolated[i].a_n  = getInterpolated(z[i],offsetof(struct CellParams, a_n));
    //cellsInterpolated[i].f0   = getInterpolated(z[i],offsetof(struct CellParams, f0));
    //cellsInterpolated[i].psi  = getInterpolated(z[i],offsetof(struct CellParams, psi));
    cellsInterpolated[i].Q    = getInterpolated(z[i],offsetof(struct CellParams, Q));
    cellsInterpolated[i].vg   = getInterpolated(z[i],offsetof(struct CellParams, vg));
    cellsInterpolated[i].rQ   = getInterpolated(z[i],offsetof(struct CellParams, rQ));
    cellsInterpolated[i].Es   = getInterpolated(z[i],offsetof(struct CellParams, Es));
    cellsInterpolated[i].Hs   = getInterpolated(z[i],offsetof(struct CellParams, Hs));
    cellsInterpolated[i].Sc   = getInterpolated(z[i],offsetof(struct CellParams, Sc));
    //cellsInterpolated[i].f1mn = getInterpolated(z[i],offsetof(struct CellParams, f1mn));
    //cellsInterpolated[i].Q1mn = getInterpolated(z[i],offsetof(struct CellParams, Q1mn));
    //cellsInterpolated[i].A1mn = getInterpolated(z[i],offsetof(struct CellParams, A1mn));
  }
}

double AccelStructure::interpolate3(double first, double mid, double last,
                                    double z, bool midEnds) const{
  if (cellFirst == NULL) {
    throw AccelStructureUninitialized("First cell has not been created!");
  }

  if (z < 0 || z > L+cellLast->h*0.01) {
    std::stringstream ss;
    ss << "z=" << z << " out of range [0, " << L+cellLast->h*0.01 << "]";
    throw std::domain_error(ss.str());
  }

  double z1 = 0.0;
  double z2 = L/2.0;
  double z3 = L;
  if (midEnds) {
    z1 = cellFirst->h/2.0;
    z3 = L-cellFirst->h/2.0;
  }

  //Lagrange polynomial
  return first*(z-z2)*(z-z3)/( (z1-z2)*(z1-z3) ) +
           mid*(z-z1)*(z-z3)/( (z2-z1)*(z2-z3) ) +
          last*(z-z1)*(z-z2)/( (z3-z1)*(z3-z2) );

}

void AccelStructure::pruneCells() {
  if (cellFirst == NULL) return;
  delete cellFirst; cellFirst = NULL;
  delete cellMid;   cellMid   = NULL;
  delete cellLast;  cellLast  = NULL;
}
void AccelStructure::prune_integrals() {
  if (has_integrals) {
    if (g == NULL) {
      throw AccelStructureInternalError("g is already NULL?");
    }
    if (g_load == NULL) {
      throw AccelStructureInternalError("g_load is already NULL?");
    }
    if (z == NULL) {
      throw AccelStructureInternalError("z is already NULL?");
    }

    delete[] g;      g      = NULL;
    delete[] g_load; g_load = NULL;
    delete[] z;      z      = NULL;

    if (doPrecalculate) {
      if (cellsInterpolated == NULL) {
        throw AccelStructureInternalError("cellsInterpolated is already NULL?");
      }
      if (cell0 == NULL) {
        throw AccelStructureInternalError("cell0 is already NULL?");
      }
      delete[] cellsInterpolated; cellsInterpolated = NULL;
      delete cell0;               cell0             = NULL;
    }
  }
  z_numPoints = 0;
  has_integrals = false;
}

void AccelStructure::calc_g_integrals(size_t numPoints) {
  if (cellMid == NULL) {
    throw AccelStructureUninitialized("Middle cell is missing!");
  }
  if (has_integrals) prune_integrals();

  //cout << "Calculating g_integral with numpoints = " << numPoints << endl;
  this->z_numPoints = numPoints;

  //Create arrays
  z = new double[numPoints];
  h = L/(numPoints-1.0);
  for (size_t i = 0; i < numPoints; i++) z[i] = h*i;
  //g = new double[numPoints];

  //Do this after populating z
  if (doPrecalculate and cellsInterpolated==NULL) {
    populateCellsInterpolated();
  }


  //Integral inside the exp()
  // Function under integral
  double* Iap = new double[numPoints];
  for (size_t i = 0; i < numPoints; i++) {
    Iap[i] = omega/(getInterpolated_zidx(i, offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 *
                    getInterpolated_zidx(i, offsetof(struct CellParams, Q)));
  }
  g = z_integral_helper(Iap);
  delete[] Iap; Iap = NULL;
  //Multiply with -0.5 and take the exp, multiply result with prefactors from Eq. 2.13.
  // Also compute the voltage.
  double sqrt_vg0_rho0 = sqrt( getInterpolatedZero(offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 /
                               getInterpolatedZero(offsetof(struct CellParams, rQ)) );
  g_int = 0.0;
  for (size_t i = 0; i < numPoints; i++) {
    g[i] = sqrt_vg0_rho0 * sqrt( getInterpolated_zidx(i,offsetof(struct CellParams, rQ)) /
                                 (getInterpolated_zidx(i,offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01) )
                         * exp(-0.5*g[i]);

    if (numPoints%2 != 0)
      g_int   += ( (i == 0 || i == (numPoints-1) ) ? 1.0 : (i%2==0 ? 2.0 : 4.0) )*g[i]*h/3.0; //Simpson
    else { //Simpson + trapz for last point
      if (i != numPoints-1)
        g_int += ( (i == 0 || i == (numPoints-2) ) ? 1.0 : (i%2==0 ? 2.0 : 4.0) )*g[i]*h/3.0; //Simpson
      else
        g_int += (g[i-1]+g[i])*h/2.0; //Trapz
    }
  }
  //cout << "g_int = " << g_int << endl; //Debug against old python code's "self.gzInt"

  //Loading integral from eq. 2.14 in [1], solve as for g(z)
  double* Ibp = new double[numPoints]; //Everything under the integral but the beam current
  for (size_t i = 0; i < numPoints; i++) {
    Ibp[i] = omega * getInterpolated_zidx(i,offsetof(struct CellParams, rQ)) /
         (g[i] * 2.0*getInterpolated_zidx(i,offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01);
  }
  g_load = z_integral_helper(Ibp);
  delete[] Ibp; Ibp = NULL;
  //Multiply the loading integral with g(z) to get g_load(z),
  // and integrate g_load(z) the to get the shunt impedance
  g_load_int = 0.0;
  for (size_t i = 0; i < numPoints; i++) {
    g_load[i] *= g[i];

    if (numPoints%2 != 0)
      g_load_int   += ( (i == 0 || i == (numPoints-1) ) ? 1.0 : (i%2==0 ? 2.0 : 4.0) )*g_load[i]*h/3.0; //Simpson
    else { //Simpson + trapz for last point
      if (i != numPoints-1)
        g_load_int += ( (i == 0 || i == (numPoints-2) ) ? 1.0 : (i%2==0 ? 2.0 : 4.0) )*g_load[i]*h/3.0; //Simpson
      else
        g_load_int += (g_load[i-1]+g_load[i])*h/2.0; //Trapz
    }
  }

  //Filling time
  t_fill = 0.0;
  for (size_t i = 0; i < numPoints; i++) {
    if (numPoints%2 != 0)
      t_fill   += ( (i == 0 || i == (numPoints-1) ) ? 1.0 : (i%2==0 ? 2.0 : 4.0) ) /
        getInterpolated_zidx(i,offsetof(struct CellParams, vg)) * h/3.0; //Simpson
    else { //Simpson + trapz for last point
      if (i != numPoints-1)
        t_fill += ( (i == 0 || i == (numPoints-2) ) ? 1.0 : (i%2==0 ? 2.0 : 4.0) ) /
          getInterpolated_zidx(i,offsetof(struct CellParams, vg)) * h/3.0; //Simpson
      else
        t_fill += (  1.0/getInterpolated_zidx(i-1, offsetof(struct CellParams, vg))
                   + 1.0/getInterpolated_zidx(i  , offsetof(struct CellParams, vg)) ) * h/2.0;
    }
  }
  t_fill /= 0.01*Constants::speed_of_light;

  //Rise time
  double vg_min = 100;
  if(cellLast->vg  < vg_min) vg_min = cellLast->vg;
  if(cellMid->vg   < vg_min) vg_min = cellMid->vg;
  if(cellFirst->vg < vg_min) vg_min = cellFirst->vg;
  t_rise = 21.0e-9 * 0.83/vg_min * psi / 120.0; //Compare to CLIC_G

  has_integrals = true;
  has_integral_results = true;
}

/** Integrate intVar from 0 to step*numPoints for "numPoints" measurements spaced "step"
 *  Return a new double of length numPoints.
 */
double* AccelStructure::integral_helper(double* intVar, double step, size_t numPoints) const {
  double* ret = new double[numPoints];
  // Solve using simpson with trapz for the last point.
  ret[0] = 0.0;
  for (size_t i = 2; i < numPoints; i+=2) {
    ret[i] = ret[i-2] + (step/3.0)*(intVar[i-2] + 4*intVar[i-1] + intVar[i]);
  }
  for (size_t i = 1; i < z_numPoints; i+=2) {
    ret[i] = ret[i-1] + (step/2.0)*(intVar[i-1]+intVar[i]);
  }
  //pure trapz, also works
  //for (size_t i = 1; i < numPoints; i++) ret[i] = ret[i-1] + (step/2.0)*(intVar[i-1]+intVar[i]);

  return ret;
}

double AccelStructure::getPowerUnloaded(double voltageUnloaded) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  if (voltageUnloaded <= 0.0) {
    throw std::domain_error("Expect voltageUnloaded > 0.0");
  }

  return getInterpolatedZero(offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 /
    (omega*getInterpolatedZero(offsetof(struct CellParams, rQ))) * pow(voltageUnloaded/g_int, 2);
}
double AccelStructure::getVoltageUnloaded(double power) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  if (power <= 0.0) {
    throw std::domain_error("Expect power > 0.0");
  }

  return g_int * sqrt(omega * getInterpolatedZero(offsetof(struct CellParams, rQ)) * power /
                      (getInterpolatedZero(offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01));
}
double AccelStructure::getVoltageLoaded(double power, double beamCurrent) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  if (beamCurrent <= 0.0) {
    throw std::domain_error("Expect beamCurrent > 0.0");
  }

  return g_int * sqrt(omega * getInterpolatedZero(offsetof(struct CellParams, rQ)) * power /
                      (getInterpolatedZero(offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01))
               - beamCurrent*g_load_int;
}
double AccelStructure::getPowerLoaded(double voltageLoaded, double beamCurrent) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  if (voltageLoaded < 0.0) {
    throw std::domain_error("Expect voltageLoaded >= 0.0");
  }

  return getInterpolatedZero(offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 /
    (omega*getInterpolatedZero(offsetof(struct CellParams, rQ))) *
    pow((voltageLoaded + beamCurrent*g_load_int)/g_int, 2);
}
double AccelStructure::getLoadingVoltage(double beamCurrent) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  return beamCurrent*g_load_int;
}
double AccelStructure::getTfill() const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  return t_fill;
}
double AccelStructure::getTrise() const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  return t_rise;
}

return_AccelStructure_getMaxFields AccelStructure::getMaxFields(double power, double beamCurrent) const {
  if (not has_integrals) {
    throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
  }

  return_AccelStructure_getMaxFields ret = {}; //Initialize to 0
  double Ez, Es, Hs, Sc, PC;

  for (size_t i = 0; i < z_numPoints; i++) {
    if (beamCurrent == 0.0)
      Ez = getEz_unloaded(i,power);
    else
      Ez = getEz_loaded(i,power,beamCurrent);

    Es = getInterpolated_zidx(i, offsetof(struct CellParams, Es))*Ez/1e6;
    if (fabs(Es) > ret.maxEs) {
      ret.maxEs = fabs(Es);
      ret.maxEs_idx = i;
    }

    Hs = getInterpolated_zidx(i, offsetof(struct CellParams, Hs))*Ez/1e6;
    if (fabs(Hs) > ret.maxHs) {
      ret.maxHs = fabs(Hs);
      ret.maxHs_idx = i;
    }

    Sc = getInterpolated_zidx(i, offsetof(struct CellParams, Sc))*Ez*Ez/1e15;
    if (fabs(Sc) > ret.maxSc) {
      ret.maxSc = fabs(Sc);
      ret.maxSc_idx = i;
    }

    PC = (Ez*Ez) * getInterpolated_zidx(i, offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 /
      ( omega * getInterpolated_zidx(i, offsetof(struct CellParams, rQ)) ) / 1e6; //Power [MW]
    PC /= 2.0 * M_PI * getInterpolated_zidx(i, offsetof(struct CellParams, a))*1e3 ; //P over C [MW/mm]
    if (fabs(PC) > ret.maxPC) {
      ret.maxPC = fabs(PC);
      ret.maxPC_idx = i;
    }

  }

  return ret;
}

double AccelStructure::getMaxAllowablePower(double beamCurrent, double max_Es, double max_Sc) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }

  return_AccelStructure_getMaxFields maxFields; //temp variable

  //Find the maximum allowable power using the bisection method
  double P_low = getPowerLoaded(0.0,beamCurrent); //Lowest allowable power: Zero voltage seen by beam
  maxFields = getMaxFields(P_low, beamCurrent);   //Find the maximum fields at P_low
  if (maxFields.maxEs > max_Es || maxFields.maxSc > max_Sc) {
#ifdef CHATTY_PROGRAM
    cout << "Bad structure: Can't have V_loaded > 0 while keeping within breakdown constraints!" << endl;
#endif
    return 0.0;
  }

  //Define initial bracket by doubling P_high until one of the boundaries are broken
  double P_high = 0.0;
  size_t i = 0; size_t i_maxIter = 1000;
  for (i = 0; i < i_maxIter; i++) {
    P_high = 2*P_low;
    maxFields = getMaxFields(P_high, beamCurrent);
    if      (maxFields.maxEs > max_Es) break; //Reached max Es
    else if (maxFields.maxSc > max_Sc) break; //Reached max Sc
    else P_low = P_high; //Moving to next bracket
  }
  if (i == i_maxIter) {
    stringstream ss;
    ss << "ERROR: In bracketing, reached i_maxIter = " << i_maxIter;
    throw AccelStructureInternalError(ss.str());
  }

  //Bisection method
  double P_guess = 0.0;
  double maxDeltaP = 1e6; //Wanted presission [W]
  for (i = 0; i < i_maxIter; i++) {
    if ( (P_high-P_low) < maxDeltaP ) break;

    P_guess = (P_high+P_low)/2.0;
    maxFields = getMaxFields(P_high, beamCurrent);
    if (maxFields.maxEs > max_Es || maxFields.maxSc > max_Sc) P_high = P_guess; //Too high
    else                                                      P_low  = P_guess; //To low
  }
  if (i == i_maxIter) {
    stringstream ss;
    ss << "In bisection, reached i_maxIter = " << i_maxIter;
    throw AccelStructureInternalError(ss.str());
  }

  return P_low; //Return low end of the interval
}

double AccelStructure::getMaxAllowablePower_beamTimeFixed(double beamCurrent, double beamTime) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }

  //Lowest allowable power: Zero voltage seen by beam
  double V_low = 0.0;
  double P_low = getPowerLoaded(V_low,beamCurrent);
  //Does this respect the beamtime constraints?
  double t_long = getMaxAllowableBeamTime(P_low,beamCurrent);
  if (t_long <= beamTime) {
#ifdef CHATTY_PROGRAM
    cout << "Too long pulse: Can't have V_loaded > 0 for the required beamTime." << endl;
#endif
    return 0.0;
  }
  else if (t_long == beamTime) {
    //Corner case, skip the bracketing and bisection
    return P_low;
  }

  //Define initial bracket by doubling P_high until one of the boundaries are broken
  double P_high  = 0.0;
  double t_short = 0.0;
  size_t i = 0; size_t i_maxIter = 1000;
  for (i = 0; i < i_maxIter; i++) {
    //V_high = 2*V_low;
    P_high = 2*P_low;
    t_short = getMaxAllowableBeamTime(P_high,beamCurrent);

    if (t_short < beamTime) {
      break; // max power for beam time between t_short(P_high) and t_long(P_low)
             // Continue to bisection
    }
    //Moving to next bracket
    P_low = P_high;
    t_long = t_short;
  }
  if (i == i_maxIter) {
    stringstream ss;
    ss << "ERROR: In bracketing, reached i_maxIter = " << i_maxIter;
    throw AccelStructureInternalError(ss.str());
  }

  //Bisection method to refine the power
  double P_guess = 0.0;
  double t_guess = 0.0;
  double maxDeltaTime = 1e-9; //Wanted presission [s]
  for (i = 0; i < i_maxIter; i++) {
    if ( (t_long-t_short) < maxDeltaTime) break; // Close enough.

    P_guess = (P_high+P_low)/2.0;
    t_guess = getMaxAllowableBeamTime(P_guess,beamCurrent);

    if (t_guess < beamTime) {
      // Too much power in P_guess
      P_high  = P_guess;
      t_short = t_guess;
    }
    else {
      // Too little power in P_guess
      P_low  = P_guess;
      t_long = t_guess;
    }
  }
  if (i == i_maxIter) {
    stringstream ss;
    ss << "In bisection, reached i_maxIter = " << i_maxIter;
    throw AccelStructureInternalError(ss.str());
  }

  return P_low; //Return low end of the interval,
                // where the corresponding t_long > t_beam
                // and (t_long-t_beam) < maxDeltaTime
}

const double AccelStructure::constBDR0 = 10e-6;  //[Breakdowns per pulse per meter] Reference breakdown rate for scaling
const double AccelStructure::constTau0 = 200e-9; //[s] Reference pulse length for scaling

double AccelStructure::getMaxAllowableBeamTime_E (double power, double beamCurrent)  const {
  double maxEs = getMaxFields(power,beamCurrent).maxEs; //[MV/m]
  double wastedTime = getExtraTimePowerAboveFraction(power,beamCurrent); //[s]
  return getMaxAllowableBeamTime_E_hasPeak(maxEs, wastedTime);
}
double AccelStructure::getMaxAllowableBeamTime_E_hasPeak (double maxEs, double wastedTime)  const {
  // cout << maxConstE << " " << maxEs << " " << pow(maxEs,6) << " " << maxConstE/pow(maxEs,6) << " " << wastedTime << endl;
  return maxConstE/pow(maxEs,6)-wastedTime;
}
const double AccelStructure::maxConstE=pow(220.0,6.0)*constTau0; //[(MV/m)^6 * s]

double AccelStructure::getMaxAllowableBeamTime_Sc(double power, double beamCurrent) const {
  double maxSc = getMaxFields(power,beamCurrent).maxSc; //[W/um^2 = MW/mm^2]
  double wastedTime = getExtraTimePowerAboveFraction(power,beamCurrent); //[s]
  return getMaxAllowableBeamTime_Sc_hasPeak(maxSc, wastedTime);
}
double AccelStructure::getMaxAllowableBeamTime_Sc_hasPeak (double maxSc, double wastedTime)  const {
  // cout << maxConstSc << " " << maxSc << " " << pow(maxSc,3) << " " << maxConstSc/pow(maxSc,3) << " " << wastedTime << endl;
  return maxConstSc/pow(maxSc,3)-wastedTime;
}
const double AccelStructure::maxConstSc=pow(4.0,3)*constTau0; //[(MW/mm^2)^3 * s]

double AccelStructure::getMaxAllowableBeamTime_PC(double power, double beamCurrent) const {
  double maxPC      = getMaxFields(power,beamCurrent).maxPC;             //[MW/mm]
  double wastedTime = getExtraTimePowerAboveFraction(power,beamCurrent); //[s]
  return getMaxAllowableBeamTime_PC_hasPeak(maxPC, wastedTime);
}
double AccelStructure::getMaxAllowableBeamTime_PC_hasPeak(double maxPC, double wastedTime) const {
  return maxConstPC/pow(maxPC,3)-wastedTime;
}
const double AccelStructure::maxConstPC = pow(2.3,3)*constTau0; //[(MW/mm)^3 * s]

return_AccelStructure_getMaxAllowableBeamTime_detailed
  AccelStructure::getMaxAllowableBeamTime_detailed(double power, double beamCurrent_pulseShape,
                                                   double beamCurrent_loading, double powerFraction, double BDR) const {

  //Invoke default values?
  if (powerFraction       < 0.0) powerFraction = constPulsePowerFraction;
  if (beamCurrent_loading < 0.0) beamCurrent_loading = beamCurrent_pulseShape;

  return_AccelStructure_getMaxAllowableBeamTime_detailed ret = {}; //Initialize to 0
  ret.power = power;
  ret.beamCurrent_pulseShape = beamCurrent_pulseShape;
  ret.beamCurrent_loading    = beamCurrent_loading;
  ret.powerFraction = powerFraction;

  ret.maxFields  = getMaxFields(power,beamCurrent_loading);
  ret.wastedTime = getExtraTimePowerAboveFraction(power, beamCurrent_pulseShape, powerFraction); //[s]

  bool foundLimit = false;
  ret.time = numeric_limits<double>::max();

  ret.time_E  = getMaxAllowableBeamTime_E_hasPeak (ret.maxFields.maxEs, ret.wastedTime);
  if (uselimit_E) {
    ret.time = ret.time_E;
    ret.which = 'E';
    foundLimit = true;
  }

  ret.time_Sc = getMaxAllowableBeamTime_Sc_hasPeak(ret.maxFields.maxSc, ret.wastedTime);
  if (uselimit_Sc) {
    if (ret.time_Sc < ret.time) {
      ret.time = ret.time_Sc;
      ret.which = 'S';
      foundLimit = true;
    }
  }

  //Note - deltaT has different signature than the others!
  ret.time_dT = getMaxAllowableBeamTime_dT_hasPeak(power, beamCurrent_pulseShape, ret.maxFields.maxHs);
  if (uselimit_dT) {
    if (ret.time_dT < ret.time) {
      ret.time = ret.time_dT;
      ret.which = 'T';
      foundLimit = true;
    }
  }

  ret.time_PC = getMaxAllowableBeamTime_PC_hasPeak(ret.maxFields.maxPC, ret.wastedTime);
  if (uselimit_PC) {
    if (ret.time_PC < ret.time) {
      ret.time = ret.time_PC;
      ret.which = 'P';
      foundLimit = true;
    }
  }

  if (not foundLimit) {
    ret.time = 0.0;
    ret.which = '?';
  }

  if (ret.time < 0.0) ret.time = 0.0;
  if (BDR > 0.0) return scaleBeamtimeBDR(ret,BDR);
  return ret;
}

  return_AccelStructure_getMaxAllowableBeamTime_detailed
    AccelStructure::scaleBeamtimeBDR(return_AccelStructure_getMaxAllowableBeamTime_detailed beamtime, double BDR) const {
      double BDRscaler = pow(BDR/constBDR0, 1.0/5.0);

      if (uselimit_dT) {
        //No scaling of deltaT
        beamtime.time = beamtime.time_dT;
        beamtime.which = 'T';
      }
      else {
        beamtime.time = numeric_limits<double>::max();
      }

      beamtime.time_E = beamtime.time_E*BDRscaler;
      if (uselimit_E) {
        if (beamtime.time_E < beamtime.time) {
          beamtime.time  = beamtime.time_E;
          beamtime.which = 'E';
        }
      }

      beamtime.time_Sc = beamtime.time_Sc*BDRscaler;
      if (uselimit_Sc) {
        if (beamtime.time_Sc < beamtime.time) {
          beamtime.time  = beamtime.time_Sc;
          beamtime.which = 'S';
        }
      }
      
      beamtime.time_PC = beamtime.time_PC*BDRscaler;
      if (uselimit_PC) {
        if (beamtime.time_PC < beamtime.time) {
          beamtime.time  = beamtime.time_PC;
          beamtime.which = 'P';
        }
      }

      if (beamtime.time < 0.0) beamtime.time = 0.0;
      return beamtime;
  }

double AccelStructure::getExtraTimePowerAboveFraction(double peakPower, double beamCurrent, double powerFraction) const {

  double fraction = constPulsePowerFraction;
  if (powerFraction >= 0) {
    fraction = powerFraction;
  }

  double breakoverPower = getBreakoverPower(peakPower, beamCurrent);
  double fractionPower = fraction*peakPower;

  double tWasted = 0.0;

  //Fill
  if (fractionPower > breakoverPower) {
    tWasted += (1.0 - (fractionPower-breakoverPower) / (peakPower-breakoverPower)) * t_fill;
  }
  else {
    tWasted += (1.0 - fractionPower/breakoverPower)*t_rise + t_fill;
  }

  //Decay
  if (fractionPower > (peakPower-breakoverPower)) {
    tWasted +=(peakPower-fractionPower) / breakoverPower * t_rise;
  }
  else {
    tWasted += (peakPower-fractionPower-breakoverPower) / (peakPower-breakoverPower) * t_fill + t_rise;
  }

  if (isnan(tWasted)) {
    //Some edgcases result in division-by-zero
    stringstream ss;
    ss << "In getExtraTimePowerAboveFraction() - tWasted was nan.";
    throw AccelStructureInternalError(ss.str());
  }

  return tWasted;
}
const double AccelStructure::constPulsePowerFraction = 0.85;


double AccelStructure::getDeltaTconst(double peakPower, double t_beam, double beamCurrent) const {
  if (not has_integral_results) {
    throw AccelStructureUninitialized("Integrals have never been calculated.");
  }
  double breakoverPower = getBreakoverPower(peakPower, beamCurrent);

  // Material constants from Table 1.1 in [2], OFC copper
  double dens    = 8.95e3; //[kg/m^3]   material density
  double Ceps    = 385.0;  //[J/(kg K)] specific heat
  double ktherm  = 391;    //[W/(m K)]  thermal conductivity
  double el_cond = 5.8e7;  //[S/m]      electric conductivity

  double R_surf = sqrt(Constants::mu0*omega/(2*el_cond)); //[Ohm] Surface resistance

  //Calulate the z-independent part of deltaT(z),
  // assuming peak temperature to be at the end of t_beam, picewise linear pulse
  double t_beamStart = t_rise+t_fill;
  double t_end = t_rise+t_fill+t_beam;

  double deltaTconst = breakoverPower/t_rise *
    ( -2.0/3.0 * ( -2.0*pow(t_end,3.0/2.0) + 2.0*t_end*sqrt(t_end-t_rise)+t_rise*sqrt(t_end-t_rise) ) );

  deltaTconst += breakoverPower *                  2.0*( sqrt(t_end-t_rise)-sqrt(t_end-t_beamStart))
    - (peakPower-breakoverPower)*(t_rise/t_fill) * 2.0*( sqrt(t_end-t_rise)-sqrt(t_end-t_beamStart))
    + (peakPower-breakoverPower)/t_fill    * (2.0/3.0)*( sqrt(t_end-t_rise)*t_rise +
                                                         2*t_end*(sqrt(t_end-t_rise) -
                                                                  sqrt(t_end-t_beamStart) ) -
                                                         t_beamStart*sqrt(t_end-t_beamStart) );

  deltaTconst += peakPower*2*sqrt(t_end-t_beamStart);

  deltaTconst *= 0.5*R_surf/sqrt(M_PI*dens*Ceps*ktherm)/peakPower;

  return deltaTconst;
}

double AccelStructure::getDeltaT(double peakPower, double t_beam, double beamCurrent, size_t zIdx, bool loaded, double deltaTconst) const {
  //Pulsed surface heating as function of z
  // Expression for deltaT(z,t) worked out from Eq. 3.36 in [2]
  // (See notebook 3 (orange-backed one), date 24/4/2012, and
  //  notebook 4, date 7/3/2013)

  double Ez;
  if (loaded) Ez = getEz_loaded(zIdx,peakPower,beamCurrent);
  else        Ez = getEz_unloaded(zIdx,peakPower);

  if(deltaTconst < 0.0) {
    deltaTconst = getDeltaTconst(peakPower, t_beam, beamCurrent);
  }

  return pow(Ez*getInterpolated_zidx(zIdx,offsetof(struct CellParams, Hs))/1e3,2) * deltaTconst; //Convert mA/V -> A/V
}

return_AccelStructure_getMaxDeltaT
  AccelStructure::getMaxDeltaT(double peakPower, double t_beam, double beamCurrent, bool loaded) const {

  double deltaTconst = getDeltaTconst(peakPower, t_beam, beamCurrent);
  return_AccelStructure_getMaxFields peakFields = getMaxFields(peakPower, loaded ? beamCurrent : 0.0);
  return_AccelStructure_getMaxDeltaT maxDeltaT= {}; //Initialize to 0
  maxDeltaT.maxDeltaT = getMaxDeltaT_hasPeak(peakFields.maxHs, deltaTconst);
  maxDeltaT.maxDeltaT_idx = peakFields.maxHs_idx;
  return maxDeltaT;
}
double AccelStructure::getMaxDeltaT_hasPeak(double maxHs, double deltaTconst) const {
  return pow(maxHs*1e3,2)*deltaTconst; //Convert maxHs from kA/m -> A/m
}


double AccelStructure::getMaxAllowableBeamTime_dT(double peakPower, double beamCurrent, bool useLoadedField) const {
  //Get the peak fields
  double maxHs = getMaxFields(peakPower, useLoadedField ? beamCurrent : 0.0).maxHs;
  return getMaxAllowableBeamTime_dT_hasPeak(peakPower, beamCurrent, maxHs);
}
double AccelStructure::getMaxAllowableBeamTime_dT_hasPeak(double peakPower, double beamCurrent, double maxHs) const {

  //Is this allowed?
  double t_low = 0.0;
  double deltaTconst = getDeltaTconst(peakPower, t_low, beamCurrent);
  double maxDeltaT = getMaxDeltaT_hasPeak(maxHs, deltaTconst);
  if (maxDeltaT >= max_deltaT) {
#ifdef CHATTY_PROGRAM
    cout << "Bad input or structure: Can't have t_beam > 0 while keeping deltaT < constraint!" << endl;
#endif
    return 0.0;
  }

  //Define initial bracket
  double t_high = 2*M_PI/omega; //one period [s]
  size_t i = 0; size_t i_maxIter = 1000;
  for (i = 0; i < i_maxIter; i++) {
    //cout << "Bracketing: trying [" << t_low*1e9 << "," << t_high*1e9 << "] ns" << endl;

    deltaTconst = getDeltaTconst(peakPower, t_high, beamCurrent);
    maxDeltaT   = getMaxDeltaT_hasPeak(maxHs, deltaTconst);

    if (maxDeltaT > max_deltaT) break; //reached max_deltaT
    //Else: trying a higher interval
    t_low = t_high;
    t_high *= 2;
  }
  if(i == i_maxIter) {
    stringstream ss;
    ss << "In getMaxAllowableBeamTime() bracketing, reached i_maxIter = " << i_maxIter;
    throw AccelStructureInternalError(ss.str());
  }

  //Bisection method
  double t_guess = 0.0;
  double max_delta_t_beam = 2*M_PI/omega; //Precission in t_beam (one period)
  for (i = 0; i < i_maxIter; i++) {
    //cout << "Bisection: trying [" << t_low*1e9 << "," << t_high*1e9 << "] ns" << endl;
    if ( (t_high-t_low) < max_delta_t_beam) break;

    t_guess = (t_high+t_low)/2.0;

    deltaTconst = getDeltaTconst(peakPower, t_guess, beamCurrent);
    maxDeltaT   = getMaxDeltaT_hasPeak(maxHs, deltaTconst);

    //cout << "At t_guess = " << t_guess*1e9 << " ns, got deltaT = " << maxDeltaT.maxDeltaT << " K" << endl;

    if (maxDeltaT > max_deltaT) t_high = t_guess; //Too high
    else                        t_low  = t_guess; //Too low
  }
  if(i == i_maxIter) {
    stringstream ss;
    ss << "In getMaxAllowableBeamTime() bisection, reached i_maxIter = " << i_maxIter;
    throw AccelStructureInternalError(ss.str());
  }

  return t_low; //Return low end of the interval
}
const double AccelStructure::max_deltaT = 50; //[K]

void AccelStructure::writeProfileFile(const char* const fname, double power, double beamCurrent) {
  if (not has_integrals) {
    throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
  }
  if (fname == NULL) {
    throw std::invalid_argument("Got fname=NULL, this is no longer accepted.");
  }

  ofstream ofile(fname);
  ofile << "# FieldProfileFile, power=" << power/1e6 << "[MW], beamCurrent=" << beamCurrent << "[A]" << endl;
  writeProfileFile_header(ofile);
  ofile << "# z[m] E_z[MV/m] E_surf[MV/m] H_surf[kA/m] Sc[W/um^2] P[MW] P/c[MW/mm]" << endl;

  double Ez;
  double Es, Hs, Sc;
  double P, PC;

  for (size_t i = 0; i < z_numPoints; i++) {
    if (beamCurrent == 0.0)
      Ez = getEz_unloaded(i,power);
    else
      Ez = getEz_loaded(i,power,beamCurrent);

    Es = getInterpolated_zidx(i, offsetof(struct CellParams, Es))*Ez/1e6;
    Hs = getInterpolated_zidx(i, offsetof(struct CellParams, Hs))*Ez/1e6;
    Sc = getInterpolated_zidx(i, offsetof(struct CellParams, Sc))*Ez*Ez/1e15;

    P = (Ez*Ez) * getInterpolated_zidx(i, offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 /
        ( omega * getInterpolated_zidx(i, offsetof(struct CellParams, rQ)) ) / 1e6;

    PC = P/(2.0 * M_PI * getInterpolated_zidx(i, offsetof(struct CellParams, a))*1e3 );

    ofile << z[i] << " " << Ez/1e6 << " "
          << Es   << " " << Hs     << " " << Sc << " "
          << P    << " " << PC     << endl;
  }

  ofile.close();
}
void AccelStructure::writeParameterProfileFile(const char* const fname) {
  if (cellFirst == NULL) {
    throw AccelStructureUninitialized("First cell has not been created!");
  }
  if (not has_integrals) {
    //Use the already-existing z[i] etc.
    throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
  }
  if (fname == NULL) {
    throw std::invalid_argument("Got fname=NULL, this is not accepted.");
  }

  ofstream ofile(fname);
  ofile << "# ParameterProfileFile " << endl;
  writeProfileFile_header(ofile);
  ofile << "# cellFirst: " << *cellFirst << endl;
  ofile << "# cellMid:   " << *cellMid << endl;
  ofile << "# cellLast:  " << *cellLast << endl;
  ofile << "#" << endl;
  ofile << "# z[m] a[m] Q vg[%c] rQ[Ohm/m] Es Hs[mA/V] Sc[mA/V] f1mn[GHz] Q1mn A1mn[V/pC/mm/m]" << endl;
  for (size_t i = 0; i < z_numPoints; i++) {
    ofile << z[i] << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, a)) << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, Q)) << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, vg)) << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, rQ)) << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, Es)) << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, Hs)) << " ";
    ofile << getInterpolated_zidx(i, offsetof(struct CellParams, Sc)) << " ";
    ofile << getInterpolated(z[i], offsetof(struct CellParams, f1mn)) << " ";
    ofile << getInterpolated(z[i], offsetof(struct CellParams, Q1mn)) << " ";
    ofile << getInterpolated(z[i], offsetof(struct CellParams, A1mn)) << endl;
  }

  ofile.close();

}

void AccelStructure::writeDeltaTprofileFile(const char* const fname,double peakPower,
                                            double t_beam, double beamCurrent, bool loaded) {
  if (fname == NULL) {
    throw std::invalid_argument("Got fname=NULL, this is no longer accepted.");
  }

  ofstream ofile(fname);
  ofile << "# DeltaT profile file, peakPower=" << peakPower/1e6 << "[MW]"
        << ", breakoverPower=" << getBreakoverPower(peakPower,beamCurrent)/1e9 << "[MW]"
        << ", t_rise=" << t_rise*1e9 << "[ns]"
        << ", t_fill=" << t_fill*1e9 << "[ns]"
        << ", t_beam=" << t_beam*1e9 << "[ns]"
        << ", beamCurrent=" << beamCurrent << "[A]" << endl;
  writeProfileFile_header(ofile);
  ofile << "# z[m] deltaT[K]" << endl;

  double deltaTconst = getDeltaTconst(peakPower, t_beam, beamCurrent);

  double Ez;
  double deltaT;
  for (size_t i = 0; i < z_numPoints; i++) {
    if (loaded) Ez = getEz_loaded(i,peakPower,beamCurrent);
    else        Ez = getEz_unloaded(i,peakPower);

    deltaT = pow(Ez*getInterpolated_zidx(i,offsetof(struct CellParams, Hs))/1e3,2)*deltaTconst; //Convert Hs from mA/V -> A/V
    ofile << z[i] << " " << deltaT << endl;
  }

  ofile.close();
}
void AccelStructure::writeTimeDeltaTprofileFile(const char* const fname, double peakPower,
                                                double t_beam_max, double beamCurrent,
                                                bool loaded, size_t numPoints) {

  if (fname == NULL) {
    throw std::invalid_argument("Got fname=NULL, this is no longer accepted.");
  }

  ofstream ofile(fname);
  ofile << "# DeltaT time profile file, peakPower=" << peakPower/1e6 << "[MW]"
        << ", breakoverPower=" << getBreakoverPower(peakPower,beamCurrent)/1e9 << "[MW]"
        << ", t_rise=" << t_rise*1e9 << "[ns]"
        << ", t_fill=" << t_fill*1e9 << "[ns]"
        << ", t_beam_max=" << t_beam_max*1e9 << "[ns]"
        << ", beamCurrent=" << beamCurrent << "[A]" << endl;
  writeProfileFile_header(ofile);
  ofile << "# t[ns] t_beam[ns] deltaT[K]" << endl;

  return_AccelStructure_getMaxFields peakFields = getMaxFields(peakPower, loaded ? beamCurrent : 0.0);

  double h = t_beam_max/(numPoints-1);
  for (size_t i = 0; i < numPoints; i++) {
    double t_beam = i*h;

    double deltaTconst = getDeltaTconst(peakPower, t_beam, beamCurrent);
    double deltaT = getMaxDeltaT_hasPeak(peakFields.maxHs, deltaTconst);

    ofile << (t_beam+t_rise+t_fill)*1e9 << " " << t_beam*1e9 << " " << deltaT << endl;
  }

  ofile.close();
}

void AccelStructure::writeTimePowerProfileFile(const char* const fname, double peakPower,
                                               double t_beam, double beamCurrent,
                                               size_t numPoints) const {

  if (fname == NULL) {
    throw std::invalid_argument("Got fname=NULL, this is not accepted.");
  }

  double breakoverPower = getBreakoverPower(peakPower,beamCurrent);

  ofstream ofile(fname);
  ofile << "# Time profile, peakPower="
        << peakPower/1e6 << "[MW], breakoverPower="
        << breakoverPower/1e6 << "[MW], t_beam="
        << t_beam*1e9 << "[ns]"
        << endl;
  writeProfileFile_header(ofile);
  ofile << "# t[ns] P[MW]" << endl;

  double t  = 0.0;
  double dt = (2*(t_rise+t_fill)+t_beam)/(numPoints-1.0);
  double P_t = 0.0;

  for (size_t i = 0; i < numPoints; i++){

    t = i*dt;
    P_t = getP_t(t,peakPower,t_beam,beamCurrent, breakoverPower);
    ofile << t << " " << P_t/1e6 << endl;
  }
  ofile.close();
}

double AccelStructure::getP_t(double t, double peakPower, double t_beam, double beamCurrent, double breakoverPower) const {
  if (breakoverPower < 0.0) {
    breakoverPower = getBreakoverPower(peakPower,beamCurrent);
  }

  double P_t = 0.0; //[W]
  if (t < t_rise) {
    P_t = t * breakoverPower/t_rise;
  }
  else if (t < (t_rise+t_fill)) {
    P_t = breakoverPower +
      (t-t_rise) * (peakPower-breakoverPower)/t_fill;
  }
  else if (t < (t_rise+t_fill+t_beam))
    P_t = peakPower;
  else if (t < (2*t_rise+t_fill+t_beam)) {
    P_t = peakPower - (t-t_rise-t_fill-t_beam) *
      breakoverPower / t_rise;
  }
  else {
    P_t = peakPower - breakoverPower + (t-2*t_rise-t_fill-t_beam) * (breakoverPower-peakPower) / t_fill;
  }

  return P_t;
}

void AccelStructure::populateWakePrecalc(){
  if (not needWakePrecalc()) {
    //pruneWakePrecalc();
    return;
  }

  wakePrecalc_zCell = new double[N];
  wakePrecalc_f_rad = new double[N];
  wakePrecalc_Q     = new double[N];
  wakePrecalc_A     = new double[N];

  for (int i = 0; i < N; i++) {

    double zCell = (L/(N-1.0))*i;                                                               //Position of data
    wakePrecalc_zCell[i] = zCell;                                                               // along structure axis

    wakePrecalc_f_rad[i] = 2*M_PI*getInterpolated(zCell,offsetof(struct CellParams, f1mn))*1e9; //Angular frequency [1/s]
    wakePrecalc_Q    [i] =        getInterpolated(zCell,offsetof(struct CellParams, Q1mn));     //Q-factor
    wakePrecalc_A    [i] =        getInterpolated(zCell,offsetof(struct CellParams, A1mn));     //Amplitude
  }

}
void AccelStructure::pruneWakePrecalc(){
  if (not needWakePrecalc()) {
    delete[] wakePrecalc_zCell; wakePrecalc_zCell = NULL;
    delete[] wakePrecalc_f_rad; wakePrecalc_f_rad = NULL;
    delete[] wakePrecalc_Q;     wakePrecalc_Q     = NULL;
    delete[] wakePrecalc_A;     wakePrecalc_A     = NULL;

    transWake_wavelength_min = -1;
    transWake_peaks.clear();
  }
}

double AccelStructure::getTransverseWakePotential(double z) const {
  if (cellFirst == NULL) {
    throw AccelStructureUninitialized("First cell has not been created!");
  }

  double t = z/Constants::speed_of_light;

  double Wt = 0.0;
  if (doPrecalculate) {
    if (wakePrecalc_zCell == NULL) {
      throw AccelStructureUninitialized("Wake precalculation not initialized.");
    }

    for (int i = 0; i < N; i++) {
      Wt += wakePrecalc_A[i]*exp(-wakePrecalc_f_rad[i]*t/(2.0*wakePrecalc_Q[i])) *
                             sin(wakePrecalc_f_rad[i]*t*sqrt(1.0-1.0/(4*wakePrecalc_Q[i]*wakePrecalc_Q[i])));
    }
  }
  else { //don't precalculate
    for (int i = 0; i < N; i++) {
      double zCell = (L/(N-1.0))*i; //Position of data along structure axis
      double f_rad = 2*M_PI*getInterpolated(zCell,offsetof(struct CellParams, f1mn))*1e9; //Angular frequency [1/s]
      double Q     =        getInterpolated(zCell,offsetof(struct CellParams, Q1mn)); //Q-factor
      double A     =        getInterpolated(zCell,offsetof(struct CellParams, A1mn)); //Amplitude
      Wt += A*exp(-f_rad*t/(2.0*Q)) * sin(f_rad*t*sqrt(1.0-1.0/(4*Q*Q)));
    }
  }
  return -Wt/double(N);
}
double AccelStructure::getTransverseWakePotentialEnvelope(double z) const {
  if (cellFirst == NULL) {
    throw AccelStructureUninitialized("First cell has not been created!");
  }

  double t = z/Constants::speed_of_light;

  double Wt = 0.0;
  if (doPrecalculate) {
    if (wakePrecalc_zCell == NULL) {
      throw AccelStructureUninitialized("Wake precalculation not initialized.");
    }

    for (int i = 0; i < N; i++) {
      Wt += wakePrecalc_A[i]*exp(-wakePrecalc_f_rad[i]*t/(2.0*wakePrecalc_Q[i]));
    }
  }
  else {
    for (int i = 0; i < N; i++) {
      double zCell = (L/(N-1.0))*i; //Position of data along structure axis
      double f_rad = 2*M_PI*getInterpolated(zCell,offsetof(struct CellParams, f1mn))*1e9; //Angular frequency [1/s]
      double Q     =        getInterpolated(zCell,offsetof(struct CellParams, Q1mn)); //Q-factor
      double A     =        getInterpolated(zCell,offsetof(struct CellParams, A1mn)); //Amplitude
      Wt += A*exp(-f_rad*t/(2.0*Q));
    }
  }
  return Wt/double(N);
}
double AccelStructure::getTransverseWakePotentialEnvelope_detuning(double z) {
  if (transWake_peaks.size() == 0) {
    //Initialize transWake_zSearchStep (once per structure)
    if (cellFirst == NULL) {
      throw AccelStructureUninitialized("First cell has not been created!");
  }

    double f = getByOffset(cellFirst,offsetof(struct CellParams, f1mn))*1e9;
    double Q = getByOffset(cellFirst,offsetof(struct CellParams, Q1mn));
    double waveLength = Constants::speed_of_light / (f * sqrt(1.0 - 1/(4*Q*Q)));
    transWake_wavelength_min = waveLength;
    //cout << "waveLength_first = " << waveLength << "[m], min =" << transWake_wavelength_min << endl;

    f = getByOffset(cellMid,offsetof(struct CellParams, f1mn))*1e9;
    Q = getByOffset(cellMid,offsetof(struct CellParams, Q1mn));
    waveLength = Constants::speed_of_light / (f * sqrt(1.0 - 1/(4*Q*Q)));
    if (waveLength < transWake_wavelength_min) transWake_wavelength_min = waveLength;
    //cout << "waveLength_mid = " << waveLength << "[m], min =" << transWake_wavelength_min << endl;

    f = getByOffset(cellLast,offsetof(struct CellParams, f1mn))*1e9;
    Q = getByOffset(cellLast,offsetof(struct CellParams, Q1mn));
    waveLength = Constants::speed_of_light / (f * sqrt(1.0 - 1/(4*Q*Q)));
    if (waveLength < transWake_wavelength_min) transWake_wavelength_min = waveLength;
    //cout << "waveLength_last = " << waveLength << "[m], min =" << transWake_wavelength_min << endl;

    transWake_wavelength_min /= 2.0; //Abs(W) => half the wave length

    //Define the negative interpolation point (starting from z=0)
    //Bracket backwards from 0.0, which is a zero-crossing:

    // Step length for initial peak search = 2/11*wavelength/2
    //  2/11 because multiple of step should not be one period.
    //  This is important in the case of constant impedance structures!
    double transWake_zSearchStep = transWake_wavelength_min*2.0/11.0;

    double z1 = 0.0-2*transWake_zSearchStep;
    double W1 = fabs(getTransverseWakePotential(z1));
    double z2 = 0.0-transWake_zSearchStep;
    double W2 = fabs(getTransverseWakePotential(z2));
    double z3 = 0.0;
    double W3 = fabs(getTransverseWakePotential(z3));

    bool found = false;
    for(int i = 0; i<100; i++) {
      // cout << "("<<z1<<", "<<W1<<") "
      //      << "("<<z2<<", "<<W2<<") "
      //      << "("<<z3<<", "<<W3<<") i= " << i << endl;
      if ( W2 > W1 and W2 > W3 ) {
        //cout << "FOUND!" << endl;
        found = true;
        break;
      }
      z3 = z2; z2 = z1;
      W3 = W2; W2 = W1;
      z1 -= transWake_zSearchStep;
      W1 = fabs(getTransverseWakePotential(z3));
    }
    if (not found) {
      stringstream ss;
      ss << "In getTransverseWakePotentialEnvelope_detuning(), reached max iterations, z= " << z;
      throw AccelStructureInternalError(ss.str());
    }

    transWake_goldenSearch(z1,W1,z2,W2,z3,W3);
    transWake_peaks.push_back(pair<double,double>(z2, W2));
  }
  if (z <= transWake_peaks[0].first) {
    std::stringstream ss;
    ss << "Can only calculate for z > first peak, zFirst=" << transWake_peaks[0].first;
    throw std::domain_error(ss.str());
  }

  while( z > transWake_peaks[transWake_peaks.size()-1].first ) {
    //Extend the peak array
    double z1,z2,z3,W1,W2,W3;
    transWake_bracketForward(transWake_peaks[transWake_peaks.size()-1].first, z1,W1, z2,W2, z3,W3);
    transWake_goldenSearch(z1,W1, z2,W2, z3,W3);
    transWake_peaks.push_back(pair<double,double>(z2,W2));
  }

  // cout << "PEAKS = ";
  // for(size_t i = 0; i < transWake_peaks.size(); i++) {
  //   cout << "(" << transWake_peaks[i].first << ", " << transWake_peaks[i].second << ") ";
  // }
  // cout << endl;

  //Interpolate
  for(size_t i = 0; i < transWake_peaks.size()-1; i++) {
    if (transWake_peaks[i].first <= z && transWake_peaks[i+1].first >= z) {
      return transWake_peaks[i].second + (z-transWake_peaks[i].first) *
             (transWake_peaks[i+1].second-transWake_peaks[i].second) /
             (transWake_peaks[i+1].first-transWake_peaks[i].first);
    }
  }

  throw AccelStructureInternalError("In getTransverseWakePotentialEnvelope_detuning(), didn't return?!?");
  return 0.0;//avoid compiler warnings
}
//Find the next peak, starting from z
void AccelStructure::transWake_bracketForward(double z,
                                              double& z1, double& W1,
                                              double& z2, double& W2,
                                              double& z3, double& W3 ) const {
  // Step length for initial peak search = 2/11*wavelength/2
  //  2/11 because multiple of step should not be one period.
  //  This is important in the case of constant impedance structures!
  double transWake_zSearchStep = transWake_wavelength_min*2.0/11.0;

  z1 = z;
  W1 = fabs(getTransverseWakePotential(z1));
  z2 = z+transWake_zSearchStep;
  W2 = fabs(getTransverseWakePotential(z2));
  z3 = z+2*transWake_zSearchStep;
  W3 = fabs(getTransverseWakePotential(z3));

  //Bracket
  bool found = false;
  for(int i = 0; i<100; i++) {
    // cout << "("<<z1<<", "<<W1<<") "
    //      << "("<<z2<<", "<<W2<<") "
    //      << "("<<z3<<", "<<W3<<") i= " << i << endl;
    if ( W2 > W1 and W2 > W3 ) {
      //cout << "FOUND!" << endl;
      found = true;
      break;
    }
    z1 = z2; z2 = z3;
    W1 = W2; W2 = W3;
    z3 += transWake_zSearchStep;
    W3 = fabs(getTransverseWakePotential(z3));
  }
  if (not found) {
    throw AccelStructureInternalError("In transWake_bracketForward(), reached max iterations.");
  }
}

void AccelStructure::transWake_goldenSearch(double& z1, double& W1, double& z2, double& W2, double& z3, double& W3) const {
  //Golden search for maxima
  // adapted from Numerical Recipies

  //Check that what we have is actually a bracket
  if (z1 >= z2 || z2 >= z3) {
    throw AccelStructureInternalError("Not a bracket in z");
  }
  if (W2 <= W1 || W2 <= W3) { // Huh on last condition
    throw AccelStructureInternalError("Not a bracket in W");
  }

  double zt0, zt1, zt2, zt3; // trial brackets
  double      Wt1, Wt2;      // only need to compare middle points,
                             //  know that edges are worse

  //Golden ratio
  const double R = 0.61803399;
  const double C = 1.0 - R;

  //Initialize
  zt0 = z1; zt3 = z3;
  if ( (z3-z2) > (z2-z1) ) { //upper is biggest
    zt1 = z2;
    zt2 = zt1+C*(z3-z2);

    Wt1 = W2;
    Wt2 = fabs(getTransverseWakePotential(zt2));

    //cout << "up" << endl;
  }
  else { //lower is biggest
    zt1 = z2-C*(z2-z1);
    zt2 = z2;

    Wt1 = fabs(getTransverseWakePotential(zt1));
    Wt2 = W2;

    //cout << "down" << endl;
  }

  // cout << "[" << zt0 << ", " << zt1 << ", " << zt2 << ", " << zt3 << "] -- "
  //      << "[" << Wt1  << ", " << Wt2 << "]" << endl;

  bool found = false;
  for (int i=0; i < 100; i++) {
    if (Wt1 > Wt2) {
      //cout << "A-";
      // New bracket (zt0,zt1,zt2)
      if ( (zt2-zt1) > (zt1-zt0) ) { //upper interval is biggest
        //zt0 = zt0;
        zt3 = zt2;

        //zt1 = zt1;
        zt2 = zt1+C*(zt3-zt1);

        //Wt1 = Wt1;
        Wt2 = fabs(getTransverseWakePotential(zt2));

        //cout << "up" << endl;
      }
      else { //lower interval is biggest OR equal size
        //zt0 = zt0;
        zt3 = zt2;

        zt2 = zt1;
        zt1 = zt2-C*(zt2-zt0);

        Wt2 = Wt1;
        Wt1 = fabs(getTransverseWakePotential(zt1));

        //cout << "down" << endl;
      }
    }
    else {
      //cout << "B-";
      //Wt1 <= Wt2, new bracket (zt1, zt2, zt3)
      if ( (zt3-zt2) > (zt2-zt1) ) { //Upper interval is biggest
        zt0 = zt1;
        //zt3 = zt3;

        zt1 = zt2;
        zt2 = zt1 + C*(zt3-zt1);

        Wt1 = Wt2;
        Wt2 = fabs(getTransverseWakePotential(zt2));

        //cout << "up" << endl;
      }
      else { //lower interval is biggest OR equal size
        zt0 = zt1;
        //zt3 = zt3;

        //zt2 = zt2;
        zt1 = zt2-C*(zt2-zt0);

        Wt1 = fabs(getTransverseWakePotential(zt1));
        //Wt2 = Wt2;

        //cout << "down" << endl;
      }
    }
    // cout << "[" << zt0 << ", " << zt1 << ", " << zt2 << ", " << zt3 << "] -- "
    //      << "[" << Wt1  << ", " << Wt2 << "]" << endl;
    //Convergence?
    if ( fabs(Wt1-Wt2) < 0.0001*max(Wt1,Wt2) && (zt3-zt0) < transWake_wavelength_min*0.0001) {
      //cout << "FOUND!" << endl;
      found = true;
      break;
    }
    if ((zt3-zt0) < sqrt( DBL_EPSILON ) ) break;
  }

  if (not found) {
    throw AccelStructureInternalError("In transWake_goldenSearch(), reached max iterations OR (zt3-zt0)<tol.");
  }

  //Return the best value
  if (Wt1 > Wt2) {
    z2 = zt1;
    W2 = Wt1;
  }
  else {
    z2 = zt2;
    W2 = Wt2;
  }
}

int AccelStructure::getMinBunchSpacing(double maxKick, bool detuning) {
  //All assertions handled by called functions.

  if (doPrecalculate && wakePrecalc_zCell==NULL) {
    populateWakePrecalc();
  }

  int trialSpacing = 1; const int maxTrialSpacing = 100;
  double RFperiod = 2*M_PI/getOmega();
  double wakeKick = 0.0;
  if (detuning)
    wakeKick = getTransverseWakePotentialEnvelope_detuning(trialSpacing*RFperiod*Constants::speed_of_light);
  else
    wakeKick = getTransverseWakePotentialEnvelope         (trialSpacing*RFperiod*Constants::speed_of_light);
#ifdef CHATTY_PROGRAM
  cout << "trying = " << wakeKick << endl;
#endif
  while (wakeKick > maxKick && trialSpacing < maxTrialSpacing) {
    trialSpacing +=1;
    if (detuning) wakeKick =
                    getTransverseWakePotentialEnvelope_detuning(trialSpacing*RFperiod*Constants::speed_of_light);
    else          wakeKick =
                    getTransverseWakePotentialEnvelope(trialSpacing*RFperiod*Constants::speed_of_light);
#ifdef CHATTY_PROGRAM
    cout << "trying = " << wakeKick << endl;
#endif
  }
  if (trialSpacing == maxTrialSpacing) {
#ifdef CHATTY_PROGRAM
    cout << "In getMinBunchSpacing(), reached maxTrialSpacing=" << maxTrialSpacing << endl;
#endif
    return 0;
  }
  return trialSpacing;
}
void AccelStructure::writeWakeFile(const char* const fname, double max_z, double delta_z) {

  if (fname == NULL) {
    throw std::invalid_argument("Got fname=NULL, this is not accepted.");
  }

  if (doPrecalculate && wakePrecalc_zCell==NULL) {
    populateWakePrecalc();
  }

  ofstream wakeFile(fname);
  wakeFile << "# z[m] Wt[V/pC/mm/m] fabs(Wt) Envelope(Wt) Envelope_detuning(Wt)" << endl;
  for (double z = 0.0; z < max_z; z+=delta_z) {
    wakeFile << z << " ";
    wakeFile << getTransverseWakePotential(z) << " ";
    wakeFile << fabs(getTransverseWakePotential(z)) << " ";
    wakeFile << getTransverseWakePotentialEnvelope(z) << " ";
    wakeFile << getTransverseWakePotentialEnvelope_detuning(z);
    wakeFile << endl;
  }
  wakeFile.close();
}

/* ***
 * ***
 * *** Constructors for different accelerator structure types
 * ***
 * ***/

/** ** AccelStructure_paramset1 implementation ** **/

void AccelStructure_paramSet1::createCells() {

  if (cellFirst != NULL) return;

  if (cellBase->numIndices != 3) {
    throw std::invalid_argument("AccelStructure_paramset1 expects 3 indices in the given cellBase");
  }
  if (not (cellBase->offsets[0] == off_psi &&
           cellBase->offsets[1] == off_a_n &&
           cellBase->offsets[2] == off_d_n   )){
    throw std::invalid_argument("AccelStructure_paramset1 expects indices in given cellBase to be {psi, a_n, d_n}.");
  }

  //Get the cells, assuming the parameters to are {psi, a_n, d_n}.
  // This is specified by the offset passed to the cellBase!
  vector<double> params = {psi_in, a_n+a_n_delta/2.0, d_n};
  cellFirst = new CellParams(cellBase->getCellInterpolated(params));
  params[1] = a_n;
  cellMid   = new CellParams(cellBase->getCellInterpolated(params));
  params[1] = a_n-a_n_delta/2.0;
  cellLast = new CellParams(cellBase->getCellInterpolated(params));

  //If required, scale the cells
  if (f0_scaleto > 0.0) {
    scaleCell(*cellFirst, f0_scaleto);
    scaleCell(*cellMid,   f0_scaleto);
    scaleCell(*cellLast,  f0_scaleto);
  }
}
void AccelStructure_paramSet1::writeProfileFile_header(ofstream& ofile) const{
  ofile << "# AccelStructure_paramSet1" << endl;
  ofile << "# L=" << L <<" [m], psi=" << psi_in << " [deg], a_n=" << a_n
        << ", a_n_delta=" << a_n_delta << ", d_n=" << d_n << endl;
}

/** ** AccelStructure_paramset2 implementation ** **/

void AccelStructure_paramSet2::createCells() {

  if (cellFirst != NULL) return;

  if (cellBase->numIndices != 3) {
    throw std::invalid_argument("AccelStructure_paramset2 expects 3 indices in the given cellBase");
  }
  if (not (cellBase->offsets[0] == off_psi &&
           cellBase->offsets[1] == off_a_n &&
           cellBase->offsets[2] == off_d_n   )) {
    throw std::invalid_argument("AccelStructure_paramset2 expects indices in given cellBase to be {psi, a_n, d_n}.");
  }

  //Get the cells, assuming the parameters to are {psi, a_n, d_n}.
  // This is specified by the offset passed to the cellBase!
  vector<double> params = {psi_in, a_n+a_n_delta/2.0, d_n+d_n_delta/2.0};
  //cout << params[0] << " " <<params[1] << " " << params[2] << endl;
  cellFirst = new CellParams(cellBase->getCellInterpolated(params));
  params[1] = a_n;
  params[2] = d_n;
  //cout << params[0] << " " <<params[1] << " " << params[2] << endl;
  cellMid   = new CellParams(cellBase->getCellInterpolated(params));
  params[1] = a_n-a_n_delta/2.0;
  params[2] = d_n-d_n_delta/2.0;
  //cout << params[0] << " " <<params[1] << " " << params[2] << endl;
  cellLast = new CellParams(cellBase->getCellInterpolated(params));

  //If required, scale the cells
  if (f0_scaleto > 0.0) {
    scaleCell(*cellFirst, f0_scaleto);
    scaleCell(*cellMid,   f0_scaleto);
    scaleCell(*cellLast,  f0_scaleto);
  }
}
void AccelStructure_paramSet2::writeProfileFile_header(ofstream& ofile) const{
  ofile << "# AccelStructure_paramSet2" << endl;
  ofile << "# L=" << L <<" [m], psi=" << psi_in << " [deg], a_n=" << a_n
        << ", a_n_delta=" << a_n_delta << ", d_n=" << d_n << ", d_n_delta=" << d_n_delta << endl;
}

/** ** AccelStructure_paramset2_noPsi implementation ** **/

void AccelStructure_paramSet2_noPsi::createCells() {

  if (cellFirst != NULL) return;

  if (cellBase->numIndices != 2) {
    throw std::invalid_argument("AccelStructure_paramset2_noPsi expects 3 indices in the given cellBase");
  }
  if (not (cellBase->offsets[0] == off_a_n &&
           cellBase->offsets[1] == off_d_n   )){
    throw std::invalid_argument("AccelStructure_paramset2_noPsi expects indices in given cellBase to be {a_n, d_n}.");
  }

  //Get the cells, assuming the parameters to are {a_n, d_n}.
  // This is specified by the offset passed to the cellBase!
  vector<double> params = {a_n+a_n_delta/2.0, d_n+d_n_delta/2.0};
  cellFirst = new CellParams(cellBase->getCellInterpolated(params));
  params[0] = a_n;
  params[1] = d_n;
  cellMid   = new CellParams(cellBase->getCellInterpolated(params));
  params[0] = a_n-a_n_delta/2.0;
  params[1] = d_n-d_n_delta/2.0;
  cellLast = new CellParams(cellBase->getCellInterpolated(params));

  //If required, scale the cells
  if (f0_scaleto > 0.0) {
    scaleCell(*cellFirst, f0_scaleto);
    scaleCell(*cellMid,   f0_scaleto);
    scaleCell(*cellLast,  f0_scaleto);
  }
}
void AccelStructure_paramSet2_noPsi::writeProfileFile_header(ofstream& ofile) const{
  ofile << "# AccelStructure_paramSet2_noPsi" << endl;
  ofile << "# L=" << L <<"[m], a_n=" << a_n << ", a_n_delta=" << a_n_delta
        << ", d_n=" << d_n << ", d_n_delta=" << d_n_delta << endl;
}

/** ** AccelStructure_CLIC502 implementation ** **/

void AccelStructure_CLIC502::createCells() {

  if (cellFirst != NULL) return;

  const double lambda = Constants::speed_of_light/11.9942e9;
  const double h = 10.41467e-3; //[m]

  cellFirst = new CellParams();
  cellFirst->h   = h;
  cellFirst->a   = 3.97e-3;
  cellFirst->d_n = 2.08e-3/h;  //d/h
  cellFirst->a_n = cellFirst->a/lambda;
  cellFirst->f0  = 11.993916; //[GHz]
  cellFirst->psi = 150.0;    //psi [deg]
  cellFirst->Q   = 6364.8;   //Q
  cellFirst->vg  = 2.056;    //vg [%c]
  cellFirst->rQ  = 10304.92; //rQ
  cellFirst->Es  = 2.25;     //Es
  cellFirst->Hs  = 4.684;    //Hs
  cellFirst->Sc  = 0.493;    //Sc
  cellFirst->f1mn = 52.78076151*Constants::speed_of_light/1e9; //Convert k [1/m] -> f [GHz]
  cellFirst->Q1mn = 16.78249817;
  cellFirst->A1mn = 77.23336969;

  cellMid = new CellParams();
  cellMid->h   = h;
  cellMid->a   = 3.625e-3;
  cellMid->d_n = 1.875e-3/h;  //d/h
  cellMid->a_n = cellMid->a/lambda;
  cellMid->f0  = 11.993975; //[GHz]
  cellMid->psi = 150.0;     //psi [deg]
  cellMid->Q   = 6370.5;    //Q
  cellMid->vg  = 1.614;     //vg [%c]
  cellMid->rQ  = 11213.4;  //rQ
  cellMid->Es  = 2.23;     //Es
  cellMid->Hs  = 4.511;      //Hs
  cellMid->Sc  = 0.435;     //Sc

  cellLast = new CellParams();
  cellLast->h   = h;
  cellLast->a   = 3.28e-3;
  cellLast->d_n = 1.67e-3/h;  //d/h
  cellLast->a_n = cellLast->a/lambda;
  cellLast->f0  = 11.993984; //[GHz]
  cellLast->psi = 150.0;     //psi [deg]
  cellLast->Q   = 6383;    //Q
  cellLast->vg	= 1.234;     //vg [%c]
  cellLast->rQ  = 12175.9;  //rQ
  cellLast->Es  = 2.22;     //Es
  cellLast->Hs  = 4.342;      //Hs
  cellLast->Sc  = 0.381;     //Sc
  cellLast->f1mn = 54.50428264*Constants::speed_of_light/1e9; //Convert k [1/m] -> f [GHz]
  cellLast->Q1mn = 9.16779521;
  cellLast->A1mn = 112.422794;

  cellMid->f1mn = (cellFirst->f1mn+cellLast->f1mn)/2.0;
  cellMid->Q1mn = (cellFirst->Q1mn+cellLast->Q1mn)/2.0;
  cellMid->A1mn = (cellFirst->A1mn+cellLast->A1mn)/2.0;

  scaleCell(*cellFirst,f0_scaleto);
  scaleCell(*cellMid,  f0_scaleto);
  scaleCell(*cellLast, f0_scaleto);
}

void AccelStructure_CLIC502::writeProfileFile_header(ofstream& ofile) const{
  ofile << "# AccelStructure_CLIC502" << endl;
}

/** ** AccelStructure_CLICG implementation ** **/

void AccelStructure_CLICG::createCells() {

  if (cellFirst != NULL) return;

  const double lambda = Constants::speed_of_light/11.9942e9; //[m]
  const double h = (120.0/360.0)*lambda; //[m]

  if (this->isR05) {
    cellFirst = new CellParams();
    cellFirst->h   = h;
    cellFirst->a   = 3.15e-3;
    cellFirst->d_n = 1.67e-3/h;  //d/h
    cellFirst->a_n = cellFirst->a/lambda;
    cellFirst->f0  = 11.9942; //[GHz]
    cellFirst->psi = 120.0;     //psi [deg]
    cellFirst->Q   = 5536;    //Q
    cellFirst->vg  = 1.65;     //vg [%c]
    cellFirst->rQ  = 14587;  //rQ
    cellFirst->Es  = 1.95;     //Es
    cellFirst->Hs  = 4.1;      //Hs
    cellFirst->Sc  = 0.41;     //Sc
    cellFirst->f1mn = 16.91;
    cellFirst->Q1mn = 11.1;
    cellFirst->A1mn = 125.0;

    cellMid = new CellParams();
    cellMid->h   = h;
    cellMid->a   = 2.75e-3;
    cellMid->d_n = 1.335e-3/h;  //d/h
    cellMid->a_n = cellMid->a/lambda;
    cellMid->f0  = 11.9942; //[GHz]
    cellMid->psi = 120.0;     //psi [deg]
    cellMid->Q   = 5635;    //Q
    cellMid->vg  = 1.2;     //vg [%c]
    cellMid->rQ  = 16220;  //rQ
    cellMid->Es  = 1.93;     //Es
    cellMid->Hs  = 3.85;      //Hs
    cellMid->Sc  = 0.35;     //Sc
    cellMid->f1mn = 17.35;
    cellMid->Q1mn = 8.7;
    cellMid->A1mn = 156.0;

    cellLast = new CellParams();
    cellLast->h   = h;
    cellLast->a   = 2.35e-3;
    cellLast->d_n = 1.0e-3/h;  //d/h
    cellLast->a_n = cellLast->a/lambda;
    cellLast->f0  = 11.9942; //[GHz]
    cellLast->psi = 120.0;     //psi [deg]
    cellLast->Q   = 5738;    //Q
    cellLast->vg  = 0.83;     //vg [%c]
    cellLast->rQ  = 17954;  //rQ
    cellLast->Es  = 1.9;     //Es
    cellLast->Hs  = 3.6;      //Hs
    cellLast->Sc  = 0.3;     //Sc
    cellLast->f1mn = 17.80;
    cellLast->Q1mn = 7.1;
    cellLast->A1mn = 182.0;
  }
  else {
    cellFirst = new CellParams();
    cellFirst->h   = h;
    cellFirst->a   = 3.15e-3;
    cellFirst->d_n = 1.67e-3/h;  //d/h
    cellFirst->a_n = cellFirst->a/lambda;
    cellFirst->f0  = 11.9942; //[GHz]
    cellFirst->psi = 120.0;     //psi [deg]
    cellFirst->Q   = 5654;    //Q
    cellFirst->vg  = 1.617;     //vg [%c]
    cellFirst->rQ  = 14271;  //rQ
    cellFirst->Es  = 2.05;     //Es
    cellFirst->Hs  = 4.75;      //Hs
    cellFirst->Sc  = 0.42;     //Sc
    cellFirst->f1mn = 0.0;
    cellFirst->Q1mn = 0.0;
    cellFirst->A1mn = 0.0;

    cellMid = new CellParams();
    cellMid->h   = h;
    cellMid->a   = 2.75e-3;
    cellMid->d_n = 1.335e-3/h;  //d/h
    cellMid->a_n = cellMid->a/lambda;
    cellMid->f0  = 11.9942; //[GHz]
    cellMid->psi = 120.0;     //psi [deg]
    cellMid->Q   = 5736;    //Q
    cellMid->vg  = 1.168;     //vg [%c]
    cellMid->rQ  = 15840;  //rQ
    cellMid->Es  = 2.05;     //Es
    cellMid->Hs  = 4.6;      //Hs
    cellMid->Sc  = 0.36;     //Sc
    cellMid->f1mn = 0.0;
    cellMid->Q1mn = 0.0;
    cellMid->A1mn = 0.0;

    cellLast = new CellParams();
    cellLast->h   = h;
    cellLast->a   = 2.35e-3;
    cellLast->d_n = 1.0e-3/h;  //d/h
    cellLast->a_n = cellLast->a/lambda;
    cellLast->f0  = 11.9942; //[GHz]
    cellLast->psi = 120.0;     //psi [deg]
    cellLast->Q   = 5822;    //Q
    cellLast->vg  = 0.811;     //vg [%c]
    cellLast->rQ  = 17443;  //rQ
    cellLast->Es  = 2.08;     //Es
    cellLast->Hs  = 4.45;      //Hs
    cellLast->Sc  = 0.315;     //Sc
    cellLast->f1mn = 0.0;
    cellLast->Q1mn = 0.0;
    cellLast->A1mn = 0.0;
  }

  scaleCell(*cellFirst,f0_scaleto);
  scaleCell(*cellMid,  f0_scaleto);
  scaleCell(*cellLast, f0_scaleto);
}

void AccelStructure_CLICG::writeProfileFile_header(ofstream& ofile) const{
  ofile << "# AccelStructure_CLICG" << endl;
}

/** ** AccelStructure_general implementation ** **/

void AccelStructure_general::createCells() {
  if (cellFirst != NULL) return;
  cellFirst = new CellParams(cellFirst_copy);
  cellMid   = new CellParams(cellMid_copy);
  cellLast  = new CellParams(cellLast_copy);
}

AccelStructure_general AccelStructure_general::copy_structure(AccelStructure& source, const char* const headerLine) {
  //TODO: Check pruning and re-prune if this was the case
  source.createCells(); // In case of pruning
  return AccelStructure_general(source.N, source.getCellFirst(),source.getCellMid(),source.getCellLast(), headerLine);
}

void AccelStructure_general::writeProfileFile_header(ofstream& ofile) const {
  ofile << "# AccelStructure_general" << endl;
  ofile << "# Header line = '" << headerline << "'" << endl;
}
