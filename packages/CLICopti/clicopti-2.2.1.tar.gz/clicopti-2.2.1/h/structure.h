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

#ifndef STRUCTURE_H
#define STRUCTURE_H

#include <fstream>
#include <cstddef> //offsetof
#include <cmath>
#include <stdexcept>

#include <vector>
#include <utility> //std::pair

#include "cellParams.h"
#include "cellBase.h"
#include "constants.h"

/*
 * References:
 * [1]: "Analytical solutions for transient and steady-state
 *      beam loading in arbitrary traveling wave accelerating structures",
 *      A. Lunin, V. Yakovlev, A. Grudiev
 *      PRST-AB 14, 2011
 * [2]: "RF Pulsed heating",
 *      David P. Pritzkau,
 *      SLAC report 577
 */

//Return structs for AccelStructure
struct return_AccelStructure_getMaxFields {
  double maxEs; // [MV/m]    (absolute value)
  double maxHs; // [kA/m]    (absolute value)
  double maxSc; // [W/um^2]  (absolute value)
  double maxPC; // [MW/mm]   (absolute value)
  size_t maxEs_idx;
  size_t maxHs_idx;
  size_t maxSc_idx;
  size_t maxPC_idx;
};
std::ostream& operator<< (std::ostream &out, const return_AccelStructure_getMaxFields& maxFields);

struct return_AccelStructure_getMaxDeltaT {
  double maxDeltaT; // [K]
  double maxDeltaT_idx;
};
std::ostream& operator<< (std::ostream &out, const return_AccelStructure_getMaxDeltaT& maxDeltaT);

struct return_AccelStructure_getMaxAllowableBeamTime_detailed {
  //Input
  double power; //Input power [W]
  double beamCurrent_pulseShape; // Beam current for pulse shape calculation [A]
  double beamCurrent_loading;    // Beam current for field profile with beam loading [A]
  double powerFraction; //Fraction of peak power counted
  //Results
  return_AccelStructure_getMaxFields maxFields; //Peak fields
  double wastedTime; //Time from the pulse which is wasted [s]
  double time_E;  //Time from electric field [s]
  double time_Sc; //Time from Sc [s]
  double time_dT; //Time from delta T [s]
  double time_PC; //Time from P/C [s]

  double time; //min(time_E, time_Sc, time_dT, time_PC)
  char which;  //E = electric field, S = Sc, T = delta T, or P = P/C
};
std::ostream& operator<< (std::ostream &out, const return_AccelStructure_getMaxAllowableBeamTime_detailed& timeData);

/* Exceptions */

// basically just renaming logic_error
// Inspired by https://stackoverflow.com/a/8152888
class AccelStructureUninitialized : public std::logic_error {
  public:
  /** Constructor (C strings).
     *  @param message C-style string error message.
     *                 The string contents are copied upon construction.
     *                 Hence, responsibility for deleting the char* lies
     *                 with the caller.
     */
    explicit AccelStructureUninitialized(const char* message)
        : std::logic_error(message) {}

    /** Constructor (C++ STL strings).
     *  @param message The error message.
     */
    explicit AccelStructureUninitialized(const std::string& message)
        : std::logic_error(message) {}
};
// basically just renaming logic_error
// Inspired by https://stackoverflow.com/a/8152888
class AccelStructureInternalError : public std::logic_error {
  public:
  /** Constructor (C strings).
     *  @param message C-style string error message.
     *                 The string contents are copied upon construction.
     *                 Hence, responsibility for deleting the char* lies
     *                 with the caller.
     */
    explicit AccelStructureInternalError(const char* message)
        : std::logic_error(message) {}

    /** Constructor (C++ STL strings).
     *  @param message The error message.
     */
    explicit AccelStructureInternalError(const std::string& message)
        : std::logic_error(message) {}
};

/**
 * This class calculates represents a single main beam accelerating structure,
 * and calculates its parameters.
 */
class AccelStructure {
  //Initializers etc.
 public:
  AccelStructure(int N) :
    has_integrals(false), has_integral_results(false),
    g(NULL), g_load(NULL), z(NULL), z_numPoints(0),
    transWake_wavelength_min(-1),
    N(N),
    cellFirst(NULL), cellMid(NULL), cellLast(NULL),
    cellsInterpolated(NULL), cell0(NULL),
    wakePrecalc_zCell(NULL), wakePrecalc_f_rad(NULL), wakePrecalc_Q(NULL), wakePrecalc_A(NULL) {};
  virtual ~AccelStructure();
 protected:
  void initializeBase();

 public:

  //RF parameters
  // Here comes functions for calculating power requirements,
  // peak surface fields, G_loaded etc.
  // as function of G_ul, pulse, and beam properties.
  // Possibly it might be a good idea to have a function
  // to "set" G_loaded etc., and then store results as class fields.
  // Also possible to have these "calculation functions" respond to
  // configuration by other (static?) class fields.

  /** Steady-state power flow calculations **/

  //Given the cell parameters, calculate the integral appearing
  // inside the exp() in g(z) from Eq. 2.13 in [1] and
  // store g(z) along the structure in g and z.
  // Also calculate the loading integral from Eq. 2.14
  // and store the result in g_load
  void calc_g_integrals(size_t numPoints = 200);
  //Delete the contents of g, g_load, and z in order to save memory.
  void prune_integrals();

  inline size_t getZNumpoints() {
    if (not has_integrals) {
      throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
    }
    return z_numPoints;
  };
  inline double getZ(size_t idx) {
    if (not has_integrals) {
      throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
    }
    if (idx >= z_numPoints) {
      throw std::domain_error("idx > z_numPoints");
    }
    return z[idx];
  }

  //Caluclate Ez [V/m] at a given z-index idx (loaded and unloaded cases) for a given power [W]
  inline double getEz_unloaded(size_t idx,double peakPower) const {
    if (not has_integrals) {
      throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
    }
    return g[idx] * sqrt(omega * getInterpolated(0.0,offsetof(struct CellParams, rQ)) * peakPower /
                         (getInterpolated(0,offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01) );
  }
  inline double getEz_loaded(size_t idx, double peakPower, double current) const {
    //Has_integrals assumption in getEz_unloaded()
    return getEz_unloaded(idx,peakPower) - current*g_load[idx];
  }

 private:
  inline double* z_integral_helper(double* intVar) const {return integral_helper(intVar,h,z_numPoints);};
  bool has_integrals, has_integral_results;
  double* g; double* g_load; double* z; size_t z_numPoints; double h;
  double g_int; double g_load_int;
  double omega;  //Angular frequency [1/s]
  double psi;    //Phase advance per cell [degrees]
  double t_fill; //Filling time [s]
  double t_rise; //Rise time to breakoverPower [s] (dependent on structure bandwidth) //TODO: is it not *from* breakoverPower?
 public:
  //Unloaded voltage and power in Volts and Watts
  double getPowerUnloaded(double voltageUnloaded) const;
  double getVoltageUnloaded(double power) const;
  //Loaded voltage and power in Volts and Watts, beam current in Amperes
  double getPowerLoaded(double voltageLoaded, double beamCurrent) const;
  double getVoltageLoaded(double power, double beamCurrent) const;
  double getLoadingVoltage(double beamCurrent) const;
  //Get t_fill and t_rise [s]
  double getTfill() const;
  double getTrise() const;
  //Get angular frequency of main mode [1/s]
  inline double getOmega() const { return omega; };
  //Get frequency of main mode [Hz]
  inline double getF0()    const { return omega/(2*M_PI); };
  //Get the phase advance per cell of the main mode [deg]
  inline double getPsi()   const { return psi;   }
  //Get the maximal values of the field along the structure and their position. Input in Watt and Amperes,
  // output units as specified in structure return_AccelStructure_getMaxFields [!!NON-SI!!].
  return_AccelStructure_getMaxFields getMaxFields(double power, double beamCurrent=0.0) const;
  //Write the gradient, and peak surface field profiles to file. Input in Watt and Amperes
  void writeProfileFile(const char* const fname, double power, double beamCurrent=0.0);
  //Write the cell parameters profiles along the structure to a file.
  void writeParameterProfileFile(const char* const fname);

  //Find the maximum allowable input power given the beam current and peak Es, Sc constraints.
  // Peak field units as specified in structure return_AccelStructure_getMaxFields [!!NON-SI!!].
  // If this leads to a loaded voltage <= 0, return 0.0., else return the power [W]
  double getMaxAllowablePower(double beamCurrent, double max_Es, double max_Sc) const;

  //Find the maximum allowable input power given the beam current [A] and beamTime pulse length [t]
  // If no solution with power>0 is found, return 0.0
  double getMaxAllowablePower_beamTimeFixed(double beamCurrent, double beamTime) const;

  static const double constBDR0; //[Breakdowns per pulse per meter] Reference breakdown rate for scaling (value set in structure.cpp)
  static const double constTau0; //[s] Reference pulse length for scaling (value set in structure.cpp)

  //Find the max allowable t_beam [s] for a given power [W] and beam current [A]
  // using the peak field constraints on the rectangle-equivalent pulse
  // May return negative value if wastedTime > max rectangular-equivalent time.
  double getMaxAllowableBeamTime_E (double power, double beamCurrent) const;
  double getMaxAllowableBeamTime_E_hasPeak(double maxEs,  double wastedTime)  const;
  static const double maxConstE; //[(MV/m)^6 * s] (default value set in structure.cpp)

  double getMaxAllowableBeamTime_Sc(double power, double beamCurrent)  const;
  double getMaxAllowableBeamTime_Sc_hasPeak(double maxSc, double wastedTime) const;
  static const double maxConstSc; //[(MW/mm^2)^3 * s] (default value set in structure.cpp)

  double getMaxAllowableBeamTime_PC(double power, double beamCurrent) const;
  double getMaxAllowableBeamTime_PC_hasPeak(double maxPC, double wastedTime) const;
  static const double maxConstPC; //[(MW/mm)^3 * s] (default value set in structure.cpp)

  //Get the overall maximum beam time [s] for the given power [W] and beamCurrent[A],
  // taking restrictions from E_surf, S_c, P/C and deltaT into account.
  // Return 0.0 if no good solution found.
  inline double getMaxAllowableBeamTime(double power, double beamCurrent) const {
    return getMaxAllowableBeamTime_detailed(power, beamCurrent).time;
  }
  // Same as above, but return more data
  // If beamCurrent_loading < 0, use beamCurrent_pulseShape
  // If powerFraction < 0, use the default from constPulsePowerFraction.
  // If BDR < 0, use the default constBDR0, else scale the limits for E,Sc, and P/C to this BDR [breakdowns per pulse per meter]
  return_AccelStructure_getMaxAllowableBeamTime_detailed
    getMaxAllowableBeamTime_detailed(double power, double beamCurrent_pulseShape,
                                     double beamCurrent_loading=-1.0, double powerFraction=-1.0,
                                     double BDR=-1.0) const;

  //Which limits to use in the overall max allowable beamtime calculation
  bool uselimit_E  = true;
  bool uselimit_Sc = true;
  bool uselimit_PC = true;
  bool uselimit_dT = true;

  //Scale the E, Sc, PC, values of a given beamtime object to a different BDR than the one given by constBDR0
  return_AccelStructure_getMaxAllowableBeamTime_detailed
    scaleBeamtimeBDR(return_AccelStructure_getMaxAllowableBeamTime_detailed beamtime, double BDR) const;

  /** Efficiency calculations **/

  //RF->beam efficiency for an infinite flattop pulse (fraction in [0,1.0])
  // as a function of peak power [W], beam current [A], and t_beam [s].
  inline double getFlattopEfficiency(double peakPower, double beamCurrent) const {
    return beamCurrent*getVoltageLoaded(peakPower, beamCurrent)/peakPower;
  }
  inline double getTotalEfficiency(double peakPower, double beamCurrent, double t_beam) const {
    return getFlattopEfficiency(peakPower, beamCurrent) * t_beam /(t_beam+t_fill+t_rise);
  }

  /** Pulse shape **/

  //Calculate the "breakoverPower" [W] for the beam loading compensation scheme
  // at a given flat-top power [W] and beam current [A]
  inline double getBreakoverPower(double peakPower, double beamCurrent) const {
    if (not has_integrals) {
      throw AccelStructureUninitialized("Integrals have never been calculated or have been pruned.");
    }
    if (not has_integral_results) {
      throw AccelStructureUninitialized("Integrals have never been calculated.");
    }

    //Equation (4.5) in [1], t=0

    return peakPower *
      pow(1.0 - sqrt(getInterpolatedZero(offsetof(struct CellParams, vg))*Constants::speed_of_light*0.01 /
                     (omega*getInterpolatedZero(offsetof(struct CellParams, rQ))*peakPower) ) *
          beamCurrent*g_load[z_numPoints-1]/g[z_numPoints-1], 2);
    //std::cout << g_load[z_numPoints-1] << " " << g[z_numPoints-1] << " " << ret << std::endl;
    //return ret;
  }

  //With the given pulse shape (peakPower[W] and beamCurrent[A]),
  // calculate the time [s] during the ramp and decay
  // when RF power > fraction*peakPower.
  // Add this to t_beam to get the total time where power > fraction*peakPower.
  // This is used for the time dependence in BDR scalings
  // If powerFraction < 0, use the default from constPulsePowerFraction.
  double getExtraTimePowerAboveFraction(double peakPower, double beamCurrent, double powerFraction = -1.0) const;
  static const double constPulsePowerFraction;

  /** DeltaT calculations **/
 public:
  //Calculate the time-independent constant (time-integral) for deltaT
  // at end of beam pulse (assumed maximum),
  // based on output from calc_g_integrals().
  // This is used to find the maximum deltaT.
  double getDeltaTconst(double peakPower, double t_beam, double beamCurrent) const;

  // Calculate peak deltaT [K] as a function of z-index along the structure.
  // Set loaded = false to use a pulse for a given beam current, but without the loading.
  // Set deltaTconst > 0.0 to use output from getDeltaTconst
  // Units K, W, s, A.
  double getDeltaT(double peakPower, double t_beam, double beamCurrent, size_t zIdx, bool loaded=false, double deltaTconst=-1.0) const;
  //Get maximum deltaT [K] and its position [idx] for a given power [W], beam-time [s], and beam current [A].
  // Use a loaded/unloaded beam profile
  return_AccelStructure_getMaxDeltaT getMaxDeltaT(double peakPower, double t_beam, double beamCurrent, bool loaded=true) const;
  //Given the peak surface magnetic field [kA/m] and output from getDeltaTconst(),
  double getMaxDeltaT_hasPeak(double maxHs, double deltaTconst) const;

  //Write the deltaT profile along the structure as function of z
  void writeDeltaTprofileFile(const char* const fname, double peakPower, double t_beam, double beamCurrent, bool loaded=false);
  //Write the maximum Delta T in the structure as a function of t_beam
  void writeTimeDeltaTprofileFile(const char* const fname, double peakPower,
                                  double t_beam_max, double beamCurrent,
                                  bool loaded=false, size_t numPoints=200);
  //Write input power as function of time
  void writeTimePowerProfileFile(const char* const fname, double peakPower,
                                 double t_beam, double beamCurrent, size_t numPoints=200) const;

  //Find the maximum allowed t_beam [s] with a pulse given by the peak power [W] and beam current [A],
  // with/without beam loading, and a limiting deltaT [K]. Returns t_beam [s].
  double getMaxAllowableBeamTime_dT(double peakPower, double beamCurrent, bool useLoadedField=false) const;
  double getMaxAllowableBeamTime_dT_hasPeak(double peakPower, double beamCurrent, double maxHs) const;
  static const double max_deltaT; //[K] (default value set in structure.cpp)

  //Compute P(t). If breakoverPower>=0, then use this a precalculated value.
  double getP_t(double t, double peakPower, double t_beam, double beamCurrent, double breakoverPower=-1.0) const;
 protected:
  //Helper function to writeProfileFile(), writeDeltaTprofileFile(), writeTimePowerProfileFile,
  // which identifies the structure.
  virtual void writeProfileFile_header(std::ofstream& ofile) const = 0;
 public:

  /** ** Wake parameters ** **/

  //Calculate the single bunch wake [V/pC/mm/m]
  // at position z [m] > 0 after the driving bunch
  double getTransverseWakePotential(double z) const;
  //Calculate the envelope of the single bunch wake [V/pC/mm/m],
  // at position z [m] > 0 after the driving bunch
  // not including detuning/interference effects.
  double getTransverseWakePotentialEnvelope(double z) const;
  //Calculate the envelope of the single bunch wake [V/pC/mm/m],
  // at position z [m] > 0 after the driving bunch
  // *including* detuning/interference effects.
  // Envelope taken using peak-to-peak linear approximation
  double getTransverseWakePotentialEnvelope_detuning(double z);

 private:
  //Temp variables to store state between runs
  std::vector<std::pair<double,double> > transWake_peaks; //(z, W)
  //Minimum wavelength of the wake
  double transWake_wavelength_min;
  //Helper functions
  void transWake_bracketForward (double z, double& z1, double& W1, double& z2, double& W2, double& z3, double& W3) const;
  // Return estimated peak position in variables z2 and W2.
  void transWake_goldenSearch(double& z1, double& W1, double& z2, double& W2, double& z3, double& W3) const;
 public:
  //Find the minimum bunch spacing (in RF cycles) allowed by a given
  // maximum kick [V/pC/mm/m]. Returns 0 if no good solution found.
  // If detuning=true, call getTransverseWakePotentialEnvelope_detuning(),
  //  else getTransverseWakePotentialEnvelope()
  int getMinBunchSpacing(double maxKick, bool detuning=true);
  //Write the wake to file, with z ranging from 0 to max_z [m], sample spacing delta_z [m]
  void writeWakeFile(const char* const fname, double max_z, double delta_z);



  //Basic geometry parameters
 public:
  const int N; //Number of cells
 protected:
  double    L; //Structure length [m]
               //(can't be const as it's calculated from cell->h in subclass constructor)
 public:
  inline double getL() const {
    return L;
  }

  /**
   * Return pointers to copy's of the first/mid/last cell.
   * If cells has been pruned, return NULL
   */
  inline CellParams* getCellFirstPtr() const {return (cellFirst != NULL ? new CellParams(*cellFirst) :  NULL);};
  inline CellParams* getCellMidPtr()   const {return (cellMid   != NULL ? new CellParams(*cellMid)   :  NULL);};
  inline CellParams* getCellLastPtr()  const {return (cellLast  != NULL ? new CellParams(*cellLast)  :  NULL);};
  /**
   * Return read-only references to the first/mid/last cell
   * (usefull for printing!)
   */
  inline const CellParams&  getCellFirst() {this->createCells(); return *cellFirst;};
  inline const CellParams&  getCellMid()   {this->createCells(); return *cellMid;};
  inline const CellParams&  getCellLast()  {this->createCells(); return *cellLast;};

  //Delete any cells in order to save memory. If no cells, do nothing.
  void pruneCells();
  //If the cells have been pruned, resurrect them using the given structure parameters.
  // Else do nothing.
  virtual void createCells() = 0;
 protected:
  //Interpolation basis cells
  CellParams* cellFirst;
  CellParams* cellMid;
  CellParams* cellLast;

  //General helpfull functions
 public:
  //Integrate from 0 to z for all z
  double* integral_helper(double* intVar, double step, size_t numPoints) const;

  //Interpolate some parameter to point z, given the first/middle/last cell value
  /**
   * Get the interpolated value of a given field at position z.
   * if midEnds=true, use middle of end cells as first/last interpolation "anchors".
   */
  inline double getInterpolated(double z, size_t field_offset, bool midEnds=false) const {
    return interpolate3(getByOffset(cellFirst,field_offset),
                        getByOffset(cellMid,  field_offset),
                        getByOffset(cellLast, field_offset),
                        z, midEnds);
  };

  inline double getInterpolated_zidx(size_t z_idx, size_t field_offset) const { //Always assume midEnds=false
    if (doPrecalculate) {
      if (cellsInterpolated == NULL) {
        throw AccelStructureUninitialized("cellsInterpolated not initialized");
      }
      if ( z_idx < 0 || z_idx >= z_numPoints) {
        throw std::domain_error("z_idx outside of valid range");
      }
      //IMPORTANT: This only really works for a,vg,Q,rQ,Es,Hs,Sc. Other fields WILL give undefined results!
      return getByOffset(cellsInterpolated[z_idx],field_offset);
    }
    return getInterpolated(z[z_idx],field_offset);
  }
  inline double getInterpolatedZero(size_t field_offset) const {
    if (doPrecalculate) {
      //IMPORTANT: This only really works for vg and rQ. Other fields WILL give undefined results!
      // See implementation of AccelStructure::populateCellsInterpolated for more info.
      if (cellsInterpolated == NULL) {
        throw AccelStructureUninitialized("cellsInterpolated not initialized");
      }
      return getByOffset(cell0,field_offset);
    }
    return getInterpolated(0.0,field_offset);
  }

  double interpolate3(double first, double mid, double last, double z, bool midEnds=false) const;

 private:
  //Set this to "true" to activate precalculation
  static const bool doPrecalculate;

  //Main mode RF parameters
  CellParams* cellsInterpolated; //array of cells
  CellParams* cell0;             //cell at z=0
  void populateCellsInterpolated();

  //Wakefield parameters
  double* wakePrecalc_zCell;
  double* wakePrecalc_f_rad;
  double* wakePrecalc_Q;
  double* wakePrecalc_A;

  void pruneWakePrecalc();
public:
  inline bool needWakePrecalc() const {return wakePrecalc_zCell==NULL;}
  void populateWakePrecalc();
};

//Accelerating structure parameterization dependent on N, psi, a, delta a, and d.
// See createCells() for the implementation.
class AccelStructure_paramSet1 : public AccelStructure {
 public:
  AccelStructure_paramSet1 (CellBase* cellBase,
                            int N,
                            double psi,
                            double a_n, double a_n_delta,
                            double d_n,
                            double f0_scaleto = -1.0
                            ) :
  AccelStructure(N),
    psi_in(psi), a_n(a_n), a_n_delta(a_n_delta),
    d_n(d_n), f0_scaleto(f0_scaleto),
    cellBase(cellBase) { initializeBase(); };

  const double psi_in;    //Phase advance per cell [deg]

  const double a_n;       //Average iris aperture / lambda (normalized aperture)
  const double a_n_delta; //Normalized iris aperture difference first-last

  const double d_n;       //Average iris thickness / cell period h (normalized thickness)

  const double f0_scaleto;//Frequency to scale the structure to [GHz]. Set to <=0.0 to disable scaling (i.e. use the scaling from cellBase).

  virtual void createCells();


 private:
  virtual void writeProfileFile_header(std::ofstream& ofile) const;

  // Pointer to the cellBase, shared by all instances
  // Note: For paralellization it might be nice to un-share this
  // (depends on the CellBase implementation's thread-safeness)
  CellBase* cellBase;
};

//Accelerating structure parameterization dependent on N, psi, a, delta a, d, and ALSO delta d.
// See createCells() for the implementation.
class AccelStructure_paramSet2 : public AccelStructure {
 public:
  AccelStructure_paramSet2 (CellBase* cellBase,
                            int N,
                            double psi,
                            double a_n, double a_n_delta,
                            double d_n, double d_n_delta,
                            double f0_scaleto = -1.0 ) :
    AccelStructure(N),
    psi_in(psi), a_n(a_n), a_n_delta(a_n_delta),
    d_n(d_n), d_n_delta(d_n_delta),
    f0_scaleto(f0_scaleto), cellBase(cellBase) {

    initializeBase();
  };

  const double psi_in;    //Phase advance per cell [deg]

  const double a_n;       //Average iris aperture / lambda (normalized aperture)
  const double a_n_delta; //Normalized iris aperture difference first-last

  const double d_n;       //Average iris thickness / cell period h (normalized thickness)
  const double d_n_delta; //Normalized iris thickness difference first-last

  const double f0_scaleto;//Frequency to scale the structure to [GHz]. Set to <=0.0 to disable scaling (i.e. use the scaling from cellBase).

  virtual void createCells();

 private:
  virtual void writeProfileFile_header(std::ofstream& ofile) const;

  // Pointer to the cellBase, shared by all instances
  // Note: For paralellization it might be nice to un-share this
  // (depends on the CellBase implementation's thread-safeness)
  CellBase* cellBase;
};

//Accelerating structure parameterization dependent on N, a, delta a, d, and ALSO delta d but NOT psi.
// See createCells() for the implementation. Intended for use with new database.
class AccelStructure_paramSet2_noPsi : public AccelStructure {
 public:
  AccelStructure_paramSet2_noPsi (CellBase* cellBase,
                                  int N,
                                  double a_n, double a_n_delta,
                                  double d_n, double d_n_delta,
                                  double f0_scaleto = -1.0 ) :
  AccelStructure(N),
    a_n(a_n), a_n_delta(a_n_delta),
    d_n(d_n), d_n_delta(d_n_delta),
    f0_scaleto(f0_scaleto),
    cellBase(cellBase) { initializeBase(); };

  const double a_n;       //Average iris aperture / lambda (normalized aperture)
  const double a_n_delta; //Normalized iris aperture difference first-last

  const double d_n;       //Average iris thickness / cell period h (normalized thickness)
  const double d_n_delta; //Normalized iris thickness difference first-last

  const double f0_scaleto;//Frequency to scale the structure to [GHz]. Set to <=0.0 to disable scaling (i.e. use the scaling from cellBase).

  virtual void createCells();

 private:
  virtual void writeProfileFile_header(std::ofstream& ofile) const;

  // Pointer to the cellBase, shared by all instances
  // Note: For paralellization it might be nice to un-share this
  // (depends on the CellBase implementation's thread-safeness)
  CellBase* cellBase;
};



//The three cells designed for IPAC'12 paper (comparing results!)
class AccelStructure_CLIC502 : public AccelStructure {
 public:
  AccelStructure_CLIC502(int N, double f0_scaleto = 11.9942) :
    AccelStructure(N), f0_scaleto(f0_scaleto) { initializeBase(); };
  virtual void createCells();

  const double f0_scaleto; // Frequency to scale the structure to [GHz]

 private:
  virtual void writeProfileFile_header(std::ofstream& ofile) const;
};

//TD24_R05 or ordinary TD24 structure (2nd level design)
class AccelStructure_CLICG : public AccelStructure {
 public:
  AccelStructure_CLICG(int N, bool isR05=true, double f0_scaleto = 11.9942) :
    AccelStructure(N), isR05(isR05), f0_scaleto(f0_scaleto) { initializeBase(); };
  virtual void createCells();

  const bool isR05;
  const double f0_scaleto;

 private:
  virtual void writeProfileFile_header(std::ofstream& ofile) const;
};

//General AccelStructure object, which is directly defined by three cells.
// The cells given as input arguments are copied when creating the class.
class AccelStructure_general : public AccelStructure {
 public:
  AccelStructure_general(int N,
                         const CellParams& cellFirst_in, const CellParams& cellMid_in, const CellParams& cellLast_in,
                         const char* const headerLine = "") :
    AccelStructure(N), headerline(headerLine) {
    cellFirst_copy = CellParams(cellFirst_in);
    cellMid_copy   = CellParams(cellMid_in);
    cellLast_copy  = CellParams(cellLast_in);
    initializeBase();
  };
  virtual void createCells();

  //Creates a new AccelStructure_general by copying an already existing structure (generic type).
  static AccelStructure_general copy_structure(AccelStructure &source, const char* const headerLine="");

  //Creates a new AccelStructure_general by copying an already existing AccelStructure_general
  // This was needed for Swig not to crash on copy structure
  // (seems like the implicit copy constructor gets called a few times)
    AccelStructure_general(const AccelStructure_general& source) :
    AccelStructure(source.N), headerline(source.headerline) {
    cellFirst_copy = CellParams(source.cellFirst_copy);
    cellMid_copy   = CellParams(source.cellMid_copy);
    cellLast_copy  = CellParams(source.cellLast_copy);
    initializeBase();
    //TODO: Also calculate integrals and such?
    //      Or handle this correctly in baseclass copy constructor and call that?
  }
  //TODO: Add explicit copy constructors everywhere?
  // otherwise we ended up with a double cell prune
  // (has-been-freed detection failed because copy constructor cloned the pointers but not the heap objects)

 private:
  virtual void writeProfileFile_header(std::ofstream& ofile) const;

  CellParams cellFirst_copy;
  CellParams cellMid_copy;
  CellParams cellLast_copy;
  std::string headerline;
};

#endif
