# Install script for directory: /home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/build/fatrop/external/blasfeo/libblasfeo.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/blasfeoConfig.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/blasfeoConfig.cmake"
         "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/build/fatrop/external/blasfeo/CMakeFiles/Export/272ceadb8458515b2ae4b5630a6029cc/blasfeoConfig.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/blasfeoConfig-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/blasfeoConfig.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/build/fatrop/external/blasfeo/CMakeFiles/Export/272ceadb8458515b2ae4b5630a6029cc/blasfeoConfig.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/build/fatrop/external/blasfeo/CMakeFiles/Export/272ceadb8458515b2ae4b5630a6029cc/blasfeoConfig-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/blasfeo/include" TYPE FILE FILES
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_block_size.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_common.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_aux_ext_dep.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_aux_ext_dep_ref.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_aux_old.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_aux_ref.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_aux_test.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_blas.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_blas_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_blasfeo_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_blasfeo_api_ref.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_blasfeo_hp_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_blasfeo_ref_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_d_kernel.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_i_aux_ext_dep.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_m_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_memory.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_naming.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_processor_features.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_aux_ext_dep.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_aux_ext_dep_ref.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_aux_old.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_aux_ref.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_aux_test.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_blas.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_blas_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_blasfeo_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_blasfeo_api_ref.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_blasfeo_ref_api.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_s_kernel.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_stdlib.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_target.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_timing.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/blasfeo_v_aux_ext_dep.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/d_blas.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/d_blas_64.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/s_blas.h"
    "/home/jgillis/meco-group/rockit/rockit/external/fatrop/build_fatrop_rockit/interface/fatrop/external/blasfeo/include/s_blas_64.h"
    )
endif()

