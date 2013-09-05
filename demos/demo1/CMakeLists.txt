cmake_minimum_required (VERSION 2.8)
project (BurdenOfProof_demo1)

set(CMAKE_VERBOSE_MAKEFILE OFF CACHE BOOL "Verbose Makefile : ON or OFF" FORCE)
set(CMAKE_BUILD_TYPE  Debug CACHE STRING "Build type : Release or Debug" FORCE)

# Support custom cmake modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMakeModules/")


#warnings
add_definitions("-Wall -Wextra -Wpedantic")

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set(CMAKE_CXX_FLAGS "-std=c++11")
endif()

# Optimization
if(NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")
add_definitions("-march=native")
endif()

# Python command
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set(PYTHON_COMMAND python2)
else()
	set(PYTHON_COMMAND ppython)
endif()

# Dependencies
set(Boost_USE_STATIC_LIBS    OFF)
set(Boost_USE_MULTITHREADED  ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost COMPONENTS python date_time system filesystem regex REQUIRED)
#find_package(Panda3D REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	set(Boost_LIBRARIES boost_python boost_date_time boost_system boost_filesystem)

	set(PYTHON_INCLUDE_DIRS "/System/Library/Frameworks/Python.framework/Versions/2.5/Headers")
	set(PYTHON_LIBRARIES "/System/Library/Frameworks/Python.framework/Versions/2.5/Python")
	link_directories(${CMAKE_BINARY_DIR})
else()
	link_directories(${Boost_LIBRARY_DIRS})
	set(PYTHON_INCLUDE_DIRS "/usr/include/python2.7")
	set(PYTHON_LIBRARIES "/usr/lib/python2.7")
	find_package(PythonLibs 2.7 REQUIRED)
endif()
include_directories(${PYTHON_INCLUDE_DIRS})

# Main target
file(GLOB SRC_CPP cpp/*.cpp)
add_library(bop SHARED ${SRC_CPP})

target_link_libraries(bop ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
	set_target_properties(bop PROPERTIES SUFFIX ".pyd")
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set_target_properties(bop PROPERTIES PREFIX "" SUFFIX ".so")
endif()

# Files to copy
if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
	file(GLOB dlls
		${Boost_LIBRARY_DIRS}/*boost_python*${CMAKE_SHARED_LIBRARY_SUFFIX}
		${Boost_LIBRARY_DIRS}/*boost_date_time*${CMAKE_SHARED_LIBRARY_SUFFIX}
		${Boost_LIBRARY_DIRS}/*boost_system*${CMAKE_SHARED_LIBRARY_SUFFIX}
                ${Boost_LIBRARY_DIRS}/*boost_filesystem*${CMAKE_SHARED_LIBRARY_SUFFIX}
                ${Boost_LIBRARY_DIRS}/*boost_regex*${CMAKE_SHARED_LIBRARY_SUFFIX})
	file(COPY ${dlls} DESTINATION ${CMAKE_BINARY_DIR}/app)
endif()

file(GLOB SCRIPTS *.py *.prc)
file(COPY ${SCRIPTS} DESTINATION ${CMAKE_BINARY_DIR}/app)

file(GLOB MODELS models/*)
file(COPY ${MODELS} DESTINATION ${CMAKE_BINARY_DIR}/app/models)

file(GLOB TEMPORALVALUES temporalValues/*)
file(COPY ${TEMPORALVALUES} DESTINATION ${CMAKE_BINARY_DIR}/app/temporalValues)

file(GLOB PROPERTYCHRONOLOGIES propertyChronologies/*)
file(COPY ${PROPERTYCHRONOLOGIES} DESTINATION ${CMAKE_BINARY_DIR}/app/propertyChronologies)

file(GLOB PERSONAS personas/*)
file(COPY ${PERSONAS} DESTINATION ${CMAKE_BINARY_DIR}/app/personas)

# Copy main target
get_property(target_location TARGET bop PROPERTY LOCATION)
add_custom_command(TARGET bop POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E make_directory ${PROJECT_BINARY_DIR}/app
	COMMAND ${CMAKE_COMMAND} -E copy ${target_location} ${PROJECT_BINARY_DIR}/app/)

# Target cpplint
add_custom_target(cpplint ALL)
file(GLOB SRC_ALL cpp/*)
foreach (f ${SRC_ALL})
	add_custom_command(TARGET cpplint COMMAND ${PYTHON_COMMAND} ${CMAKE_CURRENT_LIST_DIR}/lib/cpplint/cpplint.py --root=demos/demo1/cpp ${f})
endforeach()

# Target testcpp
add_custom_target(testcpp ALL DEPENDS bop)

# Old version: build process stops if the program ends abruptly (eg failed C assert)
#add_custom_command(TARGET testcpp COMMAND ${PYTHON} ${CMAKE_BINARY_DIR}/app/testcpp.py)

# New version: standard and error outputs are written in testcpp.output and testcpp.error
configure_file(
  ${CMAKE_MODULE_PATH}/testcpp.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/testcpp.cmake
)
add_custom_command(TARGET testcpp COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/testcpp.cmake)
