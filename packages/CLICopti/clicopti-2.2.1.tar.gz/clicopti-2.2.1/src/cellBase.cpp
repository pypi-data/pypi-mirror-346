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

#include "cellBase.h"

#include <fstream>
#include <sstream>
#include <stdexcept>
#include <cstdlib>
#include <cmath>

#include <sstream>
#include <string>

#include <vector>

//#define CHATTY_PROGRAM 1

using namespace std;

//Legacy constructor
CellBase::CellBase(const char* const fname, unsigned int numIndices, vector<size_t> offsets) : CellBase(string(fname),offsets) {
  if (offsets.size() != numIndices) {
    stringstream ss;
    ss << "offsets.size() = " << offsets.size() << " != "
       << "numIndices = " << numIndices << endl;
    throw CellBaseError(ss.str());
  }
}

CellBase::CellBase(string fname,
                   vector<size_t> offsets)
  : numIndices(offsets.size()), offsets(offsets) {
  
  string formatcode = "";
  string sorting = "";

  // Set default values
  this->cellSorting = FREE;
  this->cellType    = UNDEFINED;

  ifstream loadFrom;
  loadFrom.open(fname);
  if (!loadFrom.is_open()) {
    stringstream ss;
    ss << "Couldn't open '" << fname << "'";
    throw CellBaseError(ss.str());
  }

  while(loadFrom.good()) {
    string line;
    getline(loadFrom,line);
    //cout << line << endl;

    //Skip comment & blank lines
    bool isComment = false;
    bool isBlank = true;
    for (size_t i = 0; i < line.size(); i++) {
      char nc = line[i];
      if (nc == ' ' || nc == '\t') {
        continue;
      }
      else if (line [i] == '#') {
        isBlank = false;
        isComment = true;
        break;
      }
      else {
        isBlank = false;
      }
    } //END for
    if (isComment || isBlank) {
      //cout << "isComment=" << isComment << " isBlank=" << isBlank << endl;
      continue;
    };

    //Look for FORMATCODE
    size_t fcidx = line.find("FORMATCODE");
    if (fcidx != string::npos) {
      if (formatcode.compare("") != 0) {
        throw CellBaseError("FORMATCODE set twice in database file");
      }

      formatcode = findKeyword(line, "FORMATCODE");
#ifdef CHATTY_PROGRAM
      cout << "FORMATCODE = '" << formatcode << "'" << endl;
#endif

      if (formatcode.compare("TD_30GHz_v1") == 0) {
        this->cellType = TD_30GHz_v1;
      }
      else if (formatcode.compare("TD_12GHz_v1") == 0) {
        this->cellType = TD_12GHz_v1;
      }
      else {
        stringstream ss;
        ss << "FORMATCODE '" << formatcode << "' not recognized in database file";
        throw CellBaseError(ss.str());
      }
      //Finished processing line
      continue;
    }

    //Look for CELLSORTING
    fcidx = line.find("CELLSORTING");
    if (fcidx != string::npos) {
      if (sorting.compare("") != 0) {
        throw CellBaseError("CELLSORTING set twice in database file");
      }

      sorting = findKeyword(line, "CELLSORTING");
#ifdef CHATTY_PROGRAM
      cout << "CELLSORTING = '" << sorting << "'" << endl;
#endif

      if (sorting.compare("GRID") == 0) {
        cellSorting = GRID;
      }
      else if (sorting.compare("FREE") == 0) {
        cellSorting = FREE;
      }
      else {
        stringstream ss;
        ss << "CELLCOSRTING '" << cellSorting << "' not recognized in database file";
        throw CellBaseError(ss.str());
      }
      //Finished processing line
      continue;
    }

    //Look for other keywords, to be parsed in child constructor
    if (line.find("CHILDKEY") != string::npos) {
      childkeys.push_back(findKeyword(line, "CHILDKEY"));
#ifdef CHATTY_PROGRAM
      cout << "CHILDKEY[" << childkeys.size()-1 << "]: "
           << childkeys[childkeys.size()-1] << endl;
#endif
      continue;
    }

    //Parse data lines and load cells
    switch ( cellType ) {
    case TD_30GHz_v1:
      cellList.push_back( Cell_TD_30GHz_v1_fileParse(line) );
      //cout << cellList[cellList.size()-1] << endl;
      break;
    case TD_12GHz_v1:
      cellList.push_back( Cell_TD_12GHz_v1_fileParse(line) );
      //cout << cellList[cellList.size()-1] << endl;
      break;
    case UNDEFINED: {
      //FORMATCODE is expected to be present before any cells are loaded
      stringstream ss;
      ss << "cellType / FORMATCODE must be set by database file before loading; possibly database file '" << fname << "' corrupt or incomplete";
      throw CellBaseError(ss.str());
      break;
    }
    default: {
      stringstream ss;
      ss << "cellType / FORMATCODE not found when loading cells from database file; possibly database file '" << fname << "' corrupt, or internal error in CLICopti";
      throw CellBaseError(ss.str());
    }
    }

  }//END while

  loadFrom.close();
}
string CellBase::findKeyword(string line, string keyword) {
  //cout << "findKeyword: line = '" << line << "', keyword = '" << keyword << "'" << endl;
  size_t fcidx = line.find(keyword);
  //cout << "findKeyword: fcidx=" << fcidx << endl;
  string data = "";
  if (fcidx == string::npos) {
    stringstream ss;
    ss << "Keyword '" << keyword << "' not found in line '" << line << "'";
    throw CellBaseError(ss.str());
  }

  for (size_t i = 0; i < fcidx; i++) {
    if (line[i] == ' ' || line[i] == '\t') continue;
    stringstream ss;
    ss << "found character in front of keyword '" << keyword << "' in line '" << line << "'";
    throw CellBaseError(ss.str());
  }
  try {
    data = line.substr(fcidx+keyword.length());
    //cout << "findKeyword: data ='" << data << "'" << endl;
  }
  catch (const out_of_range& oor) {
    stringstream ss;
    ss << "Out of range error when parsing keyword '" << keyword << "':" << oor.what();
    throw CellBaseError(ss.str());
  }
  //Remove whitespace at beginning
  while(data.size() > 0 and (data[0] == ' ' || data[0] == '\t')) {
    data = data.substr(1);
  }
  //Remove trailing whitespace
  while(data.size() > 0 and
        (data[data.size()-1] == ' ' ||
         data[data.size()-1] == '\t') ) {
    data = data.substr(0,data.size()-1);
  }

  return data;
}

CellBase::~CellBase() {
  cellList.clear();
}

///////////// IMPLEMENTATION OF CellBase_grid /////////////////////////////
CellBase_grid::CellBase_grid(const char* const fname, unsigned int numIndices, vector<size_t> offsets) : CellBase_grid(string(fname),offsets) {
  if (offsets.size() != numIndices) {
    stringstream ss;
    ss << "offsets.size() = " << offsets.size() << " != "
       << "numIndices = " << numIndices << endl;
    throw CellBaseError(ss.str());
  }
}
CellBase_grid::CellBase_grid(string fname, vector<size_t> offsets)
  : CellBase(fname, offsets) {
  if ( cellSorting != GRID ) {
    throw (CellBaseError("CellBase_grid can only work with GRID cellsorting"));
  }

  //Layout a grid
  gridsort   = new size_t [numIndices];
  gridlabels = new double*[numIndices];
  gridMin    = new double [numIndices];
  gridMax    = new double [numIndices];
  if(childkeys.size() == 0) {
    throw (CellBaseError("CellBase_grid expected at least one CHILDKEY (GRIDSORT), got 0."));
  }
  istringstream ss(findKeyword(childkeys[0], "GRIDSORT"));
  string s = findKeyword(childkeys[0], "GRIDSORT");
  size_t sizecheck = 1;

  size_t d = 0;
  size_t pos_start = 0;
  size_t pos_end = 0;
  do {
    if (d >= numIndices) {
      stringstream se;
      se << "Error when reading CHILDKEY GRIDSORT, too many data fields compared to numIndices = " << numIndices << ". "
         << "Arguments and database file do not match!";
      throw CellBaseError(se.str());
    }
    
    pos_end = s.find(" ", pos_start);
    std::string s2 = s.substr(pos_start, pos_end-pos_start);

    try {
      gridsort[d] = size_t( std::stoi(s2) );
    }
    catch (const std::invalid_argument& ia) {
      stringstream se;
      se << "Error while parsing number '" << s2 << "'";
      se << " from CHILDKEY GRIDSORT '" << s << "'";
      se << " error='" << ia.what() << "'";
      throw CellBaseError(se.str());
    }

    sizecheck *= gridsort[d];

    gridlabels[d] = new double[gridsort[d]];

    pos_start = pos_end+1;
    d++;
  } while (pos_end != std::string::npos);
  
  if (d != numIndices) {
    stringstream se;
    se << "Error when reading CHILDKEY GRIDSORT, expected to read numIndices = " << numIndices
       << " data fields but got " << d << " fields";
    throw CellBaseError(se.str());
  }

  if (sizecheck != cellList.size()) {
    stringstream ss;
    ss << "sizecheck=" << sizecheck << " != number of cells=" << cellList.size();
    throw (CellBaseError(ss.str()));
  }
  // Fill gridlabels & check that they are monotonically increasing with index
  for (size_t d = 0; d < numIndices; d++) {
    vector<size_t> idxs(numIndices, 0);

    gridMin[d] = getDimension(cellList[0], d);
    idxs[d] = gridsort[d]-1;
    gridMax[d] = getDimension(cellList[getIdx(idxs)], d);
    idxs[d] = 0;

    double monocheck = getDimension(cellList[0], d);
    for (size_t i=0; i < gridsort[d]; i++) {
      idxs[d] = i;
      gridlabels[d][i] = getDimension(cellList[getIdx(idxs)], d);
      if (gridlabels[d][i] < monocheck) {
        throw (CellBaseError("Error from monocheck; gridlabels are not monotonically increasing?"));
      }
    }
  }
}

void CellBase_grid::printGrid() const {
  vector<size_t> idx(numIndices, 0);
  for (size_t i = 0; i < cellList.size(); i++) {
    //Print the current indices
    cout << "[ ";
    for (size_t d = 0; d < numIndices; d++) {
      cout << idx[d] << " ";
    }
    cout << "] -> ";

    //Compute the cellID for the current indices (the index into the global cellList)
    size_t cellID = getIdx(idx);
    cout << cellID << endl;
    if (cellID != i) {
      //This is really a *really* complicated way of iterating over i :)
      stringstream ss;
      ss << "Internal error, cellID="<<cellID<<", i="<<i;
      throw CellBaseError(ss.str());
    }

    //Print.
    for (size_t d = 0; d < numIndices; d++) {
      //cout << *( (double*) ( (char*) (&(cellList[cellID])) + offsets[d] ) ) << " ";
      cout << getByOffset(cellList[cellID], offsets[d]) << " ";
    }
    cout << endl;
    cout << cellList[cellID] << endl;
    cout << endl;

    idx[numIndices-1]++; //Increase fastest counter by 1
    for (size_t d = 0; d < numIndices-1; d++) { //Rollover
      if (idx[numIndices-1-d] >= gridsort[numIndices-1-d]) {
        idx[numIndices-1-d] = 0;
        idx[numIndices-2-d]++;
      }
    }
  }
}

size_t CellBase_grid::getIdx(const vector<size_t>& gridIdxs) const {

  // cout << "gridIdxs = ";
  // for (size_t d = 0; d < numIndices; d++) {
  //   cout << gridIdxs[d] << " ";
  // }
  // cout << endl;

  size_t globalIdx = 0;
  size_t steplen = 1;
  for (size_t d = 0; d < numIndices; d++) {
    //fastest counting digit (the last one) first
    if ((gridIdxs[numIndices-1-d] >= gridsort[numIndices-1-d]) ) {
      stringstream ss;
      ss << "Assumed that gridIdxs[numIndices-1-d] < gridsort[numIndices-1-d], this failed; "
         << "d = " << d << ", numIndices = " << numIndices
         << ", gridIdxs[numIndices-1-d] = " << gridIdxs[numIndices-1-d]
         << ", gridSort[numIndices-1-d] = " << gridsort[numIndices-1-d];
        throw CellBaseError(ss.str());
    }
    //assert( gridIdxs[numIndices-1-d] < gridsort[numIndices-1-d] );
    globalIdx += gridIdxs[numIndices-1-d]*steplen;
    steplen *= gridsort[numIndices-1-d];
  }
  if (globalIdx >= cellList.size()) {
    throw CellBaseError("globalIdx >= cellList.size()");
  }
  return globalIdx;
}

CellBase_grid::~CellBase_grid() {
  delete[] gridsort;
  for(size_t d =0; d < numIndices; d++) {
    delete[] gridlabels[d];
  }
  delete[] gridlabels;

  delete[] gridMin; delete[] gridMax;
}

///////////// IMPLEMENTATION OF CellBase_linearInterpolation /////////////////////////////

CellParams CellBase_linearInterpolation::getCellInterpolated(const vector<double>& point) {
  //Integer part: index just below this
  //Fractional part: weighting of point above it
  vector<double> normalizedIdx(numIndices);

  //Find neighbour points
  for (size_t d=0; d < numIndices; d++) {
    //First test that point[] is in range
    if(point[d] < gridlabels[d][0] || point[d] > gridlabels[d][gridsort[d]-1] ) {
      stringstream ss;
      ss << "Point outside grid: "
         << "point[d=" << d << "]=" << point[d]
         << ", gridlabels[d][:]: ";
      for (size_t i = 0; i < gridsort[d]; i++) {
        ss << gridlabels[d][i] << " ";
      }
      ss << "limits="<< gridlabels[d][0]<<","<<gridlabels[d][gridsort[d]-1];
      ss << ";\n";
      ss << "Check that you are looping inside the grid, that numIndices (now=" << numIndices
           << ") is correct, and correct formatting of input data 'point' or offsets.";
      throw CellBaseError(ss.str());

    }

    //normalizedIdx
    size_t i;
    for(i=0; i < gridsort[d]; i++) {
      if (gridlabels[d][i] <= point[d]) break;
    }
    if (i < gridsort[d]) {
      //normal case
      normalizedIdx[d] = ((double)i) + (point[d]-gridlabels[d][i])/(gridlabels[d][i+1]-gridlabels[d][i]);
    }
    else {
      normalizedIdx[d] = (size_t)i-1e-12;
    }
  }

  // cout << "normalizedIdx = ";
  // for (size_t d=0; d < numIndices; d++) {
  //   cout << normalizedIdx[d] << " ";
  // }
  // cout << endl;

  //Interpolate!
  vector<size_t> I(numIndices);
  vector<double> f(numIndices);
  for (size_t d = 0; d < numIndices; d++) {
    I[d] = (size_t) normalizedIdx[d];
    f[d] = normalizedIdx[d] - I[d];
  }
  // cout << "I = ";
  // for (size_t d=0; d < numIndices; d++) {
  //   cout << I[d] << " ";
  // }
  // cout << endl;
  // cout << "f = ";
  // for (size_t d=0; d < numIndices; d++) {
  //   cout << f[d] << " ";
  // }
  // cout << endl;

  //Total number of points to be tallied: 2^numIndices
  CellParams ret = recursiveInterpolator(I,0,f);
  return ret;
}

/**
 * As (in the 2D case) v_{\vec F} = f_1(f_2 v_{+,+} + (1-f_2)v_{+,-})
 *                                + (1-f_1)(f_2 v_{-,+} + (1-f_2)v_{-,-})
 *                                = f_1 v_{+,f_2} + (1-f_1) v_{-,f_2}
 * we can write the hyperlinear interpolation using a recursive function
 * v_{\pm_0, \pm_1, \ldots, F_{iLen}, F_{iLen+1}, \ldots F_{numIndices-1} },
 * where F_i = I_i + f_i for a given dimension i,
 * and I the index of the hyperplane which to do the interpolation
 * (represented by + or - relative to the original point),
 * while 0 <= f_i < 1 is the "remainder" in this dimension.
 */
CellParams CellBase_linearInterpolation::recursiveInterpolator(vector<size_t>& I, size_t iLen, const vector<double>& f) const {
  // string tabs = "";
  // for (size_t i =0; i < iLen; i++) tabs += "\t";
  // cout << tabs << "recursiveInterpolator called with:" << endl;
  // cout << tabs << "iLen = " << iLen << endl;
  // cout << tabs << "I = ";
  // for (size_t d=0; d < numIndices; d++) {
  //   cout << I[d] << " ";
  // }
  // cout << endl;
  // cout << tabs << "f = ";
  // for (size_t d=0; d < numIndices; d++) {
  //   cout << f[d] << " ";
  // }
  // cout << endl;

  //Edge checking
  for (size_t d = 0; d < numIndices; d++) {
    if (I[d] >= gridsort[d]) {
      // cout << tabs << "EMPTY!" << endl;
      return CellParams();
    };
  }
  if (iLen == numIndices) {
    CellParams ret = cellList[getIdx(I)];
    // cout << tabs << "Found: ";
    // cout << ret << endl;;
    // cout << ret.psi << " " << ret.a_n << " " << ret.d_n << endl;
    return ret;
  }
  else {
    //Value-initialized (all fields to 0) per C++ standard
    CellParams ret = CellParams();
    // cout << tabs << "(1-f) = " << (1-f[iLen]) << endl;
    ret = ret + (1-f[iLen])*recursiveInterpolator(I,iLen+1,f);
    //cout << tabs << "Ret = " << ret << endl;

    I[iLen]++;
    // cout << tabs << "f = " << f[iLen] << endl;
    ret = ret + f[iLen]*recursiveInterpolator(I,iLen+1,f);
    I[iLen]--; //Leave I untouched at return
    // cout << tabs << "Returning: ";
    // cout << ret << endl;
    // cout << ret.psi << " " << ret.a_n << " " << ret.d_n << endl;
    return ret;
  }
}

///////////// IMPLEMENTATION OF CellBase_linearInterpolation_freqScaling /////////////////////////////

CellParams CellBase_linearInterpolation_freqScaling::getCellInterpolated(const vector<double>& point) {
  //Get the basic cell
  CellParams ret = CellBase_linearInterpolation::getCellInterpolated(point);
  scaleCell(ret);
  return ret;
}

///////////// IMPLEMENTATION OF CellBase_compat /////////////////////////////

CellParams CellBase_compat::getCellInterpolated(const vector<double>& point) {
  double psi,a_n,d_n;
  int psiDex = -1;
  if (this->havePhaseAdvance) {
    psi = point[0];
    a_n = point[1];
    d_n = point[2];

    //Which gridIndex is this psi? If not found then -1
    for (size_t i = 0; i < gridsort[0]; i++) {
      if (gridlabels[0][i] == psi) {
        if (psiDex != -1) {
          throw CellBaseError("Internal error, got psiDex != -1?");
        }
        psiDex = (int)i;
        break;
      }
    }
  }
  else {
    psi = -1.0;
    a_n = point[0];
    d_n = point[1];
  }

  if ( (psiDex != -1 and this->havePhaseAdvance) or this->havePhaseAdvance==false ) {
    CellParams ret = interpolate_an_dn(psiDex, a_n, d_n);
    scaleCell(ret);
    return ret;
  }
  //Implicit else:
  //Linear interpolation in phase advance.
  if (gridsort[0] != 2) {
    throw CellBaseError("Got gridsort[0] != 2 but expected 2 psi points?");
  }
  if (psi <= 120 || psi >= 150) {
    throw CellBaseError("Expected psi in range (120,150)");
  }

  CellParams cell120 = interpolate_an_dn(0, a_n, d_n);
  CellParams cell150 = interpolate_an_dn(1, a_n, d_n);

  CellParams ret = cell120 + (cell150-cell120)*(psi-120.0)/(150.0-120.0);
  scaleCell(ret);
  return ret;
}

CellParams CellBase_compat::interpolate_an_dn(int psiDex, double a_n, double d_n) const {
  //Interpolate from a_n, d_n:
  if (psiDex != -1 and this->havePhaseAdvance==true){
    if (gridsort[1] != 5) {
      throw CellBaseError("Expected 5 a_n points");
    }
    if (a_n < gridlabels[1][0] || a_n > gridlabels[1][4]) {
      throw CellBaseError("a_n out of range");
    }
    if (gridsort[2] != 3) {
      throw CellBaseError("Expected 3 d_n points");
    }
    if (d_n < gridlabels[2][0] || d_n > gridlabels[2][2]) {
      throw CellBaseError("d_n out of range");
    }
  }
  else if (psiDex == -1 and this->havePhaseAdvance==false) {
    if (gridsort[0] != 5) {
      throw CellBaseError("Expected 5 a_n points");
    }
    //assert(a_n >= gridlabels[0][0] && a_n <= gridlabels[0][4]);
    if ((a_n < gridlabels[0][0] || a_n > gridlabels[0][4])) {
      stringstream ss;
      ss << "a_n = " << a_n << " should be in range ("
         << gridlabels[0][0] << ", " << gridlabels[0][4] << ")";
      throw CellBaseError(ss.str());
    }
    if (gridsort[1] != 3) {
      throw CellBaseError("Expected 3 d_n points");
    }
    if (d_n < gridlabels[1][0] || d_n > gridlabels[1][2]) {
      throw CellBaseError("d_n out of range");
    }
  }
  else {
    stringstream ss;
    ss << "psiDex and havePhaseAdvance mismatch, proably a BUG: ";
    ss << "psiDex = " << psiDex << ", havePhaseAdvance = " << (havePhaseAdvance?"True":"False");
    throw CellBaseError(ss.str());
  }
  // 1. for each value of a_n available, interpolate over d_n
  CellParams cells_dnreduced [5];
  if (this->havePhaseAdvance) {
    vector<size_t> tmpIdx1 = {size_t(psiDex),0,0};
    vector<size_t> tmpIdx2 = {size_t(psiDex),0,1};
    vector<size_t> tmpIdx3 = {size_t(psiDex),0,2};
    for (size_t i = 0; i < gridsort[1]; i++) { //a_n
      tmpIdx1[1]=i; tmpIdx2[1]=i; tmpIdx3[1]=i;
      CellParams cells[3] = {cellList[getIdx(tmpIdx1)],cellList[getIdx(tmpIdx2)],cellList[getIdx(tmpIdx3)]};
      double xmn[3] = {gridlabels[2][0],gridlabels[2][1],gridlabels[2][2]};
      cells_dnreduced[i] = interpolate_quad(cells, xmn, d_n);
    }
  }
  else {
    vector<size_t> tmpIdx1 = {0,0};
    vector<size_t> tmpIdx2 = {0,1};
    vector<size_t> tmpIdx3 = {0,2};
    for (size_t i = 0; i < gridsort[0]; i++) { //a_n
      tmpIdx1[0]=i; tmpIdx2[0]=i; tmpIdx3[0]=i;
      CellParams cells[3] = {cellList[getIdx(tmpIdx1)],cellList[getIdx(tmpIdx2)],cellList[getIdx(tmpIdx3)]};
      double xmn[3] = {gridlabels[1][0],gridlabels[1][1],gridlabels[1][2]}; //Get d_n point 0,1,2
      cells_dnreduced[i] = interpolate_quad(cells, xmn, d_n);
    }
  }

  //2. For the generated cells, interpolate over a_n (only 3 closest a_n's)
  size_t a_n_idx = 0;
  size_t a_n_dimension = 200000; //More likely to cause segfault if something goes wrong
  if (this->havePhaseAdvance) a_n_dimension = 1;
  else                        a_n_dimension = 0;
  if (a_n == gridlabels[a_n_dimension][4]){
    a_n_idx = 3;
  }
  else {
    for (size_t i = 2; i < 5; i++) {
      if (a_n < gridlabels[a_n_dimension][i]) {
        a_n_idx = i-1;
        break;
      }
    }
  }
  if (a_n_idx < 1 || a_n_idx > 3) {
    throw CellBaseError("a_n_idx out of range");
  }

  CellParams cells[3] = { cells_dnreduced[a_n_idx-1],
                          cells_dnreduced[a_n_idx],
                          cells_dnreduced[a_n_idx+1]  };
  double     xmn[3]   = { gridlabels[a_n_dimension][a_n_idx-1],
                          gridlabels[a_n_dimension][a_n_idx],
                          gridlabels[a_n_dimension][a_n_idx+1]  };

  // cout << a_n << endl;
  // cout << xmn[0] << " " << xmn[1] << " " << xmn[2] << endl;
  // cout << cells[0] << endl << cells[1] << endl << cells[2] << endl;

  CellParams ret = interpolate_quad(cells, xmn, a_n);
  //cout << endl << ret << endl;;
  return ret;
}

CellParams CellBase_compat::interpolate_quad(CellParams cells[], double xmn[], double x) const {
  double dx1 = xmn[1]-xmn[0];
  double dx2 = xmn[2]-xmn[1];
  double dx3 = dx1+dx2;

  CellParams a = (cells[0]*dx2 - cells[1]*dx3 + cells[2]*dx1) / (dx1*dx2*dx3);
  CellParams b = (cells[1]-cells[0])/dx1 - a*(xmn[1]+xmn[0]);
  CellParams c = cells[0] - b*xmn[0] - a*xmn[0]*xmn[0];

  return a*x*x + b*x + c;
}
