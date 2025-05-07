/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#pragma once

#include "settings.h"

#include <cmath>
#include <string>


namespace maingo {


/**
* @brief Function for checking if LBD is larger than UBD, or smaller by not more than the specified tolerance (absolute or relative)
*
*	This function is declared here, since it is needed in bab.cpp, ubp.cpp, and in MAiNGO.cpp
*
* @param[in] LBD is the global lower bound 
* @param[in] UBD is the global upper bound
* @param[in] mySettings is a pointer to MAiNGO settings
*/
inline bool
larger_or_equal_within_tolerance(const double LBD, const double UBD, Settings* mySettings)
{

    bool absDone = (LBD >= (UBD - mySettings->epsilonA));                     // Done means that absolute criterion is met
    bool relDone = (LBD >= (UBD - std::fabs(UBD) * mySettings->epsilonR));    // Done means that relative criterion is met
    return (absDone || relDone);                                              // If either criterion is met we are done
}

/**
* @brief Function printing the current version number
*
*	This function is declared here, since it is needed in MAiNGO.cpp, MAiNGOtoGAMS.cpp and lbp.cpp
*
* @return Returns a string of the version number as vX.X.X
*/
inline std::string
print_version()
{
    return "v0.4.0 ";
}


}    // end namespace maingo