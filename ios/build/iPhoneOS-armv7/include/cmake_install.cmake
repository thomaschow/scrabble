# Install script for directory: /Users/thomaschow/Documents/workspace/scrabble/opencv/include

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/Users/thomaschow/Documents/workspace/scrabble/ios/build/iPhoneOS-armv7/install")
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

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv" TYPE FILE FILES
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cv.h"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cv.hpp"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cvaux.h"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cvaux.hpp"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cvwimage.h"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cxcore.h"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cxcore.hpp"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cxeigen.hpp"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/cxmisc.h"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/highgui.h"
    "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv/ml.h"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2" TYPE FILE FILES "/Users/thomaschow/Documents/workspace/scrabble/opencv/include/opencv2/opencv.hpp")
endif()
