#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ALP::ALP" for configuration "Release"
set_property(TARGET ALP::ALP APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ALP::ALP PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libALP.a"
  )

list(APPEND _cmake_import_check_targets ALP::ALP )
list(APPEND _cmake_import_check_files_for_ALP::ALP "${_IMPORT_PREFIX}/lib/libALP.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
