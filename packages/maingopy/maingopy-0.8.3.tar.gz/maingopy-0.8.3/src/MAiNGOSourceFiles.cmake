
set(MAiNGO_SRC
    ${MAiNGO_SOURCE_DIR}/bab.cpp
    ${MAiNGO_SOURCE_DIR}/getTime.cpp
    ${MAiNGO_SOURCE_DIR}/ipoptProblem.cpp
    ${MAiNGO_SOURCE_DIR}/knitroProblem.cpp
    ${MAiNGO_SOURCE_DIR}/lbp.cpp
    ${MAiNGO_SOURCE_DIR}/lbpFactory.cpp
    ${MAiNGO_SOURCE_DIR}/lbpCplex.cpp
    ${MAiNGO_SOURCE_DIR}/lbpClp.cpp
    ${MAiNGO_SOURCE_DIR}/lbpDagObj.cpp
    ${MAiNGO_SOURCE_DIR}/lbpInterval.cpp
    ${MAiNGO_SOURCE_DIR}/lbpLinearizationStrats.cpp
    ${MAiNGO_SOURCE_DIR}/logger.cpp
    ${MAiNGO_SOURCE_DIR}/MAiNGO.cpp
    ${MAiNGO_SOURCE_DIR}/MAiNGOgetterFunctions.cpp
    ${MAiNGO_SOURCE_DIR}/MAiNGOmodelEpsCon.cpp
    ${MAiNGO_SOURCE_DIR}/MAiNGOprintingFunctions.cpp
    ${MAiNGO_SOURCE_DIR}/MAiNGOtoOtherLanguage.cpp
    ${MAiNGO_SOURCE_DIR}/MAiNGOwritingFunctions.cpp
    ${MAiNGO_SOURCE_DIR}/settings.cpp
    ${MAiNGO_SOURCE_DIR}/ubp.cpp
    ${MAiNGO_SOURCE_DIR}/ubpClp.cpp
    ${MAiNGO_SOURCE_DIR}/ubpCplex.cpp
    ${MAiNGO_SOURCE_DIR}/ubpFactory.cpp
    ${MAiNGO_SOURCE_DIR}/ubpIpopt.cpp
    ${MAiNGO_SOURCE_DIR}/ubpKnitro.cpp
    ${MAiNGO_SOURCE_DIR}/ubpNLopt.cpp
)

if(MAiNGO_build_parser)
    set(PARSER_SRC
        ${MAiNGO_SOURCE_DIR}/aleModel.cpp
        ${MAiNGO_SOURCE_DIR}/programParser.cpp
    )
endif()

if(MAiNGO_use_mpi)
    set(MAiNGO_SRC ${MAiNGO_SRC}
        ${MAiNGO_SOURCE_DIR}/babMpi.cpp
    )
endif()