#----------------------------------------------------------------------------
# Setup the project
cmake_minimum_required(VERSION 3.8...3.18)
if(${CMAKE_VERSION} VERSION_LESS 3.12)
  cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION})
endif()
project(rdecay01)

#----------------------------------------------------------------------------
# Find Geant4 package, activating all available UI and Vis drivers by default
# You can set WITH_GEANT4_UIVIS to OFF via the command line or ccmake/cmake-gui
# to build a batch mode only executable
#
option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

#----------------------------------------------------------------------------
# Setup Geant4 include directories and compile definitions
#
include(${Geant4_USE_FILE})

#----------------------------------------------------------------------------
# Locate sources and headers for this project
#
include_directories(${PROJECT_SOURCE_DIR}/include 
                    ${Geant4_INCLUDE_DIR})
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

# Include all mac files (inside and outside macro folder) into build folder
file(GLOB mac_files "*.mac")
file(COPY ${mac_files} DESTINATION ${PROJECT_BINARY_DIR})

file(GLOB gamma_macro_files "macros/gammas/*.mac")
file(COPY ${gamma_macro_files} DESTINATION ${PROJECT_BINARY_DIR})

file(GLOB positron_macro_files "macros/positrons/*.mac")
file(COPY ${positron_macro_files} DESTINATION ${PROJECT_BINARY_DIR})

file(GLOB electron_macro_files "macros/electrons/*.mac")
file(COPY ${electron_macro_files} DESTINATION ${PROJECT_BINARY_DIR})

# Include data files into build folder
file(GLOB data_files "*.dat")
file(COPY ${data_files} DESTINATION ${PROJECT_BINARY_DIR})

#----------------------------------------------------------------------------
# Add the executable, and link it to the Geant4 libraries
#
add_executable(rdecay01 rdecay01.cc ${sources} ${headers})
target_link_libraries(rdecay01 ${Geant4_LIBRARIES} )

#----------------------------------------------------------------------------
# Install the executable to 'bin' directory under CMAKE_INSTALL_PREFIX
#
install(TARGETS rdecay01 DESTINATION bin)

