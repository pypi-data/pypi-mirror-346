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

#ifndef CELLBASE_H
#define CELLBASE_H

#include "cellParams.h"

#include <vector>
#include <string>

/** @class CellBase
 *  This class loads the cell database file and handles data for individual cells.
 *   It is meant to be instanciated once via one of its daughter classes,
 *   and then used to create several cells via interpolation.
 *   The interpolation algorithms are implemented in the daughter classes.
 */
class CellBase {
 public:
  /** Initialize the CellBase class by parsing the specified file and make the interpolation.
    * This constructor is meant to be called by the daughter class constructor.
    * @param fname      The file name of the database file to load
    * @param offsets    Array of byte offsets into CellParams.
    */
  CellBase(std::string fname, std::vector<size_t> offsets);
  /** Legacy constructor, same meaning.
    * @param fname      The file name of the database file to load
    * @param numIndices Length of the ``offsets`` array
    * @param offsets    Array of byte offsets into CellParams.
    */
   CellBase(const char* const fname, unsigned int numIndices, std::vector<size_t> offsets);

  virtual ~CellBase();

  //! What type of cell are we using?
  enum CellType {
    UNDEFINED,   //!< CellParams type not set *default value)
    TD_30GHz_v1, //!< CellParams loaded by `Cell_TD_30GHz_v1_fileParse()`
    TD_12GHz_v1  //!< CallParams loaded by `Cell_TD_12GHz_v1_fileParse()`
  };
  CellType cellType; //!< Use TD_30GHz_v1 or TD_12GHz_v1?
  
  //! Sorting of the input file
  enum CellSorting {
    GRID, //!< Cell database has points on a regular rectangular grid
    FREE  //!< Free-form cell database (default value)
  };
  CellSorting cellSorting; //!< Use GRID or FREE?


  /** Get an interpolated cell (method implementation dependent).
    * 
    * @param point The point at which to evaluate the interpolation.
    * The passed array should have length numIndices,
    * and the meaning of each element is specified by `offsets`,
    * which is passed to the class constructor
    *
    */
  virtual CellParams getCellInterpolated(const std::vector<double>& point) = 0;

  //! Number of "index fields"
  const unsigned int numIndices;
  /** Byte-offsets into cells specifying the indexFields
    *  Should have length numIndices
    */
  std::vector<size_t> offsets;

 protected:
  //! List of precalculated cells
  std::vector<CellParams> cellList;

  //! Used by constructor to extract keyword stuff
  std::string findKeyword(std::string line, std::string keyword);
  //! Extra keywords, read and parsed by daughter constructor
  std::vector<std::string> childkeys;
};

/** @class CellBase_grid
  * Builds a grid of cells, any depth.
  * How it works: In the input file, CELLSORTING must be ``GRID``.
  * Also needs the CHILDKEY ``GRIDSORT``,
  * with "d" positive integers describing the number of entries in every dimension,
  * d being the number of dimensions.
  * This is sorted such that the first integer corresponds to the outer sorting,
  * second integer one step "below" etc.
  *
  * Internally, the ``gridsort`` array stores the data from GRIDSORT,
  * and the 2D-array gridlabels stores the values on the axis if you where to plot is as d-cube,
  * first index being which dimension, second index being the number along this dimension.
  * It is checked that the data is increasing monotonically along every dimension.
  *
  */
class CellBase_grid : public CellBase {
 public:
  CellBase_grid(std::string fname,
                std::vector<size_t> offsets );
  CellBase_grid(const char* const fname,
                unsigned int numIndices,
                std::vector<size_t> offsets );
  virtual ~CellBase_grid();

  inline CellParams getCellGrid(const std::vector<size_t>& gridIdx) const {return cellList[getIdx(gridIdx)];};
  void printGrid() const;

  //! Get the min and max allowable label for a given dimension
  inline double getMinLabel(size_t dimension) {
    if (dimension >= numIndices) {
      throw std::out_of_range("dimension >= numIndices");
    }
    return gridMin[dimension];
  };
  inline double getMaxLabel(size_t dimension) {
    if (dimension >= numIndices) {
      throw std::out_of_range("dimension >= numIndices");
    }
    return gridMax[dimension];
  };

  //! Get number of points in a given direction
  inline size_t getGridsort(size_t dimension) {
    if (dimension >= numIndices) {
      throw std::out_of_range("dimension >= numIndices");
    }
    return gridsort[dimension];
  };
  //! Get the points in a given direction
  inline std::vector<double> getGridlabels(size_t dimension) {
    if (dimension >= numIndices) {
      throw std::out_of_range("dimension >= numIndices");
    }
    std::vector<double> ret(gridsort[dimension]);
    for (size_t i = 0; i < gridsort[dimension]; i++) {
      ret[i] = gridlabels[dimension][i];
    }
    return ret;
  }


 protected:
  size_t*  gridsort;   //!< Gridsort offsets (how many in each direction)
  double** gridlabels; //!< What are the points on the ``numIndices`` axes

  double* gridMin; double* gridMax; //Max and min bounds for interpolation

  //Convert a set of grid indices into a "global" index
  size_t getIdx(const std::vector<size_t>& gridIdxs) const;
  //Gets the "label" variable #dim for a given cell
  inline double getDimension(const CellParams& cell, const size_t dim) {
    return getByOffset(cell, offsets[dim]);
  }
};

/** @class CellBase_linearInterpolation
 * On top of ``CellBase_gridSort``, do linear interpolation between the points.
 */
class CellBase_linearInterpolation : public CellBase_grid {
 public:
  CellBase_linearInterpolation(std::string fname, std::vector<size_t> offsets) : CellBase_grid(fname,offsets) {};
  //Legacy constructor (forward numIndices for checking)
  CellBase_linearInterpolation(const char* const fname,
                              unsigned int numIndices,
                              std::vector<size_t> offsets) :
    CellBase_grid(fname,numIndices,offsets) {};

  //Given some point, interpolate from nearest neighbours
  virtual CellParams getCellInterpolated(const std::vector<double>& point);
 private:
  //Recursive function to make the interpolation
  CellParams recursiveInterpolator(std::vector<size_t>& I, size_t iLen, const std::vector<double>& f) const;
};

/** @class CellBase_linearInterpolation_freqScaling
 * This is a wrapper of ``CellBase_linearInterpolation``,
 * which also scales the cells to a given frequency ``f0`` [GHz].
 *
 * Note: The output is scaled, however if ``offsets`` include frequency-dependent data,
 * the input has to be in the original scaling.
*/
class CellBase_linearInterpolation_freqScaling : public CellBase_linearInterpolation {
 public:
  CellBase_linearInterpolation_freqScaling(std::string fname,
                                           std::vector<size_t> offsets,
                                           double f0)
    : CellBase_linearInterpolation(fname, offsets), f0(f0) { };
  //Legacy constructor signature (forward numIndices for checking)
  CellBase_linearInterpolation_freqScaling(const char* fname,
                                           unsigned int numIndices,
                                           std::vector<size_t> offsets,
                                           double f0)
    : CellBase_linearInterpolation(fname, numIndices, offsets), f0(f0) { };
  //Get an interpolated and scaled cell
  virtual CellParams getCellInterpolated(const std::vector<double>& point);
  inline void scaleCell(CellParams& c) {
    //Redirect to the global scaleCell()
    ::scaleCell(c,this->f0,3);
  };

  inline double getF0() const { return f0; };

 private:
  double f0;

};

/** @class CellBase_compat
 * Implements Alexej's old algorithm for generating cells:
 *
 * 1. Quad-interpolate cell parameters for ``a_n``, ``d_n``
 * 2. If neccessary, quad-interpolate for the phase advance
 *    (EXCEPT we don't have the data for this -- need 3 phase advances,
 *    have only 120 and 150 degrees, not 90/110/130 as seems to have been used --
 *    Thus I'm only implementing linear interpolation here.)
 *    ALSO, if ``havePhaseAdvance`` = false, then assume there are no phase advance information.
 * 3. Scale to frequency f0[GHz] according to ``scalingLevel`` setting:
 * 
 *    ``scalingLevel`` = -1
 *      Ignore `f0`, no scaling.
 *    ``scalingLevel`` = 0
 *      Set the cell's frequency to `f0` without changing anything else.
 *    ``scalingLevel`` = 1
 *      Scale RF parameters and wakefield, but not geometry.
 *    ``scalingLevel`` = 2
 *      Scale RF parameters, wakefield, and geometry EXCEPT ``h``.
 *    ``scalingLevel`` = 3
 *      Scale everything.
 *    
 * Note that this class is mostly assuming the file ``TD_30GHz.dat`` to be used as input.
 */
class CellBase_compat : public CellBase_grid {
 public:
 CellBase_compat(std::string fname, double f0=29.985, bool havePhaseAdvance=true, int scalingLevel=3)
   : CellBase_grid(fname, offsets_initializer(havePhaseAdvance)),
    f0(f0), havePhaseAdvance(havePhaseAdvance), scalingLevel(scalingLevel) { };
  virtual ~CellBase_compat() {
  };

  virtual CellParams getCellInterpolated(const std::vector<double>& point);
  //Scale the input cell
  inline void scaleCell(CellParams& c) {
    //Redirect to the global scaleCell()
    ::scaleCell(c,this->f0,this->scalingLevel);
  };

  inline double getF0() const { return f0; };
  inline int getScalingLevel() const { return scalingLevel; };

 private:
  double f0;
  bool   havePhaseAdvance;
  int    scalingLevel;

  inline static std::vector<size_t> offsets_initializer(bool havePhaseAdvance) {
    std::vector<size_t> offsets;
    if (havePhaseAdvance == true) {
      offsets.push_back( offsetof(struct CellParams, psi) );
      offsets.push_back( offsetof(struct CellParams, a_n) );
      offsets.push_back( offsetof(struct CellParams, d_n) );
    }
    else {
      offsets.push_back( offsetof(struct CellParams, a_n) );
      offsets.push_back( offsetof(struct CellParams, d_n) );
    }
    return offsets;
  };

  //Quad-interpolate on an/dn grid at given psiDex. If havePhaseAdvance then expects psiDex = -1.
  CellParams interpolate_an_dn(int psiDex, double a_n, double d_n) const;
  //Interpolate to x in one dimension, using data from cells[] placed at posions xmn[]
  CellParams interpolate_quad(CellParams cells[], double xmn[], double x) const;
};

/* Exceptions */

// basically just renaming logic_error
// Inspired by https://stackoverflow.com/a/8152888
class CellBaseError : public std::logic_error {
  public:
  /** Constructor (C strings).
     *  @param message C-style string error message.
     *                 The string contents are copied upon construction.
     *                 Hence, responsibility for deleting the char* lies
     *                 with the caller.
     */
    explicit CellBaseError(const char* message)
        : std::logic_error(message) {}

    /** Constructor (C++ STL strings).
     *  @param message The error message.
     */
    explicit CellBaseError(const std::string& message)
        : std::logic_error(message) {}
};

#endif
