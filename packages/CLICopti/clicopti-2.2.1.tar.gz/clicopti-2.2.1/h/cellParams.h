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

#ifndef CELL_H
#define CELL_H

#include <cstddef>

#include <vector>
#include <iostream>

/** Description of the parameters of a given cell or point along the z axis.
 *  All parameters are doubles, note that some of the parameters
 *  may be set to NaN if not valid for the given cell
 */
struct CellParams {
  //Geometry
  double h;    //!< Cell length [m]
  double a;    //!< Iris aperture [m]

  double d_n;  //!< Normalized iris thickness / h
  double a_n;  //!< Normalized iris aperture a/lambda

  //Main mode
  double f0;   //!< Frequency [GHz] of main mode
  double psi;  //!< Phase advance [deg] of main mode

  double Q;    //!< Q-factor of main mode
  double vg;   //!< Group velocity [%c] of main mode
  double rQ;   //!< r/Q [linacOhm / m] of main mode

  double Es;   //!< Esurf/Eacc of main mode
  double Hs;   //!< Hsurf/Eacc [mA/V] of main mode
  double Sc;   //!< Sc/Eacc^2 [mA/V] of main mode

  //Wakefield 1st transverse mode
  double f1mn; //!< Frequency [GHz] of wakefield 1st transverse mode
  double Q1mn; //!< Q-factor of wakefield 1st transverse mode
  double A1mn; //!< Amplitude [V/pC/mm/m] of wakefield 1st transverse mode
};

//Offsets
const size_t off_h = offsetof(struct CellParams, h);
const size_t off_a = offsetof(struct CellParams, a);
const size_t off_d_n = offsetof(struct CellParams, d_n);
const size_t off_a_n = offsetof(struct CellParams, a_n);
const size_t off_f0 = offsetof(struct CellParams, f0);
const size_t off_psi = offsetof(struct CellParams, psi);
const size_t off_Q = offsetof(struct CellParams, Q);
const size_t off_vg = offsetof(struct CellParams, vg);
const size_t off_rQ = offsetof(struct CellParams, rQ);
const size_t off_Es = offsetof(struct CellParams, Es);
const size_t off_Hs = offsetof(struct CellParams, Hs);
const size_t off_Sc = offsetof(struct CellParams, Sc);
const size_t off_f1mn = offsetof(struct CellParams, f1mn);
const size_t off_Q1mn = offsetof(struct CellParams, Q1mn);
const size_t off_A1mn = offsetof(struct CellParams, A1mn);


// Returns the content of one field in a cell given the offset.

inline double getByOffset(const CellParams& cell, const size_t off) {
  return *( (double*) ( (char*)(&cell) + off ) );
};
inline double getByOffset(const CellParams* const cell, const size_t off) {
  return *( (double*) ( (char*)(cell) + off ) );
};

//Output
std::ostream& operator<< (std::ostream &out, const CellParams& cell);

//Initializers
CellParams Cell_TD_30GHz_v1_fileParse(std::string& line);
CellParams Cell_TD_12GHz_v1_fileParse(std::string& line);

//Math operators
CellParams operator*(const CellParams& lhs, const double rhs);
inline CellParams operator*(const double lhs, const CellParams& rhs) {return rhs*lhs;};
//inline CellParams operator*=(const CellParams lhs, const double& rhs) {return lhs*rhs;};
inline CellParams operator/(const CellParams& lhs, const double rhs) {return lhs*(1.0/rhs);};
//inline CellParams operator/=(const CellParams& lhs, const double rhs) {return lhs/rhs;};
CellParams operator+(const CellParams& lhs, const CellParams& rhs);
//inline CellParams operator+=(const CellParams& lhs, const CellParams& rhs) {return lhs+rhs;};
inline CellParams operator-(const CellParams& lhs, const CellParams& rhs) {return lhs+((-1)*rhs);};
//inline CellParams operator-=(const CellParams& lhs, const CellParams& rhs) {return lhs-rhs;};

//Cell scaling
void scaleCell(CellParams& c, double f0, int scalingLevel=3);

//Effectively a copy constructor
CellParams CellParams_copy(CellParams& c);

/* Exceptions */

// basically just renaming logic_error
// Inspired by https://stackoverflow.com/a/8152888
class CellParamsError : public std::logic_error {
  public:
  /** Constructor (C strings).
     *  @param message C-style string error message.
     *                 The string contents are copied upon construction.
     *                 Hence, responsibility for deleting the char* lies
     *                 with the caller.
     */
    explicit CellParamsError(const char* message)
        : std::logic_error(message) {}

    /** Constructor (C++ STL strings).
     *  @param message The error message.
     */
    explicit CellParamsError(const std::string& message)
        : std::logic_error(message) {}
};

#endif
