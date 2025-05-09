# - Config file for the Armadillo package
# It defines the following variables
#  ARMADILLO_INCLUDE_DIRS - include directories for Armadillo
#  ARMADILLO_LIBRARY_DIRS - library directories for Armadillo (normally not used!)
#  ARMADILLO_LIBRARIES    - libraries to link against

# Tell the user project where to find our headers and libraries
set(ARMADILLO_INCLUDE_DIRS "/Users/runner/work/L0Learn/L0Learn/python/_skbuild/macosx-11.0-arm64-3.12/cmake-install/fastsparsegams/include")
set(ARMADILLO_LIBRARY_DIRS "/Users/runner/work/L0Learn/L0Learn/python/_skbuild/macosx-11.0-arm64-3.12/cmake-install/fastsparsegams/lib")

# Our library dependencies (contains definitions for IMPORTED targets)
include("/Users/runner/work/L0Learn/L0Learn/python/_skbuild/macosx-11.0-arm64-3.12/cmake-install/fastsparsegams/share/Armadillo/CMake/ArmadilloLibraryDepends.cmake")

# These are IMPORTED targets created by ArmadilloLibraryDepends.cmake
set(ARMADILLO_LIBRARIES armadillo)

