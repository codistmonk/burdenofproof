cmake_minimum_required (VERSION 2.8)
project (BurdenOfProof_demo1)

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set(CMAKE_CXX_FLAGS "-std=c++11")
endif()

#optimization
if(NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")
add_definitions("-march=native")
endif()

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

message(${Boost_LIBRARIES})
message(${PYTHON_INCLUDE_DIRS})
message(${PYTHON_LIBRARIES})

file(GLOB SRC cpp/*.cpp)
add_library(bop SHARED ${SRC})

target_link_libraries(bop ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
	set_target_properties(bop PROPERTIES SUFFIX ".pyd")
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set_target_properties(bop PROPERTIES PREFIX "" SUFFIX ".so")
endif()

get_property(target_location TARGET bop PROPERTY LOCATION)
install(FILES ${target_location} DESTINATION ${CMAKE_BINARY_DIR}/app)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	file(GLOB dlls ${Boost_LIBRARY_DIRS}/*boost_python*${CMAKE_SHARED_LIBRARY_SUFFIX})
	install(FILES ${dlls} DESTINATION ${CMAKE_BINARY_DIR}/app)
endif()

file(GLOB scripts *.py *.prc)

install(FILES ${scripts} DESTINATION ${CMAKE_BINARY_DIR}/app)
