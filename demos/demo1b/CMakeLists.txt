cmake_minimum_required(VERSION 2.8)
project(BurdenOfProof_demo1b)

set(CMAKE_VERBOSE_MAKEFILE OFF CACHE BOOL "Verbose Makefile : ON or OFF" FORCE)
set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type : Release or Debug" FORCE)

# Warnings
if(NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")
	add_definitions("-Wall -Wextra -Wpedantic")
endif()

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
find_package(Boost COMPONENTS python REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	set(Boost_LIBRARIES boost_python)

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
file(GLOB SRC_CPP src/cpp/*.cpp)
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
	file(GLOB DLLS
		${Boost_LIBRARY_DIRS}/*boost_python*${CMAKE_SHARED_LIBRARY_SUFFIX})
	file(COPY ${DLLS} DESTINATION ${CMAKE_BINARY_DIR}/app)
endif()

file(GLOB SCRIPTS src/python/*.py src/python/*.prc test/*.py)
file(COPY ${SCRIPTS} DESTINATION ${CMAKE_BINARY_DIR}/app)

file(GLOB DATA data/*)
file(COPY ${DATA} DESTINATION ${CMAKE_BINARY_DIR}/app/data)

file(COPY test/testcityblueprint.txt DESTINATION ${CMAKE_BINARY_DIR}/app/data/)

# Copy main target
get_property(target_location TARGET bop PROPERTY LOCATION)
add_custom_command(TARGET bop POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E make_directory ${PROJECT_BINARY_DIR}/app
	COMMAND ${CMAKE_COMMAND} -E copy ${target_location} ${PROJECT_BINARY_DIR}/app/)

# Target cpplint (C++ code checker)
add_custom_target(cpplint ALL)
file(GLOB SRC_ALL src/cpp/*)
foreach (f ${SRC_ALL})
	add_custom_command(TARGET cpplint COMMAND ${PYTHON_COMMAND} ${CMAKE_CURRENT_LIST_DIR}/lib/cpplint/cpplint.py --root=demos/demo1b/src/cpp ${f})
endforeach()

# Target pep8 (Python code checker)
add_custom_target(pep8 ALL DEPENDS bop)
add_custom_command(TARGET pep8 COMMAND ${PYTHON_COMMAND} ${CMAKE_CURRENT_LIST_DIR}/lib/pep8/pep8.py ${CMAKE_BINARY_DIR}/app/)

# Target tests
add_custom_target(tests ALL DEPENDS bop)

add_custom_command(TARGET tests COMMAND ${PYTHON_COMMAND} ${CMAKE_BINARY_DIR}/app/testbopmodel.py)
