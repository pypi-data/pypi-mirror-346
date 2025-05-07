/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 * @file settings.cpp
 *
 * @brief File containing functions for specifying defaults and reading
 *        settings for MAiNGO from a file.
 *
 **********************************************************************************/

#include "settings.h"

#include <limits.h>    // Needed for maximum value for specific settings


using namespace maingo;


/////////////////////////////////////////////////////////////////////////
// constructor of settings class. Determines the default values for the different settings.
Settings::Settings()
{

    // Tolerances
    epsilonA   = 1.0e-2;
    epsilonR   = 1.0e-2;
    deltaIneq  = 1.0e-6;
    deltaEq    = 1.0e-6;
    relNodeTol = 1.0e-9;

    // Termination
    BAB_maxNodes             = std::numeric_limits<unsigned>::max();
    BAB_maxIterations        = std::numeric_limits<unsigned>::max();
    maxTime                  = 86400;    // =24h
    confirmTermination       = false;
    terminateOnFeasiblePoint = false;
    targetLowerBound         = 1.0e51;
    targetUpperBound         = -1.0e51;
    infinity                 = 1.0e51;

    // Pre-processing
    PRE_maxLocalSearches = 3;
    PRE_obbtMaxRounds    = 10;
    PRE_pureMultistart   = false;

    // B&B - Tree management
    BAB_nodeSelection  = babBase::enums::NS_BESTBOUND;
    BAB_branchVariable = babBase::enums::BV_RELDIAM;

    // B&B - Range reduction
    BAB_alwaysSolveObbt       = true;
    BAB_dbbt                  = true;
    BAB_probing               = false;
    BAB_constraintPropagation = true;

    // Lower bounding solver:
#ifdef HAVE_CPLEX
    LBP_solver = lbp::SOLVER_CPLEX;
#else
    LBP_solver = lbp::SOLVER_CLP;
#endif
    LBP_linPoints               = lbp::LINP_MID;
    LBP_subgradientIntervals    = true;
    LBP_obbtMinImprovement      = 0.01;
    LBP_activateMoreScaling     = 10000;
    LBP_addAuxiliaryVars        = false;
    LBP_minFactorsForAux        = 2;
    LBP_maxNumberOfAddedFactors = 1;

    // Default settings for MC++:
    MC_mvcompUse = true;
    MC_mvcompTol = 1e-9;
    MC_envelTol  = 1e-9;

    // Default settings for upper bounding solver:
    UBP_solverPreprocessing   = ubp::SOLVER_IPOPT;
    UBP_maxStepsPreprocessing = 3000;
    UBP_maxTimePreprocessing  = 100.;
    UBP_solverBab             = ubp::SOLVER_SLSQP;
    UBP_maxStepsBab           = 3;
    UBP_maxTimeBab            = 10.;
    UBP_ignoreNodeBounds      = false;

    // Epsilon-constraint settings
    EC_nPoints = 10;

    // Output:
    BAB_verbosity             = VERB_NORMAL;
    LBP_verbosity             = VERB_NORMAL;
    UBP_verbosity             = VERB_NORMAL;
    BAB_printFreq             = 100;
    BAB_logFreq               = 100;
    outstreamVerbosity        = OUTSTREAM_BOTH;
    writeLog                  = true;
    writeToLogSec             = 1800;
    writeResFile              = true;
    writeCsv                  = false;
    writeJson                 = false;
    PRE_printEveryLocalSearch = false;
    writeToOtherLanguage      = LANG_NONE;
}