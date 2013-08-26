cmake_minimum_required (VERSION 2.8)
project (BurdenOfProof_demo1)

set(Boost_USE_STATIC_LIBS    OFF)
set(Boost_USE_MULTITHREADED  ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost REQUIRED python)
include_directories(${Boost_INCLUDE_DIRS})

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	set(PYTHON_INCLUDE_DIRS "/System/Library/Frameworks/Python.framework/Versions/2.5/Headers")
	set(PYTHON_LIBRARIES "/System/Library/Frameworks/Python.framework/Versions/2.5/Python")
	link_directories(${CMAKE_BINARY_DIR})
	set(Boost_LIBRARIES boost_python)
else(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	link_directories(${Boost_LIBRARY_DIRS})

	find_package(PythonLibs REQUIRED)
endif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
include_directories(${PYTHON_INCLUDE_DIRS})

message(${Boost_LIBRARIES})
message(${PYTHON_INCLUDE_DIRS})
message(${PYTHON_LIBRARIES})

add_library(bop SHARED cpp/Game.cpp)

target_link_libraries(bop ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
	set_target_properties(bop PROPERTIES SUFFIX ".pyd")
endif(CMAKE_SYSTEM_NAME STREQUAL "Windows")

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	set_target_properties(bop PROPERTIES PREFIX "" SUFFIX ".so")
endif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")

get_property(target_location TARGET bop PROPERTY LOCATION)
install(FILES ${target_location} DESTINATION ${CMAKE_BINARY_DIR}/app)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	file(GLOB dlls ${Boost_LIBRARY_DIRS}/*boost_python*${CMAKE_SHARED_LIBRARY_SUFFIX})
	install(FILES ${dlls} DESTINATION ${CMAKE_BINARY_DIR}/app)
endif(NOT CMAKE_SYSTEM_NAME STREQUAL "Darwin")

file(GLOB scripts *.py *.prc)

install(FILES ${scripts} DESTINATION ${CMAKE_BINARY_DIR}/app)
