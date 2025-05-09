# Install script for directory: /home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados")
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
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so"
         RPATH "$ORIGIN:$ORIGIN/lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/build/acados/external/hpipm/libhpipm.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so"
         OLD_RPATH "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/build/acados/external/blasfeo:"
         NEW_RPATH "$ORIGIN:$ORIGIN/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libhpipm.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/hpipmConfig.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/hpipmConfig.cmake"
         "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/build/acados/external/hpipm/CMakeFiles/Export/272ceadb8458515b2ae4b5630a6029cc/hpipmConfig.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/hpipmConfig-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/hpipmConfig.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/build/acados/external/hpipm/CMakeFiles/Export/272ceadb8458515b2ae4b5630a6029cc/hpipmConfig.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/build/acados/external/hpipm/CMakeFiles/Export/272ceadb8458515b2ae4b5630a6029cc/hpipmConfig-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/hpipm/include" TYPE FILE FILES
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_aux_mem.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_aux_string.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_common.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_cast_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_cond.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_cond_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_cond_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_core_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_core_qp_ipm_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qcqp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qcqp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qcqp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qcqp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qcqp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_dense_qp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp_red.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qcqp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_red.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_solver.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_ocp_qp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_part_cond.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_part_cond_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_sim_erk.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_sim_rk.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qcqp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qcqp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qcqp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qcqp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qcqp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_d_tree_ocp_qp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_m_dense_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_m_dense_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_m_ocp_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_m_ocp_qp_ipm_hard.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_m_ocp_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_cast_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_cond.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_cond_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_cond_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_core_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_core_qp_ipm_aux.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qcqp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qcqp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qcqp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qcqp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qcqp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_dense_qp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp_red.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qcqp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_red.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_ocp_qp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_part_cond.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_part_cond_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_sim_erk.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_sim_rk.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qcqp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qcqp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qcqp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qcqp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qcqp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qcqp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp_dim.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp_ipm.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp_kkt.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp_res.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp_sol.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_s_tree_ocp_qp_utils.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_scenario_tree.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_timing.h"
    "/home/jgillis/meco-group/rockit/rockit/external/acados/examples/build_acados_rockit/acados/external/hpipm/include/hpipm_tree.h"
    )
endif()

