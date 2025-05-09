#include <cstdio>
#include <cstdlib>

void init_structure_calculator() {
    if ( std::getenv("CLICOPTI_NOSPLASH") == NULL) {
        // splash message, unless env variable CLICOPTI_NOSPLASH is set
        puts("CLICopti version 2.2.1\n"
             "Copyright (C) 2014- \n"
             " Kyrre Ness Sjobak <k.n.sjobak@fys.uio.no> (CERN and University of Oslo),\n"
             " Daniel Schulte (CERN),\n"
             " Alexej Grudiev (CERN),\n"
             " Andrea Latina (CERN),\n"
             " Jim Ögren (Uppsala University and CERN)\n");
        puts("We have invested a lot of time and effort in creating and maintaining the CLICopti library,\n"
             " please cite it when using it. See the CITATION file in the source distribution\n"
             " (e.g. on https://gitlab.cern.ch/clic-software/clicopti ) for more information.\n");
    }
}

