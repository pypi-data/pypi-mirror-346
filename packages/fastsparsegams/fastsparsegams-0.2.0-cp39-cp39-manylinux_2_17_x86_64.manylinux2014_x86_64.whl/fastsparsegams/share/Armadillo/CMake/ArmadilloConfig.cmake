# - Config file for the Armadillo package
# It defines the following variables
#  ARMADILLO_INCLUDE_DIRS - include directories for Armadillo
#  ARMADILLO_LIBRARY_DIRS - library directories for Armadillo (normally not used!)
#  ARMADILLO_LIBRARIES    - libraries to link against

# Tell the user project where to find our headers and libraries
set(ARMADILLO_INCLUDE_DIRS "/project/_skbuild/linux-x86_64-3.9/cmake-install/fastsparsegams/include")
set(ARMADILLO_LIBRARY_DIRS "/project/_skbuild/linux-x86_64-3.9/cmake-install/fastsparsegams/lib64")

# Our library dependencies (contains definitions for IMPORTED targets)
include("/project/_skbuild/linux-x86_64-3.9/cmake-install/fastsparsegams/share/Armadillo/CMake/ArmadilloLibraryDepends.cmake")

# These are IMPORTED targets created by ArmadilloLibraryDepends.cmake
set(ARMADILLO_LIBRARIES armadillo)

