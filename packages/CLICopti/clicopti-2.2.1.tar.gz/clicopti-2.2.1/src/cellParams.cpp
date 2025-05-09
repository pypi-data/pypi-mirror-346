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

#include "cellParams.h"
#include "constants.h"

#include <sstream>
#include <string>
#include <limits>
#include <cmath>

using namespace std;

CellParams Cell_TD_30GHz_v1_fileParse(string& line) {
  istringstream ss(line);
  //TODO: Make safer against format errors
  double a_n;  ss >> a_n;
  double d_n;  ss >> d_n;
  double psi;  ss >> psi;
  double Q;    ss >> Q;
  double vg;   ss >> vg;
  double rQ;   ss >> rQ;
  double Es;   ss >> Es;
  double Hs;   ss >> Hs;
  double f1mn; ss >> f1mn;
  double Q1mn; ss >> Q1mn;
  double A1mn; ss >> A1mn;

  const double lambda = Constants::speed_of_light/29.985e9; //wavelength of base frequency
  const double nan = numeric_limits<double>::quiet_NaN();

  const double sigma_z = 0.6e-3; //wake driving bunch length [m]
  //Scale to zero bunch length at reference frequency f1mn
  const double wakeAmplScale = exp(pow(2*M_PI*(f1mn*1e9)*sigma_z/Constants::speed_of_light,2)/2.0);

  CellParams ret =  {
    (psi/360.0) * lambda, //h
    a_n * lambda, //a
    d_n, a_n,
    29.985, //f0 [GHz]
    psi, Q, vg, rQ,
    Es, Hs,
    nan, //Sc
    f1mn, Q1mn, A1mn*wakeAmplScale
  };
  return ret;
}

CellParams Cell_TD_12GHz_v1_fileParse(string& line) {
  istringstream ss(line);
  //TODO: Make safer against format errors
  double a_n;  ss >> a_n;
  double d_n;  ss >> d_n;
  double psi;  ss >> psi;
  double f0;   ss >> f0;
  double Q;    ss >> Q;
  double vg;   ss >> vg;
  double rQ;   ss >> rQ; rQ*=1e3;
  double Es;   ss >> Es;
  double Sc;   ss >> Sc;
  double Hs;   ss >> Hs;
  double f1mn; ss >> f1mn;
  double Q1mn; ss >> Q1mn;
  double A1mn; ss >> A1mn;

  const double lambda = Constants::speed_of_light/11.99420e9; //wavelength of base frequency

  CellParams ret =  {
    (psi/360.0) * lambda, //h
    a_n * lambda, //a
    d_n, a_n,
    f0,
    psi, Q, vg, rQ,
    Es, Hs, Sc,
    f1mn, Q1mn, A1mn
  };
  return ret;
}

ostream& operator<< (std::ostream &out, const CellParams& cell) {
  out << "h="
      << cell.h << "[m], a="
      << cell.a << "[m], d_n="
      << cell.d_n << ", a_n="
      << cell.a_n << ", f0="
      << cell.f0  << "[GHz], psi="
      << cell.psi << "[deg], Q="
      << cell.Q   << ", vg="
      << cell.vg  << "[%c], rQ="
      << cell.rQ  << "[linacOhm/m], Es="
      << cell.Es  << ", Hs="
      << cell.Hs  << "[mA/V], Sc="
      << cell.Sc  << "[mA/V], f1mn="
      << cell.f1mn << "[GHz], Q1mn="
      << cell.Q1mn << ", A1mn="
      << cell.A1mn << "[V/pC/m/mm]";
  return out;
}

CellParams operator*(const CellParams& lhs, const double rhs) {
  CellParams ret = {lhs.h*rhs,
                    lhs.a*rhs,
                    lhs.d_n*rhs,
                    lhs.a_n*rhs,
                    lhs.f0*rhs,
                    lhs.psi*rhs,
                    lhs.Q*rhs,
                    lhs.vg*rhs,
                    lhs.rQ*rhs,
                    lhs.Es*rhs,
                    lhs.Hs*rhs,
                    lhs.Sc*rhs,
                    lhs.f1mn*rhs,
                    lhs.Q1mn*rhs,
                    lhs.A1mn*rhs};
  return ret;
}

CellParams operator+(const CellParams& lhs, const CellParams& rhs) {
  CellParams ret = { lhs.h+rhs.h,
                     lhs.a+rhs.a,
                     lhs.d_n+rhs.d_n,
                     lhs.a_n+rhs.a_n,
                     lhs.f0+rhs.f0,
                     lhs.psi+rhs.psi,
                     lhs.Q+rhs.Q,
                     lhs.vg+rhs.vg,
                     lhs.rQ+rhs.rQ,
                     lhs.Es+rhs.Es,
                     lhs.Hs+rhs.Hs,
                     lhs.Sc+rhs.Sc,
                     lhs.f1mn+rhs.f1mn,
                     lhs.Q1mn+rhs.Q1mn,
                     lhs.A1mn+rhs.A1mn
  };
  return ret;
}

void scaleCell(CellParams& c, double f0_new, int scalingLevel) {
  if (scalingLevel == -1) return; //Level -1: Do nothing

  double f0 = c.f0;
  c.f0 = f0_new;
  if (scalingLevel == 0) return; //Level   0: Set the frequency

  double ff = f0_new/f0;
  double f2 = sqrt(ff);
  double f3 = ff*ff*ff;

  //RF parameters
  c.Q  /= f2;
  c.rQ *= ff;
  c.f1mn *= ff;
  c.A1mn *= f3;
  if (scalingLevel == 1) return; //Level   1: Also scale RF parameters

  //Geom parameters scales with lambda, which scales with 1/ff
  c.a /= ff;
  if (scalingLevel == 2) return; //Level   2: Also scale a

  c.h /= ff;
  if (scalingLevel == 3) return; //Level   3: Scale everything

  stringstream ss;
  ss << "Illegal scalingLevel setting :'" << scalingLevel << "' - must be one of {0,1,2,3}";
  throw CellParamsError(ss.str());
}

CellParams CellParams_copy(CellParams& c) {
  CellParams cr = CellParams(c);
  return cr;
}
