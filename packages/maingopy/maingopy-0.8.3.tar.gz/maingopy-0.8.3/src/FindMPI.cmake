

# -------------- Set Intel MPI library configuration---------------------------
# Options:
# - st: "Set this argument to use multi-threaded optimized library (with the global lock). This is the default value"
# - mt: "Set this argument to use multi-threaded optimized library (with per-object lock for the thread-split model)"
# We always use the st version.


if(WIN32)
	execute_process(COMMAND cmd /C set I_MPI_ROOT OUTPUT_VARIABLE WINGUESS1 ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
	if(NOT WINGUESS1)
		message(FATAL_ERROR "Unable to find Intel MPI: environment variable I_MPI_ROOT not set.")
	endif()
	string(REGEX REPLACE "I_MPI_ROOT=" "" WINGUESS1 ${WINGUESS1})
	file(TO_CMAKE_PATH "${WINGUESS1}" WINGUESS1) 
else()

endif()

find_path(MPI_INCLUDE_DIR
  mpi.h
  HINTS ${WINGUESS1}/intel64/include
	$ENV{MPI_INCLUDE}
  NO_DEFAULT_PATH
)
find_library(MPI_LIBST
	NAMES impi mpi
	HINTS	${WINGUESS1}/intel64/lib/release
			$ENV{MPI_LIBDIR}
	NO_DEFAULT_PATH  
)
find_library(MPI_LIBSTD
	NAMES impid mpid mpi impi
	HINTS	${WINGUESS1}/intel64/lib/debug
			$ENV{MPI_LIBDIR}
	NO_DEFAULT_PATH  
)

if(MPI_LIBST)
	message("Found MPI at ${MPI_LIBST}.")
else()
	message(FATAL_ERROR "MPI library could not be found.")
endif()
