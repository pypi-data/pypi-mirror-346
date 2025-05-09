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

#ifndef CONSTANTS_H
#define CONSTANTS_H

#include <cmath> //Gets M_PI
#ifndef M_PI
#define M_PI 3.141592653589793116
#endif

#define MUTE_PROGRAM //Not defining this flag makes the program print less information. Defining it makes it more muted, only printing critical error messages leading to an exit().

namespace Constants {
  const double speed_of_light = 299792458; // [m/s]
  const double mu0 = 4e-7*M_PI; // [H/m] magnetic permeability
  const double electron_charge = 1.60217646e-19; //[C]
};

#endif
